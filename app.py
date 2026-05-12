import streamlit as st
import json
import os
import random
import string
from datetime import datetime
from pathlib import Path
import base64

# ─── Config ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Future Feminist Spaces",
    page_icon="♀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
CARDS_DIR = BASE_DIR / "assets" / "cards"
DATA_DIR = BASE_DIR / "data"
SESSIONS_FILE = DATA_DIR / "sessions.json"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "feminismo2025")

# ─── Card data ────────────────────────────────────────────────────────────────
WOMEN = [
    {"id": 1, "name": "Greta Thunberg",    "portrait": "portrait_01.jpg", "scenario": "scenario_02.jpg"},
    {"id": 2, "name": "Malala Yousafzai",  "portrait": "portrait_03.jpg", "scenario": "scenario_04.jpg"},
    {"id": 3, "name": "Maria Carolina",    "portrait": "portrait_05.jpg", "scenario": "scenario_06.jpg"},
    {"id": 4, "name": "Rosa Parks",        "portrait": "portrait_07.jpg", "scenario": "scenario_08.jpg"},
    {"id": 5, "name": "Olympe de Gouges",  "portrait": "portrait_09.jpg", "scenario": "scenario_10.jpg"},
    {"id": 6, "name": "Irmã Dulce",        "portrait": "portrait_11.jpg", "scenario": "scenario_12.jpg"},
    {"id": 7, "name": "Anita Garibaldi",   "portrait": "portrait_13.jpg", "scenario": "scenario_14.jpg"},
    {"id": 8, "name": "Dandara",           "portrait": "portrait_15.jpg", "scenario": "scenario_16.jpg"},
    {"id": 9, "name": "Maria da Penha",    "portrait": "portrait_17.jpg", "scenario": "scenario_18.jpg"},
    {"id":10, "name": "Maria Quitéria",    "portrait": "portrait_19.jpg", "scenario": "scenario_20.jpg"},
]

APPROACHES = [
    {"text": "Explique através de um objeto encontrado no lixo", "desc": "O que esse objeto descartado diria sobre como as pessoas vivem nesse cenário?"},
    {"text": "Explique como se fosse um post viral nas redes sociais", "desc": "Como esse cenário seria contado de forma viral e criativa?"},
    {"text": "Explique como se fosse uma fofoca de elevador", "desc": "Foque nos impactos pequenos e cotidianos."},
    {"text": "Explique como se fosse um manual de instruções para crianças", "desc": "Como ensinar as novas regras do mundo?"},
    {"text": "Explique como se fosse uma notícia de jornal", "desc": "Foque nos fatos: quem fez, onde, quando e qual foi a grande mudança institucional."},
    {"text": "Em vez de apresentar, formulem três perguntas", "desc": "Que perguntas fariam para mulheres que vivem essa realidade?"},
    {"text": "Criem uma propaganda do sistema dominante", "desc": "Como o sistema dominante (no passado) convenceria que esse cenário é perigoso ou impossível?"},
    {"text": "Narrem brevemente uma cena específica", "desc": "Uma cena do cotidiano dentro do cenário desse futuro discutido."},
    {"text": "Carta coringa: use a sua criatividade", "desc": "Escolha livremente como abordar a discussão."},
]

# ─── Session / persistence helpers ────────────────────────────────────────────
def load_sessions():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if SESSIONS_FILE.exists():
        with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_sessions(sessions: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)

def generate_code(length=6):
    return "".join(random.choices(string.ascii_uppercase.replace("O","").replace("I","") + string.digits.replace("0",""), k=length))

def create_game_session(name: str) -> str:
    """Admin creates a new game session. Returns the join code."""
    sessions = load_sessions()
    code = generate_code()
    while code in sessions:
        code = generate_code()
    sessions[code] = {
        "code": code,
        "name": name,
        "created_at": datetime.now().isoformat(),
        "status": "waiting",   # waiting | playing | finished
        "teams": {},           # team_name -> {responses...}
    }
    save_sessions(sessions)
    return code

def get_session(code: str):
    sessions = load_sessions()
    return sessions.get(code.upper())

def save_team_response(code: str, team: str, record: dict):
    sessions = load_sessions()
    if code not in sessions:
        return False
    sessions[code]["teams"][team] = record
    save_sessions(sessions)
    return True

def set_session_status(code: str, status: str):
    sessions = load_sessions()
    if code in sessions:
        sessions[code]["status"] = status
        save_sessions(sessions)

def img_to_b64(path: Path) -> str:
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background: #fdf8f5; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: #2d1b3d;
    padding: 10px 16px 0; border-radius: 12px 12px 0 0;
}
.stTabs [data-baseweb="tab"] {
    color: #e8d5f0 !important; font-weight: 600;
    font-size: 0.9rem; padding: 10px 20px; border-radius: 8px 8px 0 0;
}
.stTabs [aria-selected="true"] {
    background: #fdf8f5 !important; color: #2d1b3d !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #8b3a8b, #c2559c);
    color: white; border: none; border-radius: 10px;
    font-weight: 600; padding: 10px 24px; font-size: 1rem;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #7a2e7a, #b04490); color: white;
}

/* Cards */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem; color: #2d1b3d; margin-bottom: 4px;
}
.section-subtitle { color: #7a6589; font-size: 0.95rem; margin-bottom: 24px; }

/* Lobby screens */
.lobby-card {
    background: white; border-radius: 20px; padding: 40px;
    box-shadow: 0 8px 40px rgba(45,27,61,0.12);
    max-width: 560px; margin: 0 auto;
    border: 2px solid #e8d5f0;
}
.lobby-title {
    font-family: 'Playfair Display', serif; font-size: 2rem;
    color: #2d1b3d; text-align: center; margin-bottom: 8px;
}
.lobby-subtitle { color: #7a6589; text-align: center; margin-bottom: 32px; font-size: 1rem; }

.big-code {
    font-size: 3.5rem; font-weight: 800; letter-spacing: 0.2em;
    color: #8b3a8b; text-align: center; font-family: 'Playfair Display', serif;
    background: #f9f0ff; border-radius: 16px; padding: 24px;
    margin: 16px 0; border: 2px dashed #c2559c;
}
.team-pill {
    background: linear-gradient(135deg, #8b3a8b, #c2559c);
    color: white; border-radius: 24px; padding: 8px 20px;
    display: inline-block; font-weight: 600; font-size: 0.95rem; margin: 4px;
}
.step-badge {
    background: #2d1b3d; color: white; border-radius: 50%;
    width: 32px; height: 32px; display: inline-flex;
    align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.9rem; margin-right: 10px;
}
.step-label {
    font-family: 'Playfair Display', serif; font-size: 1.1rem;
    color: #2d1b3d; font-weight: 700;
}
.step-desc { color: #7a6589; font-size: 0.85rem; margin-bottom: 6px; }
.approach-pill {
    background: linear-gradient(135deg, #2d1b3d, #6b3578); color: white;
    padding: 16px 28px; border-radius: 16px; font-size: 1.05rem;
    font-weight: 600; text-align: center; margin: 12px 0;
}
.summary-section {
    background: white; border-radius: 16px; padding: 24px;
    margin-bottom: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border-left: 5px solid #8b3a8b;
}
.summary-title {
    font-family: 'Playfair Display', serif; font-size: 1.1rem;
    color: #2d1b3d; margin-bottom: 10px;
}
.tool-icon { font-size: 2.4rem; text-align: center; margin-bottom: 6px; }
.tool-label {
    font-family: 'Playfair Display', serif; font-size: 1rem;
    color: #2d1b3d; font-weight: 700; text-align: center; margin-bottom: 4px;
}
.tool-desc { color: #7a6589; font-size: 0.8rem; text-align: center; margin-bottom: 10px; line-height: 1.4; }

.status-waiting { color: #f59e0b; font-weight: 700; }
.status-playing { color: #10b981; font-weight: 700; }
.status-finished { color: #6b7280; font-weight: 700; }

/* Progress bar */
.progress-bar-wrapper {
    background: #e8d5f0; border-radius: 999px; height: 10px;
    margin: 8px 0 24px; overflow: hidden;
}
.progress-bar-fill {
    background: linear-gradient(90deg, #8b3a8b, #c2559c);
    height: 100%; border-radius: 999px; transition: width 0.4s ease;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 28px 0 16px;">
  <h1 style="font-family:'Playfair Display',serif; color:#2d1b3d; font-size:2.4rem; margin:0;">
    ♀ Future Feminist Spaces
  </h1>
  <p style="color:#7a6589; font-size:1rem; margin-top:6px;">
    Um jogo de futuros possíveis — cenários, imaginação e ação coletiva
  </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ESTADO GLOBAL: o que a pessoa está fazendo
# Possíveis valores de st.session_state["mode"]:
#   "home"       → tela inicial (entrar ou criar)
#   "lobby_join" → jogador: digitar código e nome do time
#   "playing"    → jogo ativo (tabs internas)
#   "admin_create" → admin: criar sessão
#   "admin_view"   → admin: ver respostas
# ══════════════════════════════════════════════════════════════════════════════

if "mode" not in st.session_state:
    st.session_state["mode"] = "home"

# ─────────────────────────────────────────────────────────────────────────────
# TELA: HOME
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state["mode"] == "home":
    st.markdown('<div class="lobby-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="lobby-title">Bem-vinde ao Jogo</div>
    <div class="lobby-subtitle">
        Escolha como você quer participar desta sessão de futuros feministas.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("""
        <div style="background:white; border-radius:16px; padding:28px; text-align:center;
             box-shadow:0 4px 20px rgba(45,27,61,0.1); border:2px solid #e8d5f0; min-height:200px;">
          <div style="font-size:2.5rem; margin-bottom:12px;">🎮</div>
          <div style="font-family:'Playfair Display',serif; font-size:1.3rem; color:#2d1b3d; font-weight:700; margin-bottom:8px;">
            Entrar numa Sessão
          </div>
          <div style="color:#7a6589; font-size:0.9rem; margin-bottom:20px;">
            Tenho um código de sessão e quero jogar com meu time.
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Entrar com código", key="btn_join", use_container_width=True):
            st.session_state["mode"] = "lobby_join"
            st.rerun()

    with col_b:
        st.markdown("""
        <div style="background:white; border-radius:16px; padding:28px; text-align:center;
             box-shadow:0 4px 20px rgba(45,27,61,0.1); border:2px solid #e8d5f0; min-height:200px;">
          <div style="font-size:2.5rem; margin-bottom:12px;">🔐</div>
          <div style="font-family:'Playfair Display',serif; font-size:1.3rem; color:#2d1b3d; font-weight:700; margin-bottom:8px;">
            Área da Admin
          </div>
          <div style="color:#7a6589; font-size:0.9rem; margin-bottom:20px;">
            Criar e gerenciar sessões, ver respostas de todos os times.
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔐 Acessar painel", key="btn_admin", use_container_width=True):
            st.session_state["mode"] = "admin_create"
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TELA: ENTRAR NUMA SESSÃO (jogador)
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state["mode"] == "lobby_join":
    st.markdown('<div class="lobby-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="lobby-title">Entrar na Sessão</div>
    <div class="lobby-subtitle">Digite o código fornecido pela facilitadora e o nome do seu time.</div>
    """, unsafe_allow_html=True)

    code_input = st.text_input("Código da Sessão", max_chars=6, placeholder="Ex: A3K7X2").upper().strip()
    team_input = st.text_input("Nome do Time", max_chars=40, placeholder="Ex: Time Dandara")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Entrar no jogo", use_container_width=True):
            if not code_input:
                st.error("Digite o código da sessão.")
            elif not team_input:
                st.error("Digite o nome do time.")
            else:
                session = get_session(code_input)
                if not session:
                    st.error("Código não encontrado. Verifique com a facilitadora.")
                elif session["status"] == "finished":
                    st.error("Esta sessão já foi encerrada.")
                else:
                    st.session_state["game_code"] = code_input
                    st.session_state["game_team"] = team_input
                    st.session_state["mode"] = "playing"
                    # Inicializa campos do jogo
                    for key in ["flipped_cards", "selected_card", "drawn_approach",
                                "tri_ima", "tri_foguete", "tri_balanca",
                                "wh_primeira", "wh_segunda", "wh_terceira"]:
                        if key not in st.session_state:
                            st.session_state[key] = None if key in ["selected_card","drawn_approach"] else (set() if key == "flipped_cards" else "")
                    st.rerun()
    with col2:
        if st.button("← Voltar", use_container_width=True):
            st.session_state["mode"] = "home"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TELA: ADMIN
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state["mode"] in ("admin_create", "admin_view"):

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        st.markdown('<div class="lobby-card">', unsafe_allow_html=True)
        st.markdown('<div class="lobby-title">🔐 Painel da Admin</div>', unsafe_allow_html=True)
        st.markdown('<div class="lobby-subtitle">Acesso restrito à facilitadora.</div>', unsafe_allow_html=True)
        pwd = st.text_input("Senha:", type="password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Entrar", use_container_width=True):
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
        with col2:
            if st.button("← Voltar", use_container_width=True):
                st.session_state["mode"] = "home"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Admin autenticada — tabs admin
        admin_tab1, admin_tab2 = st.tabs(["➕ Criar Sessão", "📊 Ver Respostas"])

        # ── TAB ADMIN 1: Criar sessão
        with admin_tab1:
            st.markdown('<div class="section-title">Criar Nova Sessão de Jogo</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Cada sessão tem um código único que os times usam para entrar.</div>', unsafe_allow_html=True)

            session_name = st.text_input("Nome da sessão", placeholder="Ex: Oficina Recife - Turma A")

            if st.button("🎲 Criar sessão e gerar código"):
                if not session_name.strip():
                    st.error("Digite um nome para a sessão.")
                else:
                    code = create_game_session(session_name.strip())
                    st.session_state["admin_created_code"] = code
                    st.session_state["admin_created_name"] = session_name.strip()
                    st.rerun()

            if "admin_created_code" in st.session_state:
                code = st.session_state["admin_created_code"]
                name = st.session_state["admin_created_name"]
                session_data = get_session(code)

                st.markdown(f"""
                <div style="background:white; border-radius:20px; padding:32px;
                     box-shadow:0 4px 24px rgba(45,27,61,0.12); border:2px solid #e8d5f0;
                     max-width:540px; margin:24px auto; text-align:center;">
                  <div style="color:#7a6589; font-size:0.9rem; margin-bottom:4px;">Sessão criada com sucesso!</div>
                  <div style="font-family:'Playfair Display',serif; font-size:1.5rem; color:#2d1b3d; margin-bottom:16px;">
                    {name}
                  </div>
                  <div style="color:#7a6589; font-size:0.85rem; margin-bottom:8px;">Código para os times entrarem:</div>
                  <div class="big-code">{code}</div>
                  <div style="color:#7a6589; font-size:0.85rem; margin-top:12px;">
                    Mostre este código no projetor ou no quadro para que os times possam entrar.
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # Times conectados
                teams = session_data.get("teams", {}) if session_data else {}
                if teams:
                    st.markdown(f"**Times que já enviaram respostas ({len(teams)}):**")
                    for t in teams:
                        st.markdown(f'<span class="team-pill">♀ {t}</span>', unsafe_allow_html=True)
                else:
                    st.info("Nenhum time enviou respostas ainda. Aguarde...")

                col_r, col_e = st.columns(2)
                with col_r:
                    if st.button("🔄 Atualizar lista de times"):
                        st.rerun()
                with col_e:
                    if st.button("⛔ Encerrar sessão"):
                        set_session_status(code, "finished")
                        st.success("Sessão encerrada!")
                        st.rerun()

        # ── TAB ADMIN 2: Ver respostas
        with admin_tab2:
            st.markdown('<div class="section-title">Respostas das Sessões</div>', unsafe_allow_html=True)
            sessions = load_sessions()

            if not sessions:
                st.info("Nenhuma sessão criada ainda.")
            else:
                session_options = {
                    f"{v['name']} ({k}) — {v.get('status','?')}": k
                    for k, v in sessions.items()
                }
                chosen_label = st.selectbox("Selecione uma sessão para ver as respostas:", list(session_options.keys()))
                chosen_code = session_options[chosen_label]
                session_data = sessions[chosen_code]

                status_emoji = {"waiting":"⏳ Aguardando","playing":"▶ Em andamento","finished":"✅ Encerrada"}.get(session_data["status"],"?")
                st.markdown(f"**Status:** {status_emoji} &nbsp;|&nbsp; **Código:** `{chosen_code}` &nbsp;|&nbsp; **Criada:** {session_data['created_at'][:16].replace('T',' ')}")

                teams = session_data.get("teams", {})
                if not teams:
                    st.info("Nenhum time enviou respostas nesta sessão.")
                else:
                    st.markdown(f"**{len(teams)} time(s) com respostas:**")
                    for team_name, record in teams.items():
                        with st.expander(f"♀ {team_name} — {record.get('selected_card','?')}"):
                            c1, c2 = st.columns(2)
                            with c1:
                                st.markdown(f"**Carta:** {record.get('selected_card','—')}")
                                st.markdown(f"**Abordagem:** {record.get('approach','—')}")
                            with c2:
                                st.markdown(f"**Salvo em:** {record.get('timestamp','—')[:16].replace('T',' ')}")

                            st.markdown("**Future Triangle:**")
                            tri = record.get("triangle", {})
                            tc1, tc2, tc3 = st.columns(3)
                            with tc1:
                                st.markdown("🧲 **IMA**")
                                st.markdown(tri.get("ima") or "_vazio_")
                            with tc2:
                                st.markdown("🚀 **FOGUETE**")
                                st.markdown(tri.get("foguete") or "_vazio_")
                            with tc3:
                                st.markdown("⚖️ **BALANÇA**")
                                st.markdown(tri.get("balanca") or "_vazio_")

                            st.markdown("**Future Wheel:**")
                            wh = record.get("wheel", {})
                            wc1, wc2, wc3 = st.columns(3)
                            with wc1:
                                st.markdown("1️⃣ **1ª Ordem**")
                                st.markdown(wh.get("primeira") or "_vazio_")
                            with wc2:
                                st.markdown("2️⃣ **2ª Ordem**")
                                st.markdown(wh.get("segunda") or "_vazio_")
                            with wc3:
                                st.markdown("3️⃣ **3ª Ordem**")
                                st.markdown(wh.get("terceira") or "_vazio_")

                    # Download CSV
                    import pandas as pd
                    rows = []
                    for tn, rec in teams.items():
                        rows.append({
                            "Time": tn,
                            "Sessão": session_data["name"],
                            "Carta": rec.get("selected_card",""),
                            "Abordagem": rec.get("approach",""),
                            "IMA": rec.get("triangle",{}).get("ima",""),
                            "Foguete": rec.get("triangle",{}).get("foguete",""),
                            "Balança": rec.get("triangle",{}).get("balanca",""),
                            "1ª Ordem": rec.get("wheel",{}).get("primeira",""),
                            "2ª Ordem": rec.get("wheel",{}).get("segunda",""),
                            "3ª Ordem": rec.get("wheel",{}).get("terceira",""),
                            "Timestamp": rec.get("timestamp",""),
                        })
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇️ Baixar respostas como CSV",
                        data=csv,
                        file_name=f"feminist_futures_{chosen_code}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                    )

        col_logout, _ = st.columns([1, 3])
        with col_logout:
            if st.button("← Sair do painel"):
                st.session_state.admin_auth = False
                st.session_state.mode = "home"
                if "admin_created_code" in st.session_state:
                    del st.session_state["admin_created_code"]
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TELA: JOGO ATIVO (times jogando)
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state["mode"] == "playing":
    code = st.session_state.get("game_code", "")
    team = st.session_state.get("game_team", "")
    session = get_session(code)

    # Header do jogo
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between;
         background:#2d1b3d; border-radius:12px; padding:14px 24px; margin-bottom:20px;">
      <div>
        <span style="color:#e8d5f0; font-size:0.85rem;">Sessão</span><br>
        <span style="color:white; font-weight:700; font-size:1rem;">{session['name'] if session else code}</span>
      </div>
      <div style="text-align:center;">
        <span style="color:#c2559c; font-size:2rem; font-weight:800; font-family:'Playfair Display',serif;">♀</span>
      </div>
      <div style="text-align:right;">
        <span style="color:#e8d5f0; font-size:0.85rem;">Time</span><br>
        <span style="color:white; font-weight:700; font-size:1rem;">{team}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Verifica se sessão foi encerrada pelo admin
    if session and session.get("status") == "finished":
        st.error("⛔ Esta sessão foi encerrada pela facilitadora. Obrigada por jogar!")
        if st.button("← Voltar ao início"):
            st.session_state["mode"] = "home"
            st.rerun()
        st.stop()

    # ── Inicializa estado interno
    if "flipped_cards" not in st.session_state or st.session_state["flipped_cards"] is None:
        st.session_state["flipped_cards"] = set()
    if "game_submitted" not in st.session_state:
        st.session_state["game_submitted"] = False

    if st.session_state.get("game_submitted"):
        st.balloons()
        st.success("🎉 Suas respostas foram enviadas com sucesso! Aguarde a facilitadora.")
        st.markdown(f"""
        <div style="background:white; border-radius:16px; padding:32px; text-align:center;
             box-shadow:0 4px 20px rgba(0,0,0,0.1); max-width:480px; margin:24px auto;">
          <div style="font-size:3rem; margin-bottom:12px;">♀</div>
          <div style="font-family:'Playfair Display',serif; font-size:1.4rem; color:#2d1b3d; margin-bottom:8px;">
            Missão cumprida, {team}!
          </div>
          <div style="color:#7a6589;">
            Suas reflexões sobre futuros feministas foram salvas. Obrigada por jogar!
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Sair do jogo"):
            for k in ["game_code","game_team","game_submitted","flipped_cards","selected_card",
                      "drawn_approach","tri_ima","tri_foguete","tri_balanca","wh_primeira","wh_segunda","wh_terceira"]:
                st.session_state.pop(k, None)
            st.session_state["mode"] = "home"
            st.rerun()
        st.stop()

    # ── TABS DO JOGO ──
    # Progresso
    selected = st.session_state.get("selected_card")
    approach = st.session_state.get("drawn_approach")
    tri_done = any([st.session_state.get("tri_ima"), st.session_state.get("tri_foguete"), st.session_state.get("tri_balanca")])
    wh_done  = any([st.session_state.get("wh_primeira"), st.session_state.get("wh_segunda"), st.session_state.get("wh_terceira")])
    steps_done = sum([bool(selected), bool(approach), tri_done, wh_done])
    pct = int(steps_done / 4 * 100)
    st.markdown(f"""
    <div style="font-size:0.8rem; color:#7a6589; margin-bottom:2px;">Progresso do time: {pct}%</div>
    <div class="progress-bar-wrapper">
      <div class="progress-bar-fill" style="width:{pct}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    gtab1, gtab2, gtab3, gtab4 = st.tabs([
        "1️⃣ CARTA & ABORDAGEM",
        "2️⃣ FUTURE TRIANGLE",
        "3️⃣ FUTURE WHEEL",
        "4️⃣ ENVIAR",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # GAME TAB 1: Carta & Abordagem
    # ══════════════════════════════════════════════════════════════════════════
    with gtab1:
        st.markdown('<div class="section-title">Escolha uma Carta</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Clique em "Virar carta" para revelar o cenário futuro de cada mulher. Escolha uma para seu time explorar.</div>', unsafe_allow_html=True)

        cols = st.columns(5)
        for idx, woman in enumerate(WOMEN):
            col = cols[idx % 5]
            with col:
                portrait_path = CARDS_DIR / woman["portrait"]
                scenario_path = CARDS_DIR / woman["scenario"]
                is_flipped = woman["id"] in st.session_state["flipped_cards"]
                is_selected = (selected is not None and selected["id"] == woman["id"])

                img_path = scenario_path if is_flipped else portrait_path
                border = "3px solid #8b3a8b" if is_selected else ("3px solid #c2559c" if is_flipped else "3px solid transparent")

                b64 = img_to_b64(img_path)
                if b64:
                    st.markdown(
                        f'<img src="data:image/jpeg;base64,{b64}" '
                        f'style="width:100%; border-radius:12px; border:{border}; '
                        f'box-shadow:0 4px 16px rgba(0,0,0,0.15); cursor:pointer;" />',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div style="width:100%;height:120px;background:#f0e0fa;border-radius:12px;'
                        f'border:{border};display:flex;align-items:center;justify-content:center;'
                        f'font-size:2rem;">♀</div>', unsafe_allow_html=True
                    )

                if is_flipped:
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        label = "✅ Ok" if is_selected else "Selecionar"
                        if st.button(label, key=f"sel_{woman['id']}"):
                            if is_selected:
                                st.session_state["selected_card"] = None
                            else:
                                st.session_state["selected_card"] = woman
                            st.rerun()
                    with bc2:
                        if st.button("↩️", key=f"unflip_{woman['id']}"):
                            st.session_state["flipped_cards"].discard(woman["id"])
                            if is_selected:
                                st.session_state["selected_card"] = None
                            st.rerun()
                else:
                    if st.button("Virar carta", key=f"flip_{woman['id']}"):
                        st.session_state["flipped_cards"].add(woman["id"])
                        st.rerun()

                st.markdown(
                    f'<p style="text-align:center;font-size:0.76rem;color:#2d1b3d;'
                    f'font-weight:{"700" if is_selected else "400"};margin-top:4px;">'
                    f'{woman["name"]}</p>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown('<div class="section-title">Sorteie uma Abordagem</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">A abordagem guia como vocês vão explorar o cenário escolhido.</div>', unsafe_allow_html=True)

        col_btn, col_res = st.columns([1, 2])
        with col_btn:
            if st.button("🎲 Sortear Abordagem"):
                st.session_state["drawn_approach"] = random.choice(APPROACHES)
                st.rerun()
        with col_res:
            if approach:
                st.markdown(
                    f'<div class="approach-pill">✦ {approach["text"]}<br>'
                    f'<span style="font-size:0.85rem;font-weight:400;opacity:0.88;">{approach["desc"]}</span></div>',
                    unsafe_allow_html=True,
                )

        if selected and approach:
            st.success(f"✅ Carta: **{selected['name']}** | Abordagem sorteada — avance para o **Future Triangle**!")
        elif selected:
            st.info("Agora sorteie uma abordagem para continuar!")
        elif approach:
            st.info("Agora selecione uma carta para continuar!")

    # ══════════════════════════════════════════════════════════════════════════
    # GAME TAB 2: Future Triangle
    # ══════════════════════════════════════════════════════════════════════════
    with gtab2:
        if not selected:
            st.info("⬅️ Primeiro escolha uma carta na aba **Carta & Abordagem**.")
        else:
            ctx1, ctx2 = st.columns([1, 3])
            with ctx1:
                b64 = img_to_b64(CARDS_DIR / selected["portrait"])
                if b64:
                    st.markdown(f'<img src="data:image/jpeg;base64,{b64}" style="width:80%;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.15);" />', unsafe_allow_html=True)
            with ctx2:
                ap_label = approach["text"] if approach else ""
                ap_desc  = approach["desc"]  if approach else ""
                st.markdown(
                    f'<div class="section-title">Future Triangle</div>'
                    f'<div class="section-subtitle">Cenário de <strong>{selected["name"]}</strong>'
                    f'{"<br>Abordagem: <em>" + ap_label + "</em> — " + ap_desc if approach else ""}</div>',
                    unsafe_allow_html=True,
                )
                b64s = img_to_b64(CARDS_DIR / selected["scenario"])
                if b64s:
                    st.markdown(f'<img src="data:image/jpeg;base64,{b64s}" style="width:50%;border-radius:12px;" />', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown('<p style="text-align:center;color:#7a6589;margin-bottom:20px;">O Future Triangle mapeia três forças que moldam o futuro. Escreva as reflexões do time em cada campo.</p>', unsafe_allow_html=True)

            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                st.markdown('<div class="tool-icon">🧲</div><div class="tool-label">IMA — Futuro Desejável</div><div class="tool-desc">Qual o futuro que queremos atrair? A visão que nos puxa para frente.</div>', unsafe_allow_html=True)
                val = st.text_area("IMA", value=st.session_state.get("tri_ima",""), height=180, key="tri_ima_w", label_visibility="collapsed", placeholder="O que queremos criar?")
                st.session_state["tri_ima"] = val
            with tc2:
                st.markdown('<div class="tool-icon">🚀</div><div class="tool-label">FOGUETE — Impulsos do Presente</div><div class="tool-desc">O que no presente já empurra na direção desse futuro?</div>', unsafe_allow_html=True)
                val = st.text_area("FOGUETE", value=st.session_state.get("tri_foguete",""), height=180, key="tri_foguete_w", label_visibility="collapsed", placeholder="Que forças já existem?")
                st.session_state["tri_foguete"] = val
            with tc3:
                st.markdown('<div class="tool-icon">⚖️</div><div class="tool-label">BALANÇA — Peso do Passado</div><div class="tool-desc">O que do passado ainda pesa e impacta esse cenário?</div>', unsafe_allow_html=True)
                val = st.text_area("BALANÇA", value=st.session_state.get("tri_balanca",""), height=180, key="tri_balanca_w", label_visibility="collapsed", placeholder="Que heranças históricas persistem?")
                st.session_state["tri_balanca"] = val

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Salvar Triangle e continuar", key="save_tri"):
                st.success("Triangle salvo! Avance para o **Future Wheel**.")

    # ══════════════════════════════════════════════════════════════════════════
    # GAME TAB 3: Future Wheel
    # ══════════════════════════════════════════════════════════════════════════
    with gtab3:
        if not selected:
            st.info("⬅️ Primeiro escolha uma carta na aba **Carta & Abordagem**.")
        else:
            ctx1, ctx2 = st.columns([1,3])
            with ctx1:
                b64 = img_to_b64(CARDS_DIR / selected["portrait"])
                if b64:
                    st.markdown(f'<img src="data:image/jpeg;base64,{b64}" style="width:80%;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.15);" />', unsafe_allow_html=True)
            with ctx2:
                ap_label = approach["text"] if approach else ""
                ap_desc  = approach["desc"]  if approach else ""
                st.markdown(
                    f'<div class="section-title">Future Wheel</div>'
                    f'<div class="section-subtitle">Cenário de <strong>{selected["name"]}</strong>'
                    f'{"<br>Abordagem: <em>" + ap_label + "</em> — " + ap_desc if approach else ""}</div>',
                    unsafe_allow_html=True,
                )
                b64s = img_to_b64(CARDS_DIR / selected["scenario"])
                if b64s:
                    st.markdown(f'<img src="data:image/jpeg;base64,{b64s}" style="width:50%;border-radius:12px;" />', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown('<p style="text-align:center;color:#7a6589;margin-bottom:20px;">O Future Wheel explora impactos em ondas — cada consequência gera novas consequências.</p>', unsafe_allow_html=True)

            wc1, wc2, wc3 = st.columns(3)
            with wc1:
                st.markdown('<div class="tool-icon">1️⃣</div><div class="tool-label">Impacto de 1ª Ordem</div><div class="tool-desc">Os efeitos diretos e imediatos do cenário. O que muda primeiro?</div>', unsafe_allow_html=True)
                val = st.text_area("1ª", value=st.session_state.get("wh_primeira",""), height=180, key="wh1_w", label_visibility="collapsed", placeholder="Consequências diretas e imediatas?")
                st.session_state["wh_primeira"] = val
            with wc2:
                st.markdown('<div class="tool-icon">2️⃣</div><div class="tool-label">Impacto de 2ª Ordem</div><div class="tool-desc">As consequências das consequências. O que emerge em seguida?</div>', unsafe_allow_html=True)
                val = st.text_area("2ª", value=st.session_state.get("wh_segunda",""), height=180, key="wh2_w", label_visibility="collapsed", placeholder="Como os impactos de 1ª geram novos efeitos?")
                st.session_state["wh_segunda"] = val
            with wc3:
                st.markdown('<div class="tool-icon">3️⃣</div><div class="tool-label">Impacto de 3ª Ordem</div><div class="tool-desc">Transformações profundas e sistêmicas.</div>', unsafe_allow_html=True)
                val = st.text_area("3ª", value=st.session_state.get("wh_terceira",""), height=180, key="wh3_w", label_visibility="collapsed", placeholder="Que transformações estruturais surgem?")
                st.session_state["wh_terceira"] = val

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Salvar Wheel e continuar", key="save_wh"):
                st.success("Wheel salvo! Avance para **Enviar** e finalize.")

    # ══════════════════════════════════════════════════════════════════════════
    # GAME TAB 4: Enviar
    # ══════════════════════════════════════════════════════════════════════════
    with gtab4:
        st.markdown('<div class="section-title">Resumo & Envio</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Revise as respostas do time antes de enviar para a facilitadora.</div>', unsafe_allow_html=True)

        if not selected:
            st.warning("⚠️ Você ainda não escolheu uma carta. Volte para a aba 1.")
        else:
            # Carta
            r1, r2 = st.columns(2)
            with r1:
                st.markdown('<div class="summary-section">', unsafe_allow_html=True)
                st.markdown('<div class="summary-title">🃏 Carta Selecionada</div>', unsafe_allow_html=True)
                b64p = img_to_b64(CARDS_DIR / selected["portrait"])
                b64s = img_to_b64(CARDS_DIR / selected["scenario"])
                pc1, pc2 = st.columns(2)
                with pc1:
                    if b64p: st.markdown(f'<img src="data:image/jpeg;base64,{b64p}" style="width:100%;border-radius:8px;"/>', unsafe_allow_html=True)
                with pc2:
                    if b64s: st.markdown(f'<img src="data:image/jpeg;base64,{b64s}" style="width:100%;border-radius:8px;"/>', unsafe_allow_html=True)
                st.markdown(f'<p style="text-align:center;font-weight:700;color:#2d1b3d;margin-top:6px;">{selected["name"]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with r2:
                st.markdown('<div class="summary-section">', unsafe_allow_html=True)
                st.markdown('<div class="summary-title">🎲 Abordagem Sorteada</div>', unsafe_allow_html=True)
                if approach:
                    st.markdown(f'<div class="approach-pill">✦ {approach["text"]}<br><span style="font-size:0.82rem;font-weight:400;opacity:0.9;">{approach["desc"]}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown("_Nenhuma abordagem sorteada._")
                st.markdown('</div>', unsafe_allow_html=True)

            # Triangle
            st.markdown('<div class="summary-section">', unsafe_allow_html=True)
            st.markdown('<div class="summary-title">🔺 Future Triangle</div>', unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown("**🧲 IMA**"); st.markdown(st.session_state.get("tri_ima") or "_vazio_")
            with sc2:
                st.markdown("**🚀 FOGUETE**"); st.markdown(st.session_state.get("tri_foguete") or "_vazio_")
            with sc3:
                st.markdown("**⚖️ BALANÇA**"); st.markdown(st.session_state.get("tri_balanca") or "_vazio_")
            st.markdown('</div>', unsafe_allow_html=True)

            # Wheel
            st.markdown('<div class="summary-section">', unsafe_allow_html=True)
            st.markdown('<div class="summary-title">⚙️ Future Wheel</div>', unsafe_allow_html=True)
            sw1, sw2, sw3 = st.columns(3)
            with sw1:
                st.markdown("**1️⃣ 1ª Ordem**"); st.markdown(st.session_state.get("wh_primeira") or "_vazio_")
            with sw2:
                st.markdown("**2️⃣ 2ª Ordem**"); st.markdown(st.session_state.get("wh_segunda") or "_vazio_")
            with sw3:
                st.markdown("**3️⃣ 3ª Ordem**"); st.markdown(st.session_state.get("wh_terceira") or "_vazio_")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Pronto para enviar?")
            st.markdown("Ao clicar em **Enviar respostas**, suas reflexões serão salvas e visíveis para a facilitadora.")

            if st.button("✅ Enviar respostas do time", key="final_submit"):
                record = {
                    "team": team,
                    "session_code": code,
                    "timestamp": datetime.now().isoformat(),
                    "selected_card": selected["name"] if selected else None,
                    "approach": approach["text"] if approach else None,
                    "triangle": {
                        "ima":     st.session_state.get("tri_ima", ""),
                        "foguete": st.session_state.get("tri_foguete", ""),
                        "balanca": st.session_state.get("tri_balanca", ""),
                    },
                    "wheel": {
                        "primeira": st.session_state.get("wh_primeira", ""),
                        "segunda":  st.session_state.get("wh_segunda", ""),
                        "terceira": st.session_state.get("wh_terceira", ""),
                    },
                }
                ok = save_team_response(code, team, record)
                if ok:
                    st.session_state["game_submitted"] = True
                    st.rerun()
                else:
                    st.error("Erro ao salvar. Verifique se o código da sessão ainda é válido.")

