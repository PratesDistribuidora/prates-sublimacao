"""
auth.py — Autenticação Prates Sublimação
Login + Recuperação de senha por código de 6 dígitos.
"""
import bcrypt
import streamlit as st
import secrets
import string
from datetime import datetime, timedelta
from database import get_usuario_por_email, update_usuario, add_token_recuperacao, get_token_recuperacao, deletar_token_recuperacao

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
    for key in ['usuario_logado', 'pagina', 'login_tela']:
        st.session_state.pop(key, None)
    st.rerun()

def paginas_disponiveis() -> list:
    usuario = st.session_state.get('usuario_logado')
    if not usuario:
        return []
    return PERMISSOES.get(usuario.get('nivel', ''), [])

def _gerar_codigo():
    return ''.join(secrets.choice(string.digits) for _ in range(6))

def _enviar_email(email, nome, codigo):
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
        msg["From"] = smtp_email
        msg["To"] = email
        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:420px;margin:0 auto;background:#16191f;padding:32px;border-radius:10px">
          <h2 style="color:#e2e8f0;text-align:center;margin:0 0 8px">Recuperação de Senha</h2>
          <p style="color:#6b7280;text-align:center;margin:0 0 24px">Olá, <b style="color:#c5cad3">{nome}</b>! Use o código abaixo:</p>
          <div style="background:#111318;border:1px solid #252932;border-radius:8px;padding:20px;text-align:center;margin:0 0 20px">
            <span style="font-size:36px;font-weight:700;color:#2d7a4f;letter-spacing:8px">{codigo}</span>
          </div>
          <p style="color:#6b7280;font-size:12px;text-align:center">Expira em <b>15 minutos</b>. Se não foi você, ignore.</p>
          <hr style="border-color:#252932;margin:20px 0">
          <p style="color:#3a4050;font-size:11px;text-align:center">Prates Sublimação · Macaé/RJ</p>
        </div>"""
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(smtp_email, smtp_senha)
            server.sendmail(smtp_email, email, msg.as_string())
        return True
    except:
        return False

def tela_login(_logo=None):
    if 'login_tela' not in st.session_state:
        st.session_state.login_tela = 'login'

    # CSS global da tela de login
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #111318; }
    [data-testid="stHeader"] { background: transparent; }
    section[data-testid="stSidebar"] { display: none !important; }
    div[data-testid="stForm"] { background: #16191f; border: 1px solid #252932; border-radius: 10px; padding: 24px; }
    .stTextInput input { background: #111318 !important; border: 1px solid #252932 !important; color: #e2e8f0 !important; }
    .stFormSubmitButton button { background: #1e6b3e !important; color: #fff !important; width: 100% !important; }
    .stButton button { background: transparent !important; color: #6b7280 !important; border: 1px solid #252932 !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

        if _logo:
            st.markdown(
                f'<div style="text-align:center;margin-bottom:20px">'
                f'<img src="data:image/png;base64,{_logo}" width="110" style="border-radius:8px"></div>',
                unsafe_allow_html=True
            )

        tela = st.session_state.login_tela

        # ─── TELA LOGIN ───────────────────────────────
        if tela == 'login':
            with st.form("form_login"):
                st.markdown('<p style="color:#e2e8f0;font-size:15px;font-weight:600;margin:0 0 2px">Prates Sublimação</p>', unsafe_allow_html=True)
                st.markdown('<p style="color:#6b7280;font-size:12px;margin:0 0 16px">Faça login para continuar</p>', unsafe_allow_html=True)
                email = st.text_input("E-mail", placeholder="seu@email.com")
                senha = st.text_input("Senha", type="password", placeholder="••••••••")
                entrar = st.form_submit_button("Entrar", use_container_width=True)

            if entrar:
                if not email or not senha:
                    st.error("Preencha e-mail e senha.")
                else:
                    u = get_usuario_por_email(email.strip().lower())
                    if not u:
                        st.error("E-mail não encontrado.")
                    elif not u.get('ativo', False):
                        st.error("Usuário inativo. Fale com o administrador.")
                    elif not verificar_senha(senha, u['senha_hash']):
                        st.error("Senha incorreta.")
                    else:
                        st.session_state['usuario_logado'] = u
                        st.rerun()

            if st.button("🔑 Esqueci minha senha", use_container_width=True, key="btn_forgot"):
                st.session_state.login_tela = 'recuperar'
                st.rerun()

        # ─── TELA RECUPERAR ───────────────────────────
        elif tela == 'recuperar':
            with st.form("form_recuperar"):
                st.markdown('<p style="color:#e2e8f0;font-size:15px;font-weight:600;margin:0 0 2px">Recuperar Senha</p>', unsafe_allow_html=True)
                st.markdown('<p style="color:#6b7280;font-size:12px;margin:0 0 16px">Informe seu e-mail para receber o código.</p>', unsafe_allow_html=True)
                rec_email = st.text_input("E-mail", placeholder="seu@email.com")
                enviar = st.form_submit_button("Enviar Código", use_container_width=True)

            if enviar:
                if not rec_email:
                    st.error("Informe o e-mail.")
                else:
                    u = get_usuario_por_email(rec_email.strip().lower())
                    if not u:
                        st.error("E-mail não encontrado.")
                    elif not u.get('ativo', False):
                        st.error("Usuário inativo. Fale com o administrador.")
                    else:
                        codigo = _gerar_codigo()
                        expira = (datetime.now() + timedelta(minutes=15)).isoformat()
                        add_token_recuperacao(rec_email.strip().lower(), codigo, expira)
                        enviado = _enviar_email(rec_email.strip().lower(), u['nome'], codigo)
                        st.session_state['rec_email'] = rec_email.strip().lower()
                        st.session_state.login_tela = 'codigo'
                        if not enviado:
                            st.session_state['codigo_debug'] = codigo
                        st.rerun()

            if st.button("← Voltar", use_container_width=True, key="btn_volta_rec"):
                st.session_state.login_tela = 'login'
                st.rerun()

        # ─── TELA CÓDIGO ──────────────────────────────
        elif tela == 'codigo':
            # Mostra código na tela se SMTP não configurado
            if 'codigo_debug' in st.session_state:
                st.info(f"SMTP não configurado. Use o código: **{st.session_state['codigo_debug']}**")

            with st.form("form_codigo"):
                st.markdown('<p style="color:#e2e8f0;font-size:15px;font-weight:600;margin:0 0 2px">Digite o Código</p>', unsafe_allow_html=True)
                st.markdown('<p style="color:#6b7280;font-size:12px;margin:0 0 16px">Código enviado ao seu e-mail. Expira em 15 min.</p>', unsafe_allow_html=True)
                codigo_inp = st.text_input("Código de 6 dígitos", max_chars=6, placeholder="000000")
                nova_senha = st.text_input("Nova Senha", type="password", placeholder="••••••••")
                conf_senha = st.text_input("Confirmar Senha", type="password", placeholder="••••••••")
                redefinir = st.form_submit_button("Redefinir Senha", use_container_width=True)

            if redefinir:
                email_temp = st.session_state.get('rec_email', '')
                if not codigo_inp or not nova_senha or not conf_senha:
                    st.error("Preencha todos os campos.")
                elif nova_senha != conf_senha:
                    st.error("As senhas não conferem.")
                elif len(nova_senha) < 6:
                    st.error("Mínimo 6 caracteres.")
                else:
                    token = get_token_recuperacao(email_temp, codigo_inp)
                    if not token:
                        st.error("Código inválido ou expirado.")
                    elif datetime.now() > datetime.fromisoformat(token['expira_em']):
                        deletar_token_recuperacao(email_temp)
                        st.error("Código expirado. Solicite um novo.")
                    else:
                        u = get_usuario_por_email(email_temp)
                        update_usuario(u['id'], {'senha_hash': hash_senha(nova_senha)})
                        deletar_token_recuperacao(email_temp)
                        st.session_state.pop('rec_email', None)
                        st.session_state.pop('codigo_debug', None)
                        st.session_state.login_tela = 'login'
                        st.success("✅ Senha redefinida! Faça login.")
                        st.rerun()

            if st.button("← Voltar", use_container_width=True, key="btn_volta_cod"):
                st.session_state.login_tela = 'login'
                st.rerun()

        st.markdown('<p style="text-align:center;color:#3a4050;font-size:11px;margin-top:12px">Prates Sublimação · Macaé/RJ · v6.0</p>', unsafe_allow_html=True)
