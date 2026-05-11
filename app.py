import streamlit as st
import json
import os
import random
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
DATA_FILE = BASE_DIR / "data" / "responses.json"
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
    {
        "text": "Explique através de um objeto encontrado no lixo",
        "desc": "O que esse objeto descartado diria sobre como as pessoas vivem nesse cenário?",
    },
    {
        "text": "Explique como se fosse um post viral nas redes sociais",
        "desc": "Como esse cenário seria contado de forma viral e criativa?",
    },
    {
        "text": "Explique como se fosse uma fofoca de elevador",
        "desc": "Foque nos impactos pequenos e cotidianos.",
    },
    {
        "text": "Explique como se fosse um manual de instruções para crianças",
        "desc": "Como ensinar as novas regras do mundo?",
    },
    {
        "text": "Explique como se fosse uma notícia de jornal",
        "desc": "Foque nos fatos: quem fez, onde, quando e qual foi a grande mudança institucional.",
    },
    {
        "text": "Em vez de apresentar, formulem três perguntas",
        "desc": "Que perguntas fariam para mulheres que vivem essa realidade?",
    },
    {
        "text": "Criem uma propaganda do sistema dominante",
        "desc": "Como o sistema dominante (no passado) convenceria que esse cenário é perigoso ou impossível?",
    },
    {
        "text": "Narrem brevemente uma cena específica",
        "desc": "Uma cena do cotidiano dentro do cenário desse futuro discutido.",
    },
    {
        "text": "Carta coringa: use a sua criatividade",
        "desc": "Escolha livremente como abordar a discussão.",
    },
]

# ─── Helpers ──────────────────────────────────────────────────────────────────
def img_to_b64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def load_responses():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_response(record: dict):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    responses = load_responses()
    # Update if same session_id exists, else append
    for i, r in enumerate(responses):
        if r.get("session_id") == record.get("session_id"):
            responses[i] = record
            break
    else:
        responses.append(record)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)

def get_or_create_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S_") + str(random.randint(1000, 9999))
    return st.session_state.session_id

def build_record():
    sid = get_or_create_session()
    selected = st.session_state.get("selected_card")
    approach = st.session_state.get("drawn_approach")
    approach_text = approach["text"] if approach else None
    return {
        "session_id": sid,
        "timestamp": datetime.now().isoformat(),
        "selected_card": selected["name"] if selected else None,
        "approach": approach_text,
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

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: #fdf8f5; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #2d1b3d;
    padding: 10px 16px 0;
    border-radius: 12px 12px 0 0;
}
.stTabs [data-baseweb="tab"] {
    color: #e8d5f0 !important;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 10px 20px;
    border-radius: 8px 8px 0 0;
}
.stTabs [aria-selected="true"] {
    background: #fdf8f5 !important;
    color: #2d1b3d !important;
}

/* Cards */
.card-container {
    perspective: 1000px;
    cursor: pointer;
    margin: 8px;
}
.flip-card-inner {
    transition: transform 0.6s;
    transform-style: preserve-3d;
    position: relative;
}
.flipped .flip-card-inner { transform: rotateY(180deg); }
.flip-card-front, .flip-card-back {
    backface-visibility: hidden;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
.flip-card-back { transform: rotateY(180deg); position: absolute; top:0; left:0; width:100%; }

/* Section headers */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #2d1b3d;
    margin-bottom: 4px;
}
.section-subtitle {
    color: #7a6589;
    font-size: 0.95rem;
    margin-bottom: 24px;
}

/* Selected badge */
.selected-badge {
    background: linear-gradient(135deg, #8b3a8b, #c2559c);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 12px;
}

/* Approach pill */
.approach-pill {
    background: linear-gradient(135deg, #2d1b3d, #6b3578);
    color: white;
    padding: 16px 28px;
    border-radius: 16px;
    font-size: 1.1rem;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 4px 16px rgba(45,27,61,0.3);
    margin: 16px 0;
}

/* Future tool icons */
.tool-icon {
    font-size: 3rem;
    text-align: center;
    margin-bottom: 8px;
}
.tool-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: #2d1b3d;
    font-weight: 700;
    text-align: center;
    margin-bottom: 4px;
}
.tool-desc {
    color: #7a6589;
    font-size: 0.82rem;
    text-align: center;
    margin-bottom: 12px;
    line-height: 1.4;
}

/* Banner */
.banner {
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 24px;
    max-height: 220px;
    object-fit: cover;
}

/* Summary card */
.summary-section {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border-left: 5px solid #8b3a8b;
}
.summary-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #2d1b3d;
    margin-bottom: 12px;
}

/* Drag/draw button */
.stButton > button {
    background: linear-gradient(135deg, #8b3a8b, #c2559c);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 24px;
    font-size: 1rem;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #7a2e7a, #b04490);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 32px 0 20px;">
  <h1 style="font-family:'Playfair Display',serif; color:#2d1b3d; font-size:2.6rem; margin:0;">
    ♀ Future Feminist Spaces
  </h1>
  <p style="color:#7a6589; font-size:1.05rem; margin-top:6px;">
    Um jogo de futuros possíveis — cenários, imaginação e ação coletiva
  </p>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "CENÁRIOS & ABORDAGENS",
    "🔺 FUTURE TRIANGLE",
    "⚙️ FUTURE WHEEL",
    "SEU RESUMO",
    "Admin",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Cenários & Abordagens
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Escolha uma Carta</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Clique numa mulher para revelar o cenário do futuro associado a ela.</div>', unsafe_allow_html=True)

    if "flipped_cards" not in st.session_state:
        st.session_state.flipped_cards = set()
    if "selected_card" not in st.session_state:
        st.session_state.selected_card = None

    cols = st.columns(5)
    for idx, woman in enumerate(WOMEN):
        col = cols[idx % 5]
        with col:
            portrait_path = CARDS_DIR / woman["portrait"]
            scenario_path = CARDS_DIR / woman["scenario"]
            is_flipped = woman["id"] in st.session_state.flipped_cards
            is_selected = (
                st.session_state.selected_card is not None
                and st.session_state.selected_card["id"] == woman["id"]
            )

            if is_flipped:
                img_path = scenario_path
                border = "3px solid #8b3a8b" if is_selected else "3px solid #c2559c"
            else:
                img_path = portrait_path
                border = "3px solid transparent"

            b64 = img_to_b64(img_path)
            st.markdown(
                f'<img src="data:image/jpeg;base64,{b64}" '
                f'style="width:100%; border-radius:12px; border:{border}; '
                f'box-shadow:0 4px 16px rgba(0,0,0,0.15); cursor:pointer;" />',
                unsafe_allow_html=True,
            )

            if is_flipped:
                # Cria duas colunas pequenas para os botões de ação na carta virada
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if is_selected:
                        if st.button("✅ Ok", key=f"sel_{woman['id']}"):
                            st.session_state.selected_card = None
                            st.rerun()
                    else:
                        if st.button("Selecionar", key=f"sel_{woman['id']}"):
                            st.session_state.selected_card = woman
                            st.rerun()
                
                with btn_col2:
                    if st.button("↩️ Voltar", key=f"unflip_{woman['id']}"):
                        # Remove o ID da mulher do conjunto de cartas viradas
                        st.session_state.flipped_cards.remove(woman["id"])
                        # Se ela estava selecionada, deseleciona ao desvirar (opcional)
                        if is_selected:
                            st.session_state.selected_card = None
                        st.rerun()
            else:
                if st.button(f"Virar carta", key=f"flip_{woman['id']}"):
                    st.session_state.flipped_cards.add(woman["id"])
                    st.rerun()

            st.markdown(
                f'<p style="text-align:center;font-size:0.78rem;color:#2d1b3d;'
                f'font-weight:{"700" if is_selected else "400"};margin-top:4px;">'
                f'{woman["name"]}</p>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Approach draw
    st.markdown('<div class="section-title">Sorteie uma Abordagem</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">A abordagem guiará como você vai pensar o cenário escolhido.</div>', unsafe_allow_html=True)

    col_btn, col_result = st.columns([1, 2])
    with col_btn:
        if st.button("🎲 Sortear Abordagem"):
            st.session_state.drawn_approach = random.choice(APPROACHES)
            st.rerun()

    with col_result:
        if st.session_state.get("drawn_approach"):
            ap = st.session_state.drawn_approach
            st.markdown(
                f'<div class="approach-pill">✦ {ap["text"]}<br>'
                f'<span style="font-size:0.85rem;font-weight:400;opacity:0.88;">{ap["desc"]}</span></div>',
                unsafe_allow_html=True,
            )

    # Status
    if st.session_state.get("selected_card"):
        card = st.session_state.selected_card
        ap = st.session_state.get("drawn_approach")
        approach_label = ap["text"] if ap else "—"
        st.success(
            f"✅ Carta selecionada: **{card['name']}** | "
            f"Abordagem: **{approach_label}** — Vá para a aba **Future Triangle** para continuar!"
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Future Triangle
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    selected = st.session_state.get("selected_card")
    approach = st.session_state.get("drawn_approach")

    if not selected:
        st.info("⬅️ Primeiro escolha uma carta na aba **Cenários & Abordagens**.")
    else:
        # Show context
        ctx_col1, ctx_col2 = st.columns([1, 3])
        with ctx_col1:
            b64 = img_to_b64(CARDS_DIR / selected["portrait"])
            st.markdown(
                f'<img src="data:image/jpeg;base64,{b64}" '
                f'style="width:100%;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.15);" />',
                unsafe_allow_html=True,
            )
        with ctx_col2:
            approach_label = approach["text"] if approach else ""
            approach_desc  = approach["desc"]  if approach else ""
            st.markdown(
                f'<div class="section-title">Future Triangle</div>'
                f'<div class="section-subtitle">'
                f'Cenário de <strong>{selected["name"]}</strong>'
                f'{"<br>Abordagem: <em>" + approach_label + "</em> — " + approach_desc if approach else ""}'
                f'</div>',
                unsafe_allow_html=True,
            )
            b64s = img_to_b64(CARDS_DIR / selected["scenario"])
            st.markdown(
                f'<img src="data:image/jpeg;base64,{b64s}" '
                f'style="width:350%;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.12);" />',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            '<p style="text-align:center;color:#7a6589;margin-bottom:24px;">'
            'O Future Triangle mapeia três forças que moldam o futuro. '
            'Escreva suas reflexões em cada campo abaixo.</p>',
            unsafe_allow_html=True,
        )

        tri_col1, tri_col2, tri_col3 = st.columns(3)

        with tri_col1:
            st.markdown(
                '<div class="tool-icon">🧲</div>'
                '<div class="tool-label">IMA — Futuro Desejável</div>'
                '<div class="tool-desc">Qual o futuro que queremos atrair?<br>'
                'A visão que nos puxa para frente.</div>',
                unsafe_allow_html=True,
            )
            tri_ima = st.text_area(
                "Descreva o futuro desejável",
                value=st.session_state.get("tri_ima", ""),
                height=180,
                key="tri_ima_input",
                label_visibility="collapsed",
                placeholder="O que queremos criar? Como seria esse futuro ideal?",
            )
            st.session_state["tri_ima"] = tri_ima

        with tri_col2:
            st.markdown(
                '<div class="tool-icon">🚀</div>'
                '<div class="tool-label">FOGUETE — Impulsos do Presente</div>'
                '<div class="tool-desc">O que no presente já empurra<br>'
                'na direção desse futuro?</div>',
                unsafe_allow_html=True,
            )
            tri_foguete = st.text_area(
                "Descreva os impulsos do presente",
                value=st.session_state.get("tri_foguete", ""),
                height=180,
                key="tri_foguete_input",
                label_visibility="collapsed",
                placeholder="Que forças, movimentos ou tecnologias já existem?",
            )
            st.session_state["tri_foguete"] = tri_foguete

        with tri_col3:
            st.markdown(
                '<div class="tool-icon">⚖️</div>'
                '<div class="tool-label">BALANÇA — Peso do Passado</div>'
                '<div class="tool-desc">O que do passado ainda pesa<br>'
                'e impacta esse cenário?</div>',
                unsafe_allow_html=True,
            )
            tri_balanca = st.text_area(
                "Descreva o peso do passado",
                value=st.session_state.get("tri_balanca", ""),
                height=180,
                key="tri_balanca_input",
                label_visibility="collapsed",
                placeholder="Que heranças históricas, estruturas ou traumas persistem?",
            )
            st.session_state["tri_balanca"] = tri_balanca

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Salvar respostas do Triangle", key="save_triangle"):
            record = build_record()
            save_response(record)
            st.success("Respostas salvas! Avance para o **Future Wheel**.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Future Wheel
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    selected = st.session_state.get("selected_card")
    approach = st.session_state.get("drawn_approach")

    # Banner — Liberdade Guiando o Povo (real image)
    wheel_banner_path = BASE_DIR / "assets" / "future_wheel.png"
    if wheel_banner_path.exists():
        b64_banner = img_to_b64(wheel_banner_path)
        st.markdown(
            f'<img src="data:image/png;base64,{b64_banner}" '
            f'style="width:100%;max-height:260px;object-fit:cover;object-position:top;'
            f'border-radius:12px;margin-bottom:24px;" />',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="width:100%;background:linear-gradient(135deg,#2d1b3d,#6b3578,#c2559c);'
            'border-radius:12px;padding:40px 32px;margin-bottom:28px;text-align:center;">'
            '<p style="color:#f0e0fa;font-size:0.9rem;margin:0;font-style:italic;">'
            '« A liberdade não é dada — ela é conquistada. »'
            '</p></div>',
            unsafe_allow_html=True,
        )

    if not selected:
        st.info("⬅️ Primeiro escolha uma carta na aba **Cenários & Abordagens**.")
    else:
        ctx_col1, ctx_col2 = st.columns([1, 3])
        with ctx_col1:
            b64 = img_to_b64(CARDS_DIR / selected["portrait"])
            st.markdown(
                f'<img src="data:image/jpeg;base64,{b64}" '
                f'style="width:100%;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.15);" />',
                unsafe_allow_html=True,
            )
        with ctx_col2:
            approach_label = approach["text"] if approach else ""
            approach_desc  = approach["desc"]  if approach else ""
            st.markdown(
                f'<div class="section-title">Future Wheel</div>'
                f'<div class="section-subtitle">'
                f'Cenário de <strong>{selected["name"]}</strong>'
                f'{"<br>Abordagem: <em>" + approach_label + "</em> — " + approach_desc if approach else ""}'
                f'</div>',
                unsafe_allow_html=True,
            )
            b64s = img_to_b64(CARDS_DIR / selected["scenario"])
            st.markdown(
                f'<img src="data:image/jpeg;base64,{b64s}" '
                f'style="width:100%;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.12);" />',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            '<p style="text-align:center;color:#7a6589;margin-bottom:24px;">'
            'O Future Wheel explora impactos em ondas — cada consequência gera novas consequências. '
            'Reflita sobre os efeitos em cada ordem.</p>',
            unsafe_allow_html=True,
        )

        wh_col1, wh_col2, wh_col3 = st.columns(3)

        with wh_col1:
            st.markdown(
                '<div class="tool-icon">1️⃣</div>'
                '<div class="tool-label">Impacto de 1ª Ordem</div>'
                '<div class="tool-desc">Os efeitos diretos e imediatos<br>'
                'do cenário. O que muda primeiro?</div>',
                unsafe_allow_html=True,
            )
            wh_primeira = st.text_area(
                "Impacto de 1ª ordem",
                value=st.session_state.get("wh_primeira", ""),
                height=180,
                key="wh_primeira_input",
                label_visibility="collapsed",
                placeholder="Quais são as consequências diretas e imediatas?",
            )
            st.session_state["wh_primeira"] = wh_primeira

        with wh_col2:
            st.markdown(
                '<div class="tool-icon">2️⃣</div>'
                '<div class="tool-label">Impacto de 2ª Ordem</div>'
                '<div class="tool-desc">As consequências das consequências.<br>'
                'O que emerge em seguida?</div>',
                unsafe_allow_html=True,
            )
            wh_segunda = st.text_area(
                "Impacto de 2ª ordem",
                value=st.session_state.get("wh_segunda", ""),
                height=180,
                key="wh_segunda_input",
                label_visibility="collapsed",
                placeholder="Como os impactos de 1ª ordem geram novos efeitos?",
            )
            st.session_state["wh_segunda"] = wh_segunda

        with wh_col3:
            st.markdown(
                '<div class="tool-icon">3️⃣</div>'
                '<div class="tool-label">Impacto de 3ª Ordem</div>'
                '<div class="tool-desc">Transformações profundas e sistêmicas.<br>'
                'O que muda estruturalmente?</div>',
                unsafe_allow_html=True,
            )
            wh_terceira = st.text_area(
                "Impacto de 3ª ordem",
                value=st.session_state.get("wh_terceira", ""),
                height=180,
                key="wh_terceira_input",
                label_visibility="collapsed",
                placeholder="Que transformações estruturais e culturais surgem?",
            )
            st.session_state["wh_terceira"] = wh_terceira

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Salvar respostas do Wheel", key="save_wheel"):
            record = build_record()
            save_response(record)
            st.success("Respostas salvas! Veja o resumo completo na aba **Resumo**.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Resumo
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Resumo da Sessão</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Tudo que você explorou nesta sessão, reunido em um só lugar.</div>',
        unsafe_allow_html=True,
    )

    selected = st.session_state.get("selected_card")
    approach = st.session_state.get("drawn_approach")

    if not selected:
        st.info("⬅️ Você ainda não selecionou uma carta. Comece pela aba **Cenários & Abordagens**.")
    else:
        # Card + scenario
        r1, r2 = st.columns(2)
        with r1:
            st.markdown('<div class="summary-section">', unsafe_allow_html=True)
            st.markdown('<div class="summary-title">🃏 Carta Selecionada</div>', unsafe_allow_html=True)
            b64p = img_to_b64(CARDS_DIR / selected["portrait"])
            b64s = img_to_b64(CARDS_DIR / selected["scenario"])
            pc1, pc2 = st.columns(2)
            with pc1:
                st.markdown(
                    f'<img src="data:image/jpeg;base64,{b64p}" style="width:100%;border-radius:8px;"/>',
                    unsafe_allow_html=True,
                )
            with pc2:
                st.markdown(
                    f'<img src="data:image/jpeg;base64,{b64s}" style="width:100%;border-radius:8px;"/>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<p style="text-align:center;font-weight:700;color:#2d1b3d;margin-top:8px;">{selected["name"]}</p>',
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with r2:
            st.markdown('<div class="summary-section">', unsafe_allow_html=True)
            st.markdown('<div class="summary-title">🎲 Abordagem Sorteada</div>', unsafe_allow_html=True)
            if approach:
                st.markdown(
                    f'<div class="approach-pill">✦ {approach["text"]}<br>'
                    f'<span style="font-size:0.85rem;font-weight:400;opacity:0.88;">{approach["desc"]}</span></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown('<p style="color:#7a6589;">Nenhuma abordagem sorteada ainda.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Triangle
        st.markdown('<div class="summary-section">', unsafe_allow_html=True)
        st.markdown('<div class="summary-title">🔺 Future Triangle</div>', unsafe_allow_html=True)
        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            st.markdown("**🧲 IMA — Futuro Desejável**")
            st.markdown(st.session_state.get("tri_ima") or "_Não preenchido_")
        with tc2:
            st.markdown("**🚀 FOGUETE — Impulsos do Presente**")
            st.markdown(st.session_state.get("tri_foguete") or "_Não preenchido_")
        with tc3:
            st.markdown("**⚖️ BALANÇA — Peso do Passado**")
            st.markdown(st.session_state.get("tri_balanca") or "_Não preenchido_")
        st.markdown('</div>', unsafe_allow_html=True)

        # Wheel
        st.markdown('<div class="summary-section">', unsafe_allow_html=True)
        st.markdown('<div class="summary-title">⚙️ Future Wheel</div>', unsafe_allow_html=True)
        wc1, wc2, wc3 = st.columns(3)
        with wc1:
            st.markdown("**1️⃣ Impacto de 1ª Ordem**")
            st.markdown(st.session_state.get("wh_primeira") or "_Não preenchido_")
        with wc2:
            st.markdown("**2️⃣ Impacto de 2ª Ordem**")
            st.markdown(st.session_state.get("wh_segunda") or "_Não preenchido_")
        with wc3:
            st.markdown("**3️⃣ Impacto de 3ª Ordem**")
            st.markdown(st.session_state.get("wh_terceira") or "_Não preenchido_")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("💾 Salvar resumo final", key="save_final"):
            record = build_record()
            save_response(record)
            st.balloons()
            st.success("Sessão salva com sucesso! Obrigada por jogar. ♀")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Admin
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">🔐 Painel de Admin</div>', unsafe_allow_html=True)

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        pwd = st.text_input("Senha de acesso:", type="password", key="admin_pwd")
        if st.button("Entrar", key="admin_login"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    else:
        responses = load_responses()
        st.success(f"✅ {len(responses)} resposta(s) registrada(s).")

        if st.button("🔓 Sair do Admin"):
            st.session_state.admin_auth = False
            st.rerun()

        if not responses:
            st.info("Nenhuma resposta salva ainda.")
        else:
            import pandas as pd

            # Flatten for display
            rows = []
            for r in responses:
                rows.append({
                    "Sessão": r.get("session_id", ""),
                    "Data/Hora": r.get("timestamp", ""),
                    "Carta": r.get("selected_card", ""),
                    "Abordagem": r.get("approach", ""),
                    "IMA": r.get("triangle", {}).get("ima", ""),
                    "Foguete": r.get("triangle", {}).get("foguete", ""),
                    "Balança": r.get("triangle", {}).get("balanca", ""),
                    "1ª Ordem": r.get("wheel", {}).get("primeira", ""),
                    "2ª Ordem": r.get("wheel", {}).get("segunda", ""),
                    "3ª Ordem": r.get("wheel", {}).get("terceira", ""),
                })

            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)

            # Download
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Baixar como CSV",
                data=csv,
                file_name=f"feminist_futures_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )

            # Detail view
            st.markdown("---")
            st.markdown("**Ver resposta detalhada:**")
            sessions = [r["session_id"] for r in responses]
            chosen = st.selectbox("Selecione uma sessão", sessions)
            detail = next((r for r in responses if r["session_id"] == chosen), None)
            if detail:
                st.json(detail)
