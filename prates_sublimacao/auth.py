"""
auth.py — Autenticação Prates Sublimação
Login, hierarquia de acesso e recuperação de senha.
"""
import bcrypt
import streamlit as st
import secrets
import string
from datetime import datetime, timedelta
from database import get_usuario_por_email, update_usuario, add_token_recuperacao, get_token_recuperacao, deletar_token_recuperacao

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
    usuario = get_usuario_por_email(email.strip().lower())
    if not usuario:
        return None, "E-mail não encontrado."
    if not usuario.get('ativo', False):
        return None, "Usuário desativado. Fale com o administrador."
    if not verificar_senha(senha, usuario['senha_hash']):
        return None, "Senha incorreta."
    return usuario, None

def fazer_logout():
    for key in ['usuario_logado', 'pagina', 'tela']:
        st.session_state.pop(key, None)
    st.rerun()

# ─────────────────────────────────────────
# RECUPERAÇÃO DE SENHA
# ─────────────────────────────────────────
def gerar_codigo():
    return ''.join(secrets.choice(string.digits) for _ in range(6))

def enviar_email_recuperacao(email: str, nome: str, codigo: str) -> bool:
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        smtp_email = st.secrets.get("SMTP_EMAIL", "")
        smtp_senha = st.secrets.get("SMTP_SENHA", "")

        if not smtp_email or not smtp_senha:
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Recuperação de Senha — Prates Sublimação"
        msg["From"]    = smtp_email
        msg["To"]      = email

        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;background:#16191f;padding:32px;border-radius:10px">
          <img src="https://prates-sublimacao.streamlit.app/logo.png" width="80" style="border-radius:8px;display:block;margin:0 auto 20px">
          <h2 style="color:#e2e8f0;text-align:center;margin:0 0 8px">Recuperação de Senha</h2>
          <p style="color:#6b7280;text-align:center;margin:0 0 24px">Olá, <b style="color:#c5cad3">{nome}</b>!</p>
          <p style="color:#6b7280;text-align:center;margin:0 0 16px">Use o código abaixo para redefinir sua senha:</p>
          <div style="background:#111318;border:1px solid #252932;border-radius:8px;padding:20px;text-align:center;margin:0 0 24px">
            <span style="font-size:36px;font-weight:700;color:#2d7a4f;letter-spacing:8px">{codigo}</span>
          </div>
          <p style="color:#6b7280;font-size:12px;text-align:center;margin:0">Este código expira em <b>15 minutos</b>.<br>Se não foi você, ignore este e-mail.</p>
          <hr style="border-color:#252932;margin:20px 0">
          <p style="color:#3a4050;font-size:11px;text-align:center;margin:0">Prates Sublimação · Macaé/RJ</p>
        </div>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(smtp_email, smtp_senha)
            server.sendmail(smtp_email, email, msg.as_string())
        return True
    except Exception as e:
        return False

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

    if 'tela' not in st.session_state:
        st.session_state.tela = 'login'

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

        if _logo:
            st.markdown(
                f'<div style="text-align:center;margin-bottom:20px">'
                f'<img src="data:image/png;base64,{_logo}" width="110" style="border-radius:8px"></div>',
                unsafe_allow_html=True
            )

        # ── TELA LOGIN ──
        if st.session_state.tela == 'login':
            st.markdown("""
            <div style="background:#16191f;border:1px solid #252932;border-radius:10px;padding:32px 28px 8px">
            <p style="color:#e2e8f0;font-size:18px;font-weight:600;margin:0 0 4px">Prates Sublimação</p>
            <p style="color:#6b7280;font-size:13px;margin:0 0 20px">Faça login para continuar</p>
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
                        st.session_state['tela'] = 'login'
                        st.rerun()
                        st.stop()

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("🔑 Esqueci minha senha", use_container_width=True, key="btn_forgot"):
                st.session_state.tela = 'recuperar'
                st.rerun()

        # ── TELA RECUPERAR ──
        elif st.session_state.tela == 'recuperar':
            st.markdown("""
            <div style="background:#16191f;border:1px solid #252932;border-radius:10px;padding:32px 28px 8px">
            <p style="color:#e2e8f0;font-size:18px;font-weight:600;margin:0 0 4px">Recuperar Senha</p>
            <p style="color:#6b7280;font-size:13px;margin:0 0 20px">Informe seu e-mail cadastrado para receber o código.</p>
            """, unsafe_allow_html=True)

            rec_email = st.text_input("E-mail", placeholder="seu@email.com", key="rec_email")

            if st.button("Enviar Código", use_container_width=True, key="btn_enviar_codigo"):
                if not rec_email:
                    st.error("Informe o e-mail.")
                else:
                    usuario = get_usuario_por_email(rec_email.strip().lower())
                    if not usuario:
                        st.error("E-mail não encontrado.")
                    elif not usuario.get('ativo', False):
                        st.error("Usuário inativo. Fale com o administrador.")
                    else:
                        codigo = gerar_codigo()
                        expira = (datetime.now() + timedelta(minutes=15)).isoformat()
                        add_token_recuperacao(rec_email.strip().lower(), codigo, expira)
                        enviado = enviar_email_recuperacao(rec_email.strip().lower(), usuario['nome'], codigo)
                        if enviado:
                            st.session_state['rec_email_temp'] = rec_email.strip().lower()
                            st.session_state.tela = 'codigo'
                            st.rerun()
                        else:
                            st.warning(f"Não foi possível enviar o e-mail. Use o código abaixo diretamente:")
                            st.code(codigo)
                            st.session_state['rec_email_temp'] = rec_email.strip().lower()
                            st.session_state.tela = 'codigo'

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("← Voltar ao login", use_container_width=True, key="btn_volta_login"):
                st.session_state.tela = 'login'
                st.rerun()

        # ── TELA CÓDIGO ──
        elif st.session_state.tela == 'codigo':
            st.markdown("""
            <div style="background:#16191f;border:1px solid #252932;border-radius:10px;padding:32px 28px 8px">
            <p style="color:#e2e8f0;font-size:18px;font-weight:600;margin:0 0 4px">Digite o Código</p>
            <p style="color:#6b7280;font-size:13px;margin:0 0 20px">Informe o código de 6 dígitos enviado ao seu e-mail e a nova senha.</p>
            """, unsafe_allow_html=True)

            cod_input   = st.text_input("Código de 6 dígitos", max_chars=6, key="cod_input")
            nova_senha  = st.text_input("Nova Senha", type="password", key="nova_senha")
            conf_senha  = st.text_input("Confirmar Nova Senha", type="password", key="conf_senha")

            if st.button("Redefinir Senha", use_container_width=True, key="btn_redef"):
                email_temp = st.session_state.get('rec_email_temp', '')
                if not cod_input or not nova_senha or not conf_senha:
                    st.error("Preencha todos os campos.")
                elif nova_senha != conf_senha:
                    st.error("As senhas não conferem.")
                elif len(nova_senha) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres.")
                else:
                    token = get_token_recuperacao(email_temp, cod_input)
                    if not token:
                        st.error("Código inválido ou expirado.")
                    else:
                        expira = datetime.fromisoformat(token['expira_em'])
                        if datetime.now() > expira:
                            deletar_token_recuperacao(email_temp)
                            st.error("Código expirado. Solicite um novo.")
                        else:
                            usuario = get_usuario_por_email(email_temp)
                            update_usuario(usuario['id'], {'senha_hash': hash_senha(nova_senha)})
                            deletar_token_recuperacao(email_temp)
                            st.success("✅ Senha redefinida com sucesso! Faça login.")
                            st.session_state.tela = 'login'
                            st.session_state.pop('rec_email_temp', None)
                            st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("← Voltar ao login", use_container_width=True, key="btn_volta2"):
                st.session_state.tela = 'login'
                st.rerun()

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
