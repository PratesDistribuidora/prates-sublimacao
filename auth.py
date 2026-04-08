"""
auth.py — Autenticação Prates Sublimação
Login com email + senha, hash bcrypt, níveis de acesso.
"""
import bcrypt
import streamlit as st
from database import get_usuario_por_email, update_usuario

# ─────────────────────────────────────────
# PERMISSÕES POR NÍVEL
# ─────────────────────────────────────────
PERMISSOES = {
    'admin': [
        "📊 Dashboard",
        "🧮 Simulador de Preço",
        "🔄 Margem Reversa",
        "📦 Simulador de Lote",
        "📤 Tabela para Cliente",
        "📈 Relatório Mensal",
        "⚙️ Configurações",
        "📋 Histórico de Preços",
        "📥 Importar Planilha",
        "👥 Usuários",
    ],
    'gerente': [
        "📊 Dashboard",
        "🧮 Simulador de Preço",
        "🔄 Margem Reversa",
        "📦 Simulador de Lote",
        "📤 Tabela para Cliente",
        "📈 Relatório Mensal",
        "📋 Histórico de Preços",
        "📥 Importar Planilha",
    ],
    'vendedor': [
        "📤 Tabela para Cliente",
    ],
    'operador': [
        "🧮 Simulador de Preço",
        "📦 Simulador de Lote",
        "📈 Relatório Mensal",
    ],
}

# ─────────────────────────────────────────
# HASH DE SENHA
# ─────────────────────────────────────────
def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt(12)).decode()

def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_armazenado.encode())
    except:
        return False

# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────
def fazer_login(email: str, senha: str):
    """Retorna o usuário se login válido, None se inválido."""
    usuario = get_usuario_por_email(email.strip().lower())
    if not usuario:
        return None, "E-mail não encontrado."
    if not usuario.get('ativo', False):
        return None, "Usuário desativado. Fale com o administrador."
    if not verificar_senha(senha, usuario['senha_hash']):
        return None, "Senha incorreta."
    return usuario, None

def fazer_logout():
    for key in ['usuario_logado', 'pagina']:
        st.session_state.pop(key, None)
    st.rerun()

# ─────────────────────────────────────────
# TELA DE LOGIN
# ─────────────────────────────────────────
def tela_login(_logo=None):
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #111318; }
    [data-testid="stHeader"] { background: transparent; }
    </style>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        if _logo:
            st.markdown(
                f'<div style="text-align:center;margin-bottom:24px">'
                f'<img src="data:image/png;base64,{_logo}" width="120" style="border-radius:8px"></div>',
                unsafe_allow_html=True
            )
        st.markdown("""
        <div style="background:#16191f;border:1px solid #252932;border-radius:10px;padding:32px 28px 24px">
        <p style="color:#e2e8f0;font-size:18px;font-weight:600;margin:0 0 4px">Prates Sublimação</p>
        <p style="color:#6b7280;font-size:13px;margin:0 0 24px">Faça login para continuar</p>
        """, unsafe_allow_html=True)

        email = st.text_input("E-mail", placeholder="seu@email.com", key="login_email")
        senha = st.text_input("Senha", type="password", placeholder="••••••••", key="login_senha")

        if st.button("Entrar", use_container_width=True, key="btn_login"):
            if not email or not senha:
                st.error("Preencha e-mail e senha.")
            else:
                usuario, erro = fazer_login(email, senha)
                if erro:
                    st.error(erro)
                else:
                    st.session_state['usuario_logado'] = usuario
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align:center;color:#3a4050;font-size:11px;margin-top:16px">Prates Sublimação · Macaé/RJ · v6.0</p>',
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────
# VERIFICAÇÃO DE ACESSO
# ─────────────────────────────────────────
def tem_acesso(pagina: str) -> bool:
    usuario = st.session_state.get('usuario_logado')
    if not usuario:
        return False
    nivel = usuario.get('nivel', '')
    return pagina in PERMISSOES.get(nivel, [])

def paginas_disponiveis() -> list:
    usuario = st.session_state.get('usuario_logado')
    if not usuario:
        return []
    nivel = usuario.get('nivel', '')
    return PERMISSOES.get(nivel, [])
