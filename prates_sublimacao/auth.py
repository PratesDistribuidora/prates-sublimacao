"""
auth.py — Autenticação Prates Sublimação
Login simples com email + senha.
"""
import bcrypt
import streamlit as st
from database import get_usuario_por_email

PERMISSOES = {
    'admin': [
        "📊 Dashboard", "🧮 Simulador de Preço", "🔄 Margem Reversa",
        "📦 Simulador de Lote", "📤 Tabela para Cliente", "📈 Relatório Mensal",
        "⚙️ Configurações", "📋 Histórico de Preços", "📥 Importar Planilha", "👥 Usuários",
    ],
    'gerente': [
        "📊 Dashboard", "🧮 Simulador de Preço", "🔄 Margem Reversa",
        "📦 Simulador de Lote", "📤 Tabela para Cliente", "📈 Relatório Mensal",
        "📋 Histórico de Preços", "📥 Importar Planilha",
    ],
    'vendedor': ["📤 Tabela para Cliente"],
    'operador': ["🧮 Simulador de Preço", "📦 Simulador de Lote", "📈 Relatório Mensal"],
}

def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt(12)).decode()

def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_armazenado.encode())
    except:
        return False

def fazer_logout():
    for key in ['usuario_logado', 'pagina']:
        st.session_state.pop(key, None)
    st.rerun()

def paginas_disponiveis() -> list:
    usuario = st.session_state.get('usuario_logado')
    if not usuario:
        return []
    return PERMISSOES.get(usuario.get('nivel', ''), [])

def tela_login(_logo=None):
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    [data-testid="stAppViewContainer"] { background: #111318; }
    [data-testid="stHeader"] { background: transparent; }
    section[data-testid="stSidebar"] { display: none !important; }
    .stButton > button { background: #1e6b3e !important; color: #fff !important; }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        if _logo:
            st.markdown(
                f'<div style="text-align:center;margin-bottom:24px">'
                f'<img src="data:image/png;base64,{_logo}" width="120" style="border-radius:8px"></div>',
                unsafe_allow_html=True
            )
        with st.form("form_login", clear_on_submit=False):
            st.markdown('<p style="color:#e2e8f0;font-size:16px;font-weight:600;margin:0 0 4px">Prates Sublimação</p>', unsafe_allow_html=True)
            st.markdown('<p style="color:#6b7280;font-size:12px;margin:0 0 16px">Faça login para continuar</p>', unsafe_allow_html=True)
            email = st.text_input("E-mail", placeholder="seu@email.com")
            senha = st.text_input("Senha", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Entrar", use_container_width=True)

        if submitted:
            if not email or not senha:
                st.error("Preencha e-mail e senha.")
            else:
                usuario = get_usuario_por_email(email.strip().lower())
                if not usuario:
                    st.error("E-mail não encontrado.")
                elif not usuario.get('ativo', False):
                    st.error("Usuário desativado. Fale com o administrador.")
                elif not verificar_senha(senha, usuario['senha_hash']):
                    st.error("Senha incorreta.")
                else:
                    st.session_state['usuario_logado'] = usuario
                    st.rerun()

        st.markdown('<p style="text-align:center;color:#3a4050;font-size:11px;margin-top:16px">Prates Sublimação · Macaé/RJ · v6.0</p>', unsafe_allow_html=True)
