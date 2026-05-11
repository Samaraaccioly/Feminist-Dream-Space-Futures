# ♀ Future Feminist Spaces — Guia de Instalação e Deploy

## O que é esse projeto?

Site interativo do jogo **Future Feminist Spaces**, com:
- 🃏 Cartas de cenários (10 mulheres + cenários futuristas)
- 🔺 Future Triangle (Ima, Foguete, Balança)
- ⚙️ Future Wheel (impactos de 1ª, 2ª e 3ª ordem)
- 📋 Resumo da sessão
- 🔐 Painel admin com senha

---

## Estrutura de Pastas

```
feminist_futures/
├── app.py                  ← código principal
├── requirements.txt        ← dependências Python
├── .streamlit/
│   ├── config.toml         ← tema e configurações
│   └── secrets.toml        ← senha admin 
├── assets/
│   └── cards/              ← imagens das cartas (portraits + scenarios)
├── data/
│   └── responses.json      ← respostas salvas dos usuários
└── README.md
```

---

## Passo a passo: Publicar no Streamlit Cloud (GRATUITO)

### 1. Suba os arquivos

Abra o terminal (ou Git Bash no Windows) na pasta do projeto e rode:

```bash
git init
git add .
git commit -m "primeiro commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/feminist-futures.git
git push -u origin main
```

> ⚠️ O arquivo `.streamlit/secrets.toml` está no `.gitignore` — ele **não** vai para o GitHub. Você vai configurar a senha no próximo passo.

### 2. Crie uma conta no Streamlit Cloud

Acesse https://streamlit.io/cloud e faça login **com a sua conta do GitHub**.

### 3. Publique o app

1. Clique em **New app**
2. Selecione seu repositório `feminist-futures`
3. Branch: `main`
4. Main file path: `app.py`
5. Clique em **Deploy**

### 4. Configure a senha do admin

Ainda no Streamlit Cloud, vá em:
**⚙️ Settings → Secrets** e cole:

```toml
ADMIN_PASSWORD = "sua_senha_aqui"
```

---

## Rodar localmente (no seu computador)

### Pré-requisitos
- Python 3.9+ instalado (https://python.org/downloads)

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Rodar o app

```bash
streamlit run app.py
```

O navegador vai abrir automaticamente em `http://localhost:8501`

---

## Senha do admin

Para alterar:
- **Localmente**: edite `.streamlit/secrets.toml`
- **Streamlit Cloud**: edite em Settings → Secrets

---

## Como os dados são salvos?

As respostas ficam em `data/responses.json`. No painel admin você pode:
- Ver todas as respostas em tabela
- Baixar como planilha `.csv`
- Ver detalhes de cada sessão

> ⚠️ No Streamlit Cloud o arquivo `responses.json` é resetado a cada redeploy.
> Para persistência permanente, considere usar o **Supabase** (gratuito) 
