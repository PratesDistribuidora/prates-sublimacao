"""
app.py — Sistema Prates Sublimação v6
Com login, hierarquia de usuários e Supabase.
"""
import streamlit as st
import pandas as pd
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go
import base64, os

from database import (
    get_parametros, set_parametro,
    get_fornecedores, update_fornecedor, get_preco_kg, add_fornecedor,
    get_faccionistas, update_faccionista, get_preco_costura,
    get_skus, upsert_sku, delete_sku, update_sku_campo,
    get_relatorio_mensal, add_registro_mensal, delete_registro_mensal,
    get_historico, add_historico,
    get_usuarios, add_usuario, update_usuario, delete_usuario,
)
from calculadora import (
    calcular_sku_completo, calcular_manual, calcular_lote,
    gerar_tabela_catalogo, resumo_dashboard,
)
from auth import tela_login, fazer_logout, paginas_disponiveis, hash_senha

st.set_page_config(
    page_title="Prates Sublimação",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data(show_spinner=False)
def get_logo():
    # Tenta na subpasta primeiro, depois na raiz
    for path in ["prates_sublimacao/logo.png", "logo.png"]:
        if os.path.exists(path):
            with open(path,"rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

_LOGO = get_logo()

# ══ ROTEADOR PRINCIPAL ════════════════════════════
if 'usuario_logado' not in st.session_state:
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    [data-testid="stAppViewContainer"] { background: #111318; }
    [data-testid="stHeader"] { background: transparent; }
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="stAppViewContainer"] > section.main > div { padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)
    placeholder = st.empty()
    with placeholder.container():
        tela_login(_LOGO)
    st.stop()

st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
[data-testid="stAppViewContainer"] { background: #111318; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #16191f; border-right: 1px solid #252932; }
[data-testid="stSidebar"] * { color: #c5cad3 !important; }
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background: transparent !important; border: none !important;
    border-left: 3px solid transparent !important; border-radius: 0 5px 5px 0 !important;
    color: #8892a0 !important; font-size: 13px !important; font-weight: 400 !important;
    padding: 7px 14px !important; text-align: left !important; margin: 1px 0 !important;
    box-shadow: none !important; transition: all 0.15s !important;
    width: 100% !important; display: block !important;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
    background: #1a2235 !important; color: #c5cad3 !important;
    border-left: 3px solid #2d7a4f44 !important;
}
[data-testid="stSidebar"] .stButton > button div,
[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] div,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p {
    text-align: left !important; margin: 0 !important; width: 100% !important; display: block !important;
}
.stButton > button { background: #1e6b3e; color: #fff; border: none; border-radius: 5px; padding: 6px 16px; font-size: 13px; font-weight: 500; }
.stButton > button:hover { background: #248a4e; }
[data-testid="stDownloadButton"] > button { background: #1a2540; color: #7eb8f7; border: 1px solid #253560; border-radius: 5px; font-size: 13px; }
[data-testid="stDownloadButton"] > button:hover { background: #1e2d50; }
[data-testid="stMetric"] { background: #16191f; border-radius: 6px; padding: 12px 14px; border: 1px solid #252932; }
[data-testid="stMetricLabel"] { color: #6b7280 !important; font-size: 11px !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 20px !important; font-weight: 600 !important; }
[data-testid="stTabs"] [role="tablist"] { background: transparent; border-bottom: 1px solid #252932; gap: 0; }
[data-testid="stTabs"] [role="tab"] { color: #6b7280 !important; font-size: 13px !important; padding: 8px 16px !important; border-radius: 0 !important; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { color: #e2e8f0 !important; border-bottom: 2px solid #2d7a4f !important; font-weight: 600 !important; }
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input { background: #16191f !important; border: 1px solid #252932 !important; border-radius: 5px !important; color: #e2e8f0 !important; font-size: 13px !important; }
[data-testid="stSelectbox"] > div > div { background: #16191f !important; border: 1px solid #252932 !important; border-radius: 5px !important; font-size: 13px !important; }
[data-testid="stExpander"] { background: #16191f !important; border: 1px solid #252932 !important; border-radius: 6px !important; margin-bottom: 6px !important; }
[data-testid="stDataFrame"] { border-radius: 6px; border: 1px solid #252932; font-size: 13px; }
[data-testid="stInfo"] { background: #0d1e35 !important; border: 1px solid #1a3a5c !important; border-radius: 6px !important; font-size: 13px !important; color: #7eb8f7 !important; }
[data-testid="stSuccess"] { background: #0a1f12 !important; border: 1px solid #1a4a2a !important; border-radius: 6px !important; font-size: 13px !important; }
[data-testid="stWarning"] { background: #1f1a0a !important; border: 1px solid #3a2a0a !important; border-radius: 6px !important; font-size: 13px !important; }
[data-testid="stError"] { background: #1f0a0a !important; border: 1px solid #3a1a1a !important; border-radius: 6px !important; font-size: 13px !important; }
.kpi-card { background: #16191f; border: 1px solid #252932; border-radius: 6px; padding: 14px 16px; text-align: center; }
.kpi-card .label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; margin: 0; }
.kpi-card .value { font-size: 20px; font-weight: 600; color: #e2e8f0; margin: 4px 0 0 0; }
.kpi-card.verde .value { color: #4ade80; }
.kpi-card.vermelho .value { color: #f87171; }
.page-title { font-size: 18px; font-weight: 600; color: #e2e8f0; padding-bottom: 10px; border-bottom: 1px solid #252932; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
.section-label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.8px; margin: 16px 0 8px 0; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #111318; }
::-webkit-scrollbar-thumb { background: #252932; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

usuario = st.session_state['usuario_logado']
nivel = usuario.get('nivel', '')
paginas = paginas_disponiveis()

# Sidebar
with st.sidebar:
    if _LOGO:
        st.markdown(
            f'<div style="text-align:center;padding:16px 8px 8px">'
            f'<img src="data:image/png;base64,{_LOGO}" width="130" style="border-radius:6px"></div>',
            unsafe_allow_html=True
        )
    st.markdown(
        f'<p style="text-align:center;color:#6b7280;font-size:12px;margin:4px 0 8px">'
        f'👤 {usuario["nome"]} <span style="color:#2d7a4f;font-size:10px">({nivel})</span></p>',
        unsafe_allow_html=True
    )
    st.markdown('<hr style="border-color:#252932;margin:4px 0 10px">', unsafe_allow_html=True)

    if 'pagina' not in st.session_state or st.session_state.pagina not in paginas:
        st.session_state.pagina = paginas[0] if paginas else ""

    for item in paginas:
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.pagina = item
            st.rerun()

    pagina = st.session_state.pagina
    st.markdown('<hr style="border-color:#252932;margin:10px 0 8px">', unsafe_allow_html=True)
    if st.button("🚪 Sair", use_container_width=True, key="btn_sair"):
        fazer_logout()
    st.markdown('<p style="text-align:center;color:#3a4050;font-size:11px;margin:8px 0 0">Prates Sublimação · Macaé/RJ · v6.0</p>', unsafe_allow_html=True)

# Helpers
def fmt(v):
    if v is None: return "—"
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
def fpct(v): return f"{v*100:.1f}%"
def kpi(label, valor, cor=""):
    return f'<div class="kpi-card {cor}"><p class="label">{label}</p><p class="value">{fmt(valor)}</p></div>'
def kpi_txt(label, valor, cor=""):
    return f'<div class="kpi-card {cor}"><p class="label">{label}</p><p class="value">{valor}</p></div>'
def titulo(icon, texto):
    logo_html = f'<img src="data:image/png;base64,{_LOGO}" height="32" style="border-radius:4px">' if _LOGO else icon
    st.markdown(f'<div class="page-title">{logo_html} {texto}</div>', unsafe_allow_html=True)
def sec(t):
    st.markdown(f'<p class="section-label">{t}</p>', unsafe_allow_html=True)

@st.cache_data(ttl=60, show_spinner=False)
def catalogo_cache():
    return gerar_tabela_catalogo()

def get_opcoes():
    s = get_skus()
    return s, sorted(set(x['modelo'] for x in s)), sorted(set(x['tecido'] for x in s))

def cores(s,m,t):
    return sorted(set(x['cor'] for x in s if x['modelo']==m and x['tecido']==t))

def tams(s,m,t,c):
    return sorted(set(x['tamanho'] for x in s if x['modelo']==m and x['tecido']==t and x['cor']==c))

CHART = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#6b7280', size=11), height=220,
    margin=dict(l=10,r=10,t=30,b=10),
)

# ══ DASHBOARD ══════════════════════════════════
if pagina == "📊 Dashboard":
    titulo("📊", "Dashboard")
    kpis = resumo_dashboard()
    if not kpis:
        st.warning("Nenhum SKU cadastrado.")
    else:
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.metric("Total SKUs",        kpis['total_skus'])
        c2.metric("Menor Custo",       fmt(kpis['menor_custo']))
        c3.metric("Maior Custo",       fmt(kpis['maior_custo']))
        c4.metric("Menor SR",          fmt(kpis['menor_sr']))
        c5.metric("Maior SR",          fmt(kpis['maior_sr']))
        c6.metric("Margem SR Média",   fmt(kpis['margem_sr_media']))
        st.markdown('<hr style="border-color:#252932;margin:16px 0">', unsafe_allow_html=True)
        df = pd.DataFrame(catalogo_cache())
        col1, col2 = st.columns(2)
        with col1:
            sec("Custo Médio × Super Revenda por Modelo")
            dm = df.groupby('Modelo').agg(Custo=('Custo Final','mean'),SR=('Super Revenda','mean')).reset_index().round(2)
            fig = go.Figure()
            fig.add_bar(x=dm['Modelo'], y=dm['Custo'], name='Custo', marker_color='#475569')
            fig.add_bar(x=dm['Modelo'], y=dm['SR'], name='Super Revenda', marker_color='#2d7a4f')
            fig.update_layout(barmode='group', **CHART, legend=dict(orientation='h', y=1.1, font=dict(size=10, color='#6b7280')))
            fig.update_xaxes(gridcolor='#1e2330', tickfont=dict(size=10))
            fig.update_yaxes(gridcolor='#1e2330', tickfont=dict(size=10))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            sec("Margem SR por Tecido")
            dt = df.groupby('Tecido').agg(C=('Custo Final','mean'), S=('Super Revenda','mean')).reset_index()
            dt['Margem'] = (dt['S'] - dt['C']).round(2)
            fig2 = px.bar(dt, x='Tecido', y='Margem', color='Tecido', color_discrete_sequence=['#2d7a4f','#2563eb','#d97706','#7c3aed'])
            fig2.update_layout(**CHART, showlegend=False)
            fig2.update_xaxes(gridcolor='#1e2330', tickfont=dict(size=10))
            fig2.update_yaxes(gridcolor='#1e2330', tickfont=dict(size=10))
            fig2.update_traces(marker_line_width=0)
            st.plotly_chart(fig2, use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            sec("Distribuição de SKUs por Tecido")
            dp = df.groupby('Tecido').size().reset_index(name='SKUs')
            fig3 = px.pie(dp, names='Tecido', values='SKUs', hole=0.5, color_discrete_sequence=['#2d7a4f','#2563eb','#d97706','#7c3aed'])
            fig3.update_layout(**CHART)
            fig3.update_traces(textfont=dict(size=10))
            st.plotly_chart(fig3, use_container_width=True)
        with col4:
            sec("Top 10 SKUs Mais Caros")
            st.dataframe(df.nlargest(10,'Custo Final')[['Modelo','Tecido','Cor','Tamanho','Custo Final']].reset_index(drop=True), use_container_width=True, hide_index=True)
        st.markdown('<hr style="border-color:#252932;margin:16px 0">', unsafe_allow_html=True)
        sec("Costura Ativa por Modelo")
        st.dataframe(pd.DataFrame([{'Modelo': f['modelo'], 'Faccionista Ativa': f['faccionista_ativa'], 'Preço Ativo': fmt(get_preco_costura(f['modelo']))} for f in get_faccionistas()]), use_container_width=True, hide_index=True)

# ══ SIMULADOR ══════════════════════════════════
elif pagina == "🧮 Simulador de Preço":
    titulo("🧮", "Simulador de Preço")
    ta, tb = st.tabs(["Produto do Catálogo", "Produto Avulso"])
    with ta:
        st.info("Selecione o produto e veja o custo + preços calculados automaticamente.")
        skus, mods, _ = get_opcoes()
        c1, c2 = st.columns(2)
        with c1:
            ma  = st.selectbox("Modelo", mods, key="sa_m")
            ts  = sorted(set(s['tecido'] for s in skus if s['modelo']==ma))
            ta_ = st.selectbox("Tecido", ts, key="sa_t")
        with c2:
            cr  = cores(skus, ma, ta_)
            ca_ = st.selectbox("Cor", cr, key="sa_c") if cr else None
            tm  = tams(skus, ma, ta_, ca_) if ca_ else []
            tm_ = st.selectbox("Tamanho", tm, key="sa_tam") if tm else None
        if ca_ and tm_:
            calc = calcular_sku_completo(ma, ta_, ca_, tm_)
            if calc:
                st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
                sec("Detalhamento do Custo")
                c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
                c1.metric("Peso", f"{calc['peso_g']}g"); c2.metric("R$/kg", fmt(calc['preco_kg']))
                c3.metric("Tecido", fmt(calc['custo_tecido'])); c4.metric("Costura", fmt(calc['costura']))
                c5.metric("Frete 5%", fmt(calc['frete'])); c6.metric("Outros 3%", fmt(calc['outros'])); c7.metric("Embalagem", fmt(calc['embalagem']))
                st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
                sec("Preços de Venda")
                p1,p2,p3,p4,p5 = st.columns(5)
                p1.markdown(kpi("Subtotal", calc['subtotal']), unsafe_allow_html=True)
                p2.markdown(kpi("Custo Final", calc['custo_final']), unsafe_allow_html=True)
                p3.markdown(kpi("Super Revenda", calc['super_revenda'], "verde"), unsafe_allow_html=True)
                p4.markdown(kpi("Atacado +35%", calc['atacado'], "verde"), unsafe_allow_html=True)
                p5.markdown(kpi("Varejo +50%", calc['varejo'], "verde"), unsafe_allow_html=True)
                st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
                if st.button("📄 Gerar Ficha de Custo PDF"):
                    from pdf_gerador import gerar_pdf_ficha_custo
                    pdf = gerar_pdf_ficha_custo(calc)
                    st.download_button("⬇️ Baixar PDF", pdf, file_name=f"ficha_{ma}_{ta_}_{ca_}_{tm_}.pdf".replace(" ","_"), mime="application/pdf")
    with tb:
        st.info("Para produtos não cadastrados — informe os dados manualmente.")
        c1, c2 = st.columns(2)
        with c1:
            desc = st.text_input("Descrição", "Ex: Blusa Polo")
            peso = st.number_input("Peso (g)", 1.0, value=200.0, step=5.0)
            pkg  = st.number_input("Valor/kg (R$)", 0.0, value=28.0, step=0.5)
        with c2:
            p    = get_parametros()
            cost = st.number_input("Costura (R$/peça)", 0.0, value=4.0, step=0.5)
            out  = st.number_input("Outros (%)", 0.0, 1.0, float(p.get('outros_pct',0.03)), 0.01, format="%.2f")
            emb  = st.number_input("Embalagem (R$)", 0.0, value=float(p.get('embalagem',0.0)), step=0.5)
        if st.button("Calcular", key="calc_b"):
            cb = calcular_manual(peso, pkg, cost, emb, out)
            st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
            sec(f"Resultado — {desc}")
            p1,p2,p3,p4 = st.columns(4)
            p1.markdown(kpi("Custo Final", cb['custo_final']), unsafe_allow_html=True)
            p2.markdown(kpi("Super Revenda", cb['super_revenda'], "verde"), unsafe_allow_html=True)
            p3.markdown(kpi("Atacado +35%", cb['atacado'], "verde"), unsafe_allow_html=True)
            p4.markdown(kpi("Varejo +50%", cb['varejo'], "verde"), unsafe_allow_html=True)

# ══ MARGEM REVERSA ══════════════════════════════
elif pagina == "🔄 Margem Reversa":
    titulo("🔄", "Margem Reversa")
    t1, t2 = st.tabs(["Qual minha margem se cobrar R$X?", "Quanto cobrar para ter X% de margem?"])
    skus, mods, _ = get_opcoes()
    with t1:
        st.info("Informe o preço que o cliente quer pagar e veja sua margem real.")
        c1, c2 = st.columns(2)
        with c1:
            m1  = st.selectbox("Modelo", mods, key="mr_m")
            ts1 = sorted(set(s['tecido'] for s in skus if s['modelo']==m1))
            t1_ = st.selectbox("Tecido", ts1, key="mr_t")
        with c2:
            cr1  = cores(skus, m1, t1_)
            c1_  = st.selectbox("Cor", cr1, key="mr_c") if cr1 else None
            tm1  = tams(skus, m1, t1_, c1_) if c1_ else []
            tm1_ = st.selectbox("Tamanho", tm1, key="mr_tam") if tm1 else None
        preco_cli = st.number_input("Preço que o cliente quer pagar (R$)", 0.01, value=12.0, step=0.5)
        if c1_ and tm1_:
            calc = calcular_sku_completo(m1, t1_, c1_, tm1_)
            if calc:
                custo  = calc['custo_final']
                lucro  = round(preco_cli - custo, 2)
                margem = round(lucro / preco_cli * 100, 1) if preco_cli else 0
                markup = round(lucro / custo * 100, 1) if custo else 0
                st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
                p1,p2,p3,p4 = st.columns(4)
                p1.markdown(kpi("Custo Final", custo), unsafe_allow_html=True)
                p2.markdown(kpi("Preço Cobrado", preco_cli), unsafe_allow_html=True)
                if lucro >= 0:
                    p3.markdown(kpi("Lucro / Peça", lucro, "verde"), unsafe_allow_html=True)
                else:
                    p3.markdown(kpi("⚠️ Prejuízo", lucro, "vermelho"), unsafe_allow_html=True)
                p4.metric("Margem Real", f"{margem:.1f}%", delta=f"Markup: {markup:.1f}%")
                st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
                sec("Comparação com suas faixas padrão")
                dc = {'Faixa': ['Super Revenda +20%','Atacado +35%','Varejo +50%','Preço do cliente'],
                      'Preço': [calc['super_revenda'], calc['atacado'], calc['varejo'], preco_cli],
                      'Lucro': [round(calc['super_revenda']-custo,2), round(calc['atacado']-custo,2), round(calc['varejo']-custo,2), lucro],
                      'Margem %': [round((calc['super_revenda']-custo)/calc['super_revenda']*100,1), round((calc['atacado']-custo)/calc['atacado']*100,1), round((calc['varejo']-custo)/calc['varejo']*100,1), margem]}
                st.dataframe(pd.DataFrame(dc), use_container_width=True, hide_index=True)
                if lucro < 0: st.error(f"Abaixo do custo! Mínimo sem prejuízo: {fmt(custo)}")
                elif margem < 10: st.warning(f"Margem muito baixa ({margem:.1f}%). Sua faixa SR padrão é 20%.")
                else: st.success(f"Margem de {margem:.1f}% — dentro do esperado.")
    with t2:
        st.info("Arraste o slider e veja qual preço cobrar para atingir a margem desejada.")
        c1, c2 = st.columns(2)
        with c1:
            m2  = st.selectbox("Modelo", mods, key="mr2_m")
            ts2 = sorted(set(s['tecido'] for s in skus if s['modelo']==m2))
            t2_ = st.selectbox("Tecido", ts2, key="mr2_t")
        with c2:
            cr2  = cores(skus, m2, t2_)
            c2_  = st.selectbox("Cor", cr2, key="mr2_c") if cr2 else None
            tm2  = tams(skus, m2, t2_, c2_) if c2_ else []
            tm2_ = st.selectbox("Tamanho", tm2, key="mr2_tam") if tm2 else None
        mg_des = st.slider("Margem desejada (%)", 5, 100, 20, 1)
        if c2_ and tm2_:
            calc2 = calcular_sku_completo(m2, t2_, c2_, tm2_)
            if calc2:
                custo2 = calc2['custo_final']
                pnec   = round(custo2 / (1 - mg_des/100), 2)
                luc2   = round(pnec - custo2, 2)
                st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
                p1,p2,p3,p4 = st.columns(4)
                p1.markdown(kpi("Custo Final", custo2), unsafe_allow_html=True)
                p2.markdown(kpi(f"Preço p/ {mg_des}%", pnec, "verde"), unsafe_allow_html=True)
                p3.markdown(kpi("Lucro / Peça", luc2, "verde"), unsafe_allow_html=True)
                p4.metric("Markup equivalente", f"{round(luc2/custo2*100,1):.1f}%")
                margens = list(range(5, 65, 5))
                precos  = [round(custo2/(1-m_/100), 2) for m_ in margens]
                fig = px.line(pd.DataFrame({'Margem (%)': margens, 'Preço (R$)': precos}), x='Margem (%)', y='Preço (R$)', markers=True, color_discrete_sequence=['#2d7a4f'])
                fig.add_vline(x=mg_des, line_dash="dash", line_color="#d97706", annotation_text=f"  {mg_des}%", annotation_font_color="#d97706")
                fig.update_layout(**CHART)
                fig.update_xaxes(gridcolor='#1e2330'); fig.update_yaxes(gridcolor='#1e2330')
                st.plotly_chart(fig, use_container_width=True)

# ══ LOTE ═══════════════════════════════════════
elif pagina == "📦 Simulador de Lote":
    titulo("📦", "Simulador de Lote — Kg → Peças")
    st.info("Informe quantos kg vai comprar e veja quantas peças saem, o custo e o lucro.")
    skus, mods, _ = get_opcoes()
    if not skus:
        st.warning("Nenhum SKU cadastrado.")
    else:
        if 'll' not in st.session_state: st.session_state.ll = [{}]
        st.button("+ Adicionar linha", on_click=lambda: st.session_state.ll.append({}))
        inputs = []
        for idx in range(len(st.session_state.ll)):
            c1,c2,c3,c4,c5,c6 = st.columns([2,2,2,2,2,1])
            tec = c1.selectbox("Tecido", sorted(set(s['tecido'] for s in skus)), key=f"lt_t{idx}")
            mod = c2.selectbox("Modelo", sorted(set(s['modelo'] for s in skus if s['tecido']==tec)), key=f"lt_m{idx}")
            cr  = cores(skus, mod, tec)
            co  = c3.selectbox("Cor", cr, key=f"lt_c{idx}") if cr else None
            tm  = tams(skus, mod, tec, co) if co else []
            ta__= c4.selectbox("Tamanho", tm, key=f"lt_ta{idx}") if tm else None
            kg  = c5.number_input("Kg", 0.1, value=10.0, step=0.5, key=f"lt_k{idx}")
            if c6.button("✕", key=f"lt_r{idx}"): st.session_state.ll.pop(idx); st.rerun()
            if tec and mod and co and ta__: inputs.append((tec, co, mod, ta__, kg))
        if st.button("Calcular Lote") and inputs:
            res = []
            for tec,co,mod,ta__,kg in inputs:
                r = calcular_lote(tec, co, mod, ta__, kg)
                if r: res.append(r)
                else: st.warning(f"SKU não encontrado: {mod} {tec} {co} {ta__}")
            if res:
                st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
                df = pd.DataFrame(res); ds = df.copy()
                for col in ['custo_tecido_lote','custo_final_peca','custo_total_lote','faturamento_sr','lucro']: ds[col] = ds[col].apply(fmt)
                ds['markup_pct'] = ds['markup_pct'].apply(fpct); ds['margem_pct'] = ds['margem_pct'].apply(fpct)
                ds.columns = ['Descrição','Kg','Peso/g','Qtd','C.Tecido','C/Peça','C.Total','Fat.SR','Lucro','Markup%','Margem%']
                st.dataframe(ds, use_container_width=True, hide_index=True)
                st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
                tkg=sum(r['kg'] for r in res); tpcs=sum(r['qtd_pecas'] for r in res)
                tct=sum(r['custo_total_lote'] for r in res); tft=sum(r['faturamento_sr'] for r in res)
                tlc=sum(r['lucro'] for r in res); mgr=tlc/tft if tft else 0
                c1,c2,c3,c4,c5,c6 = st.columns(6)
                c1.metric("Total Kg", f"{tkg:.1f}kg"); c2.metric("Total Peças", tpcs)
                c3.metric("Custo Total", fmt(tct)); c4.metric("Faturamento SR", fmt(tft))
                c5.metric("Lucro Total", fmt(tlc)); c6.metric("Margem Real", fpct(mgr))

# ══ TABELA CLIENTE ══════════════════════════════
elif pagina == "📤 Tabela para Cliente":
    titulo("📤", "Tabela de Preços para Cliente")
    cat = catalogo_cache()
    if not cat:
        st.warning("Nenhum SKU cadastrado.")
    else:
        df = pd.DataFrame(cat)
        c1,c2,c3 = st.columns(3)
        mf = c1.selectbox("Modelo", ['Todos'] + sorted(df['Modelo'].unique()))
        tf = c2.selectbox("Tecido", ['Todos'] + sorted(df['Tecido'].unique()))
        dff = df.copy()
        if mf != 'Todos': dff = dff[dff['Modelo']==mf]
        if tf != 'Todos': dff = dff[dff['Tecido']==tf]
        cf = c3.selectbox("Cor", ['Todas'] + sorted(dff['Cor'].unique()))
        if cf != 'Todas': dff = dff[dff['Cor']==cf]
        fx = st.radio("Faixa de Preço para o Cliente:", ["Super Revenda","Atacado","Varejo","Todas as Faixas"], horizontal=True)
        st.caption(f"{len(dff)} produtos — Faixa: {fx}")
        ds = dff.copy()
        if fx == "Todas as Faixas":
            for c in ['Super Revenda','Atacado','Varejo']: ds[c] = ds[c].apply(fmt)
            cols = ['Modelo','Cor','Tecido','Tamanho','Super Revenda','Atacado','Varejo']
        else:
            ds['Preço'] = ds[fx].apply(fmt)
            cols = ['Modelo','Cor','Tecido','Tamanho','Preço']
        st.dataframe(ds[cols], use_container_width=True, hide_index=True)
        st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
        cp, cw, cc_ = st.columns(3)
        with cp:
            if st.button("Gerar PDF para Cliente"):
                from pdf_gerador import gerar_pdf_tabela_precos
                dados_pdf = []
                for _, row in dff.iterrows():
                    if fx == "Todas as Faixas":
                        dados_pdf.append({'Modelo':row['Modelo'],'Tecido':row['Tecido'],'Cor':row['Cor'],'Tamanho':row['Tamanho'],'Super Revenda':row['Super Revenda'],'Atacado':row['Atacado'],'Varejo':row['Varejo']})
                    else:
                        dados_pdf.append({'Modelo':row['Modelo'],'Tecido':row['Tecido'],'Cor':row['Cor'],'Tamanho':row['Tamanho'],'Faixa':fx,'Preço':row[fx]})
                with st.spinner("Gerando PDF..."):
                    pdf = gerar_pdf_tabela_precos(dados_pdf, f"Modelo: {mf} | Tecido: {tf} | Cor: {cf} | Faixa: {fx}")
                st.download_button("⬇️ Baixar PDF", pdf, file_name=f"tabela_cliente_{date.today()}.pdf", mime="application/pdf")
        with cw:
            if st.button("Gerar Texto WhatsApp"):
                lns = ["*Tabela de Preços — Prates Sublimação* 🧵", ""]
                for _, row in dff.iterrows():
                    if fx == "Todas as Faixas":
                        lns.append(f"• {row['Modelo']} {row['Tecido']} {row['Cor']} ({row['Tamanho']}): SR {fmt(row['Super Revenda'])} | AT {fmt(row['Atacado'])} | VR {fmt(row['Varejo'])}")
                    else:
                        lns.append(f"• {row['Modelo']} {row['Tecido']} {row['Cor']} ({row['Tamanho']}): {fmt(row[fx])}")
                lns += ["", "Pix ou Dinheiro | Retirada local — Macaé/RJ 😊"]
                st.text_area("Copie:", "\n".join(lns), height=220)
        with cc_:
            if fx != "Todas as Faixas":
                dff_csv = dff[['Modelo','Cor','Tecido','Tamanho',fx]].copy(); dff_csv.columns = ['Modelo','Cor','Tecido','Tamanho','Preço']
            else:
                dff_csv = dff[['Modelo','Cor','Tecido','Tamanho','Super Revenda','Atacado','Varejo']].copy()
            st.download_button("⬇️ Exportar CSV", dff_csv.to_csv(index=False).encode('utf-8-sig'), file_name=f"tabela_{date.today()}.csv", mime="text/csv")

# ══ RELATÓRIO MENSAL ════════════════════════════
elif pagina == "📈 Relatório Mensal":
    titulo("📈", "Relatório Mensal")
    ms = st.sidebar.text_input("Mês (AAAA-MM)", datetime.today().strftime('%Y-%m'))
    tp, tr, ta = st.tabs(["Painel do Mês", "Registros", "Novo Registro"])
    with tp:
        regs = get_relatorio_mensal(ms)
        if not regs:
            st.info(f"Nenhum registro para {ms}.")
        else:
            df = pd.DataFrame(regs)
            rec=df['receita'].sum(); cst=df['custo'].sum(); luc=df['lucro'].sum()
            c1,c2,c3,c4,c5,c6 = st.columns(6)
            c1.metric("Pedidos", len(df)); c2.metric("Peças", int(df['qtd_pecas'].sum()))
            c3.metric("Receita", fmt(rec)); c4.metric("Custo", fmt(cst))
            c5.metric("Lucro", fmt(luc)); c6.metric("Margem", fpct(luc/rec if rec else 0))
            col1, col2 = st.columns(2)
            with col1:
                dm = df.groupby('modelo')['receita'].sum().reset_index()
                fig = px.bar(dm, x='modelo', y='receita', color='modelo', color_discrete_sequence=['#2d7a4f','#2563eb','#d97706','#7c3aed'])
                fig.update_layout(**CHART, title="Receita por Modelo", showlegend=False)
                fig.update_xaxes(gridcolor='#1e2330'); fig.update_yaxes(gridcolor='#1e2330')
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                df2 = df.groupby('faixa')['receita'].sum().reset_index()
                fig2 = px.pie(df2, names='faixa', values='receita', hole=0.5, color_discrete_sequence=['#2d7a4f','#2563eb','#d97706'])
                fig2.update_layout(**CHART, title="Receita por Faixa")
                st.plotly_chart(fig2, use_container_width=True)
    with tr:
        regs = get_relatorio_mensal(ms)
        if not regs:
            st.info("Nenhum registro.")
        else:
            df = pd.DataFrame(regs)
            st.dataframe(df[['data','numero_pedido','modelo','faixa','tecido','qtd_pecas','receita','custo','lucro','observacao']], use_container_width=True, hide_index=True)
            rid = st.selectbox("Excluir registro ID:", df['id'].tolist())
            if st.button("Excluir"): delete_registro_mensal(rid); st.rerun()
            st.download_button("⬇️ CSV", df.to_csv(index=False).encode('utf-8-sig'), file_name=f"rel_{ms}.csv", mime="text/csv")
    with ta:
        skus, mods, _ = get_opcoes()
        c1,c2,c3 = st.columns(3)
        dr=c1.date_input("Data",date.today()); nr=c2.text_input("Nº Pedido"); fx_r=c3.selectbox("Faixa",["Super Revenda","Atacado","Varejo"])
        c4,c5,c6 = st.columns(3)
        mr_=c4.selectbox("Modelo",mods); tr_=c5.text_input("Tecido"); qr=c6.number_input("Qtd",1,value=10)
        c7,c8,c9 = st.columns(3)
        cor_r=c7.text_input("Cor"); rr=c8.number_input("Receita (R$)",0.0,step=0.01); cr_=c9.number_input("Custo (R$)",0.0,step=0.01)
        vr_=c1.text_input("Variante"); obs_r=st.text_area("Observação")
        if st.button("Salvar Registro"):
            add_registro_mensal(str(dr),nr,mr_,fx_r,vr_,tr_,qr,cor_r,rr,cr_,round(rr-cr_,2),obs_r)
            st.success("Salvo!"); st.rerun()

# ══ CONFIGURAÇÕES ════════════════════════════════
elif pagina == "⚙️ Configurações":
    titulo("⚙️", "Configurações")
    tp, tf, tfa, ts = st.tabs(["Parâmetros Globais","Fornecedores","Faccionistas","SKUs"])
    with tp:
        st.info("Altere aqui → todos os SKUs recalculam automaticamente.")
        p = get_parametros()
        c1, c2 = st.columns(2)
        with c1:
            fr = st.number_input("Frete (%)", 0.0,1.0,float(p.get('frete_pct',0.05)),0.01,format="%.2f")
            ou = st.number_input("Outros Custos (%)", 0.0,1.0,float(p.get('outros_pct',0.03)),0.01,format="%.2f")
            em = st.number_input("Embalagem/peça (R$)", 0.0,value=float(p.get('embalagem',0.0)),step=0.5)
        with c2:
            ms_= st.number_input("Margem Super Revenda (%)", 0.0,5.0,float(p.get('margem_sr',0.20)),0.01,format="%.2f")
            ma_= st.number_input("Margem Atacado (%)", 0.0,5.0,float(p.get('margem_atacado',0.35)),0.01,format="%.2f")
            mv_= st.number_input("Margem Varejo (%)", 0.0,5.0,float(p.get('margem_varejo',0.50)),0.01,format="%.2f")
        if st.button("Salvar Parâmetros"):
            for k,v in [('frete_pct',fr),('outros_pct',ou),('embalagem',em),('margem_sr',ms_),('margem_atacado',ma_),('margem_varejo',mv_)]: set_parametro(k,v)
            catalogo_cache.clear(); st.success("Parâmetros salvos!"); st.rerun()
    with tf:
        st.info("Atualize o preço/kg aqui. O Fornecedor Ativo é usado em todos os cálculos.")
        busca_forn = st.text_input("🔍 Buscar tecido ou cor", key="busca_forn", placeholder="Digite tecido ou cor...")
        forn_list = get_fornecedores()
        if busca_forn:
            forn_list = [f for f in forn_list if busca_forn.lower() in f['tecido'].lower() or busca_forn.lower() in f['cor'].lower()]
        for fo in forn_list:
            with st.expander(f"{fo['tecido']} — {fo['cor']}   |   Ativo: {fo['fornecedor_ativo']}   |   {fmt(get_preco_kg(fo['tecido'],fo['cor']))}/kg"):
                c1,c2,c3,c4 = st.columns(4)
                f1n=c1.text_input("Fornecedor 1",fo['f1_nome'],key=f"f1n{fo['id']}")
                f1p=c2.number_input("Preço F1",0.0,value=float(fo['f1_preco']),step=0.1,key=f"f1p{fo['id']}")
                f2n=c3.text_input("Fornecedor 2",fo['f2_nome'],key=f"f2n{fo['id']}")
                f2p=c4.number_input("Preço F2",0.0,value=float(fo['f2_preco']),step=0.1,key=f"f2p{fo['id']}")
                c5,c6,c7 = st.columns(3)
                f3n=c5.text_input("Fornecedor 3",fo['f3_nome'],key=f"f3n{fo['id']}")
                f3p=c6.number_input("Preço F3",0.0,value=float(fo['f3_preco']),step=0.1,key=f"f3p{fo['id']}")
                op=['Mais Barato',f1n,f2n,f3n]; ix=op.index(fo['fornecedor_ativo']) if fo['fornecedor_ativo'] in op else 0
                fa_=c7.selectbox("Ativo",op,index=ix,key=f"fa{fo['id']}")
                if st.button("Salvar",key=f"sf{fo['id']}"):
                    ant=get_preco_kg(fo['tecido'],fo['cor'])
                    update_fornecedor(fo['id'],{'f1_nome':f1n,'f1_preco':f1p,'f2_nome':f2n,'f2_preco':f2p,'f3_nome':f3n,'f3_preco':f3p,'fornecedor_ativo':fa_})
                    novo=get_preco_kg(fo['tecido'],fo['cor'])
                    if abs(novo-ant)>0.001: add_historico('Tecido',f"{fo['tecido']} | {fo['cor']}",ant,novo,fa_,'')
                    catalogo_cache.clear(); st.success("Atualizado!"); st.rerun()
        st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
        sec("Adicionar novo Tecido/Cor")
        c1,c2,c3 = st.columns(3)
        nt=c1.text_input("Tecido",key="nt"); nc=c2.text_input("Cor",key="nc"); np_=c3.number_input("Preço F1 (R$/kg)",0.0,step=0.1,key="np")
        if st.button("Adicionar") and nt and nc:
            ok=add_fornecedor(nt,nc,'Fornecedor 1',np_)
            st.success("Adicionado!") if ok else st.error("Já existe."); st.rerun()
    with tfa:
        busca_fac = st.text_input("🔍 Buscar modelo", key="busca_fac", placeholder="Digite o modelo...")
        facs = get_faccionistas()
        if busca_fac:
            facs = [f for f in facs if busca_fac.lower() in f['modelo'].lower()]
        for f in facs:
            pb = float(f.get('f1_preco_branco') or f['f1_preco'])
            pc = float(f.get('f1_preco_colorido') or f['f1_preco'])
            with st.expander(f"{f['modelo']}   |   Ativa: {f['faccionista_ativa']}   |   🤍 Branca: {fmt(pb)}   |   🎨 Colorida: {fmt(pc)}"):
                c1,c2,c3 = st.columns(3)
                fn1=c1.text_input("Faccionista 1",f['f1_nome'],key=f"fn1{f['id']}")
                fn2=c2.text_input("Faccionista 2",f['f2_nome'],key=f"fn2{f['id']}")
                fn3=c3.text_input("Faccionista 3",f['f3_nome'],key=f"fn3{f['id']}")
                st.markdown('<p style="color:#6b7280;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin:8px 0 4px">Costura Blusa Branca</p>', unsafe_allow_html=True)
                cb1,cb2,cb3 = st.columns(3)
                fpb1=cb1.number_input(f"{fn1}",0.0,value=float(f.get('f1_preco_branco') or f['f1_preco']),step=0.1,key=f"fpb1{f['id']}")
                fpb2=cb2.number_input(f"{fn2}",0.0,value=float(f.get('f2_preco_branco') or 0),step=0.1,key=f"fpb2{f['id']}")
                fpb3=cb3.number_input(f"{fn3}",0.0,value=float(f.get('f3_preco_branco') or 0),step=0.1,key=f"fpb3{f['id']}")
                st.markdown('<p style="color:#6b7280;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin:8px 0 4px">Costura Blusa Colorida</p>', unsafe_allow_html=True)
                cc1,cc2,cc3 = st.columns(3)
                fpc1=cc1.number_input(f"{fn1} ",0.0,value=float(f.get('f1_preco_colorido') or f['f1_preco']),step=0.1,key=f"fpc1{f['id']}")
                fpc2=cc2.number_input(f"{fn2} ",0.0,value=float(f.get('f2_preco_colorido') or 0),step=0.1,key=f"fpc2{f['id']}")
                fpc3=cc3.number_input(f"{fn3} ",0.0,value=float(f.get('f3_preco_colorido') or 0),step=0.1,key=f"fpc3{f['id']}")
                c5,c6 = st.columns([1,3])
                op=['Mais Barata',fn1,fn2,fn3]; ix=op.index(f['faccionista_ativa']) if f['faccionista_ativa'] in op else 0
                faa=c5.selectbox("Faccionista Ativa",op,index=ix,key=f"faa{f['id']}")
                if st.button("💾 Salvar",key=f"sfac{f['id']}"):
                    ant=get_preco_costura(f['modelo'])
                    update_faccionista(f['id'],{
                        'f1_nome':fn1,'f1_preco':fpc1,'f2_nome':fn2,'f2_preco':fpc2,'f3_nome':fn3,'f3_preco':fpc3,
                        'f1_preco_branco':fpb1,'f2_preco_branco':fpb2,'f3_preco_branco':fpb3,
                        'f1_preco_colorido':fpc1,'f2_preco_colorido':fpc2,'f3_preco_colorido':fpc3,
                        'faccionista_ativa':faa
                    })
                    novo=get_preco_costura(f['modelo'])
                    if abs(novo-ant)>0.001: add_historico('Costura',f['modelo'],ant,novo,faa,'')
                    catalogo_cache.clear(); st.success("Atualizado!"); st.rerun()
    with ts:
        sk = get_skus()
        df_sk = pd.DataFrame(sk)[['id','modelo','tecido','cor','tamanho','peso_g']] if sk else pd.DataFrame()
        tab_lista, tab_editar, tab_lote, tab_adicionar = st.tabs(["📋 Lista", "✏️ Editar SKU", "🔄 Edição em Lote", "➕ Adicionar SKU"])
        with tab_lista:
            if df_sk.empty:
                st.warning("Nenhum SKU cadastrado.")
            else:
                c1, c2, c3 = st.columns(3)
                f_mod = c1.selectbox("Filtrar Modelo", ['Todos'] + sorted(df_sk['modelo'].unique()), key="lst_mod")
                f_tec = c2.selectbox("Filtrar Tecido", ['Todos'] + sorted(df_sk['tecido'].unique()), key="lst_tec")
                f_cor = c3.selectbox("Filtrar Cor",    ['Todas'] + sorted(df_sk['cor'].unique()),    key="lst_cor")
                dff = df_sk.copy()
                if f_mod != 'Todos': dff = dff[dff['modelo'] == f_mod]
                if f_tec != 'Todos': dff = dff[dff['tecido'] == f_tec]
                if f_cor != 'Todas': dff = dff[dff['cor']    == f_cor]
                st.dataframe(dff, use_container_width=True, hide_index=True)
                st.caption(f"Exibindo {len(dff)} de {len(sk)} SKUs")
        with tab_editar:
            if df_sk.empty:
                st.warning("Nenhum SKU cadastrado.")
            else:
                st.info("Use os filtros para localizar o SKU e edite os dados abaixo.")
                sec("Filtros de Localização")
                c1, c2, c3, c4 = st.columns(4)
                ed_mod = c1.selectbox("Modelo",  ['Todos'] + sorted(df_sk['modelo'].unique()), key="ed_mod")
                ed_tec = c2.selectbox("Tecido",  ['Todos'] + sorted(df_sk['tecido'].unique()), key="ed_tec")
                ed_cor = c3.selectbox("Cor",     ['Todas'] + sorted(df_sk['cor'].unique()),    key="ed_cor")
                ed_tam = c4.selectbox("Tamanho", ['Todos'] + sorted(df_sk['tamanho'].unique()),key="ed_tam")
                df_ed = df_sk.copy()
                if ed_mod != 'Todos': df_ed = df_ed[df_ed['modelo']  == ed_mod]
                if ed_tec != 'Todos': df_ed = df_ed[df_ed['tecido']  == ed_tec]
                if ed_cor != 'Todas': df_ed = df_ed[df_ed['cor']     == ed_cor]
                if ed_tam != 'Todos': df_ed = df_ed[df_ed['tamanho'] == ed_tam]
                st.caption(f"{len(df_ed)} SKU(s) encontrado(s)")
                st.dataframe(df_ed, use_container_width=True, hide_index=True)
                if len(df_ed) == 0:
                    st.warning("Nenhum SKU encontrado com esses filtros.")
                elif len(df_ed) > 1:
                    st.info(f"🔍 {len(df_ed)} SKUs encontrados. Refine os filtros até chegar em 1 SKU para editar.")
                else:
                    sel_id = str(df_ed.iloc[0]['id'])
                    sku_sel = next(s for s in sk if str(s['id']) == sel_id)
                    st.markdown('<hr style="border-color:#252932;margin:10px 0">', unsafe_allow_html=True)
                    c1, c2, c3, c4, c5 = st.columns(5)
                    e_mod = c1.text_input("Modelo",  sku_sel['modelo'],  key="e_mod")
                    e_tec = c2.text_input("Tecido",  sku_sel['tecido'],  key="e_tec")
                    e_cor = c3.text_input("Cor",     sku_sel['cor'],     key="e_cor")
                    _tam_opts = ["P-GG","XGG","1-14"]
                    _tam_idx  = _tam_opts.index(sku_sel['tamanho']) if sku_sel['tamanho'] in _tam_opts else 0
                    e_tam = c4.selectbox("Tamanho", _tam_opts, index=_tam_idx, key="e_tam")
                    e_pes = c5.number_input("Peso (g)", 1.0, value=float(sku_sel['peso_g']), step=5.0, key="e_pes")
                    col_salvar, col_excluir, _ = st.columns([1, 1, 4])
                    with col_salvar:
                        if st.button("💾 Salvar", key="btn_edit_salvar"):
                            upsert_sku(e_mod, e_tec, e_cor, e_tam, e_pes); catalogo_cache.clear()
                            st.success(f"SKU #{sel_id} atualizado!"); st.rerun()
                    with col_excluir:
                        if st.button("🗑️ Excluir", key="btn_edit_excluir"):
                            st.session_state['confirmar_exclusao'] = sel_id
                    if st.session_state.get('confirmar_exclusao') == sel_id:
                        st.warning(f"Confirma exclusão de **#{sel_id} — {sku_sel['modelo']} {sku_sel['tecido']} {sku_sel['cor']} {sku_sel['tamanho']}**?")
                        cc1, cc2, _ = st.columns([1, 1, 4])
                        with cc1:
                            if st.button("✅ Confirmar", key="btn_confirm_del"):
                                delete_sku(int(sel_id)); catalogo_cache.clear()
                                st.session_state.pop('confirmar_exclusao', None); st.success("SKU excluído!"); st.rerun()
                        with cc2:
                            if st.button("❌ Cancelar", key="btn_cancel_del"):
                                st.session_state.pop('confirmar_exclusao', None); st.rerun()
        with tab_lote:
            st.info("Use os filtros para selecionar um grupo de SKUs e altere um campo em todos de uma vez.")
            if df_sk.empty:
                st.warning("Nenhum SKU cadastrado.")
            else:
                sec("Filtros de Seleção")
                c1, c2, c3, c4 = st.columns(4)
                bl_mod = c1.selectbox("Modelo", ['Todos'] + sorted(df_sk['modelo'].unique()), key="bl_mod")
                bl_tec = c2.selectbox("Tecido", ['Todos'] + sorted(df_sk['tecido'].unique()), key="bl_tec")
                bl_cor = c3.selectbox("Cor",    ['Todas'] + sorted(df_sk['cor'].unique()),    key="bl_cor")
                bl_tam = c4.selectbox("Tamanho",['Todos'] + sorted(df_sk['tamanho'].unique()),key="bl_tam")
                df_lote = df_sk.copy()
                if bl_mod != 'Todos': df_lote = df_lote[df_lote['modelo']  == bl_mod]
                if bl_tec != 'Todos': df_lote = df_lote[df_lote['tecido']  == bl_tec]
                if bl_cor != 'Todas': df_lote = df_lote[df_lote['cor']     == bl_cor]
                if bl_tam != 'Todos': df_lote = df_lote[df_lote['tamanho'] == bl_tam]
                st.caption(f"**{len(df_lote)} SKUs** selecionados:")
                st.dataframe(df_lote, use_container_width=True, hide_index=True)
                if len(df_lote) > 0:
                    st.markdown('<hr style="border-color:#252932;margin:10px 0">', unsafe_allow_html=True)
                    sec("Alterar Campo nos SKUs Selecionados")
                    c1, c2 = st.columns(2)
                    campo_lote = c1.selectbox("Campo a alterar", ["peso_g","modelo","tecido","cor","tamanho"], key="bl_campo")
                    if campo_lote == "peso_g":
                        novo_val = c2.number_input("Novo Peso (g)", 1.0, value=235.0, step=5.0, key="bl_val_num")
                    elif campo_lote == "tamanho":
                        novo_val = c2.selectbox("Novo Tamanho", ["P-GG","XGG","1-14"], key="bl_val_tam")
                    else:
                        novo_val = c2.text_input(f"Novo valor para '{campo_lote}'", key="bl_val_txt")
                    if st.button(f"⚡ Aplicar em {len(df_lote)} SKUs", key="btn_lote"):
                        if not novo_val and campo_lote != "peso_g":
                            st.error("Informe o novo valor antes de aplicar.")
                        else:
                            ids_lote = df_lote['id'].tolist()
                            update_sku_campo(ids_lote, campo_lote, novo_val)
                            catalogo_cache.clear()
                            st.success(f"✅ {len(ids_lote)} SKUs atualizados — '{campo_lote}' → '{novo_val}'"); st.rerun()
        with tab_adicionar:
            st.info("Preencha os dados para adicionar ou atualizar um SKU.")
            c1, c2, c3, c4, c5 = st.columns(5)
            ms2  = c1.text_input("Modelo",  "Adulto", key="add_mod")
            ts2  = c2.text_input("Tecido",  "PP",     key="add_tec")
            cs2  = c3.text_input("Cor",               key="add_cor")
            tms2 = c4.selectbox("Tamanho",  ["P-GG","XGG","1-14"], key="add_tam")
            ps2  = c5.number_input("Peso (g)", 1.0, value=235.0, step=5.0, key="add_pes")
            if st.button("💾 Salvar SKU", key="btn_add_sku"):
                upsert_sku(ms2, ts2, cs2, tms2, ps2); catalogo_cache.clear()
                st.success("SKU salvo!"); st.rerun()

# ══ HISTÓRICO ════════════════════════════════════
elif pagina == "📋 Histórico de Preços":
    titulo("📋", "Histórico de Preços")
    tv, ta = st.tabs(["Ver Histórico", "Registrar Manualmente"])
    with tv:
        h = get_historico()
        if not h:
            st.info("Nenhum registro.")
        else:
            dh = pd.DataFrame(h)
            dh['variacao_pct'] = dh['variacao_pct'].apply(fpct)
            st.dataframe(dh[['data','tipo','tecido_modelo','preco_anterior','preco_novo','variacao_pct','fornecedor_faccionista','motivo']], use_container_width=True, hide_index=True)
            st.download_button("⬇️ CSV", dh.to_csv(index=False).encode('utf-8-sig'), file_name=f"historico_{date.today()}.csv", mime="text/csv")
    with ta:
        c1,c2 = st.columns(2)
        th=c1.selectbox("Tipo",["Tecido","Costura"]); tmh=c2.text_input("Tecido/Modelo")
        c3,c4,c5 = st.columns(3)
        ph1=c3.number_input("Preço Anterior",0.0,step=0.01); ph2=c4.number_input("Preço Novo",0.0,step=0.01); fh=c5.text_input("Fornecedor/Faccionista")
        mh=st.text_input("Motivo")
        if st.button("Registrar") and tmh and ph2:
            add_historico(th,tmh,ph1,ph2,fh,mh); st.success("Registrado!"); st.rerun()

# ══ IMPORTAR ═════════════════════════════════════
elif pagina == "📥 Importar Planilha":
    titulo("📥", "Importar Planilha Excel")
    st.info("Faça upload do .xlsx para importar SKUs, fornecedores, faccionistas e parâmetros.")
    arq = st.file_uploader("Selecione o arquivo .xlsx", type=['xlsx'])
    if arq:
        import tempfile, os as _os
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            tmp.write(arq.read()); tp=tmp.name
        if st.button("Importar"):
            from importador import importar_xlsx
            with st.spinner("Importando..."):
                res = importar_xlsx(tp)
            if 'erro' in res: st.error(f"Erro: {res['erro']}")
            else:
                catalogo_cache.clear()
                st.success(f"SKUs: {res['skus']} | Fornecedores: {res['fornecedores']} | Parâmetros: {res['parametros']}")
            _os.unlink(tp)
    st.markdown('<hr style="border-color:#252932;margin:12px 0">', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("SKUs", len(get_skus())); c2.metric("Fornecedores", len(get_fornecedores()))
    c3.metric("Faccionistas", len(get_faccionistas())); c4.metric("Histórico", len(get_historico()))

# ══ USUÁRIOS ═════════════════════════════════════
elif pagina == "👥 Usuários":
    titulo("👥", "Gestão de Usuários")
    tab_lista, tab_novo, tab_minha_conta = st.tabs(["👥 Usuários", "➕ Novo Usuário", "🔑 Minha Conta"])

    with tab_lista:
        usuarios = get_usuarios()
        if not usuarios:
            st.info("Nenhum usuário cadastrado.")
        else:
            for u in usuarios:
                ativo_label = "🟢 Ativo" if u['ativo'] else "🔴 Inativo"
                nivel_color = {"admin": "#2d7a4f", "gerente": "#2563eb", "vendedor": "#d97706", "operador": "#7c3aed"}.get(u['nivel'], "#6b7280")
                with st.expander(f"{u['nome']} — {u['email']}   |   {ativo_label}   |   Nível: {u['nivel']}"):
                    c1, c2, c3 = st.columns(3)
                    novo_nome  = c1.text_input("Nome",  u['nome'],  key=f"un_{u['id']}")
                    novo_email = c2.text_input("Email", u['email'], key=f"ue_{u['id']}")
                    novo_nivel = c3.selectbox("Nível", ["admin","gerente","vendedor","operador"],
                                              index=["admin","gerente","vendedor","operador"].index(u['nivel']),
                                              key=f"uv_{u['id']}")
                    nova_senha = st.text_input("Nova Senha (deixe vazio para não alterar)", type="password", key=f"us_{u['id']}")

                    ca, cb, cc = st.columns(3)
                    with ca:
                        if st.button("💾 Salvar", key=f"usave_{u['id']}"):
                            dados = {'nome': novo_nome, 'email': novo_email.lower(), 'nivel': novo_nivel}
                            if nova_senha:
                                dados['senha_hash'] = hash_senha(nova_senha)
                            update_usuario(u['id'], dados)
                            st.success("Atualizado!"); st.rerun()
                    with cb:
                        label_ativo = "🔴 Desativar" if u['ativo'] else "🟢 Ativar"
                        if st.button(label_ativo, key=f"utog_{u['id']}"):
                            update_usuario(u['id'], {'ativo': not u['ativo']}); st.rerun()
                    with cc:
                        if u['nivel'] != 'admin' or sum(1 for x in usuarios if x['nivel'] == 'admin') > 1:
                            if st.button("🗑️ Excluir", key=f"udel_{u['id']}"):
                                st.session_state[f'confirm_del_user_{u["id"]}'] = True
                        if st.session_state.get(f'confirm_del_user_{u["id"]}'):
                            st.warning(f"Confirma exclusão de **{u['nome']}**?")
                            cd1, cd2 = st.columns(2)
                            with cd1:
                                if st.button("✅ Confirmar", key=f"udelok_{u['id']}"):
                                    delete_usuario(u['id'])
                                    st.session_state.pop(f'confirm_del_user_{u["id"]}', None)
                                    st.success("Excluído!"); st.rerun()
                            with cd2:
                                if st.button("❌ Cancelar", key=f"udelno_{u['id']}"):
                                    st.session_state.pop(f'confirm_del_user_{u["id"]}', None); st.rerun()

    with tab_novo:
        st.info("Crie um novo usuário com nível de acesso definido.")
        c1, c2 = st.columns(2)
        nn = c1.text_input("Nome completo", key="nn")
        ne = c2.text_input("E-mail", key="ne")
        c3, c4 = st.columns(2)
        nv = c3.selectbox("Nível", ["gerente","vendedor","operador","admin"], key="nv")
        ns = c4.text_input("Senha", type="password", key="ns")
        if st.button("➕ Criar Usuário"):
            if not nn or not ne or not ns:
                st.error("Preencha todos os campos.")
            else:
                ok = add_usuario(nn, ne, hash_senha(ns), nv)
                if ok: st.success(f"Usuário **{nn}** criado com sucesso!"); st.rerun()
                else:  st.error("E-mail já cadastrado.")

    with tab_minha_conta:
        st.info("Atualize seus próprios dados de acesso.")
        c1, c2 = st.columns(2)
        mc_nome  = c1.text_input("Nome",  usuario['nome'],  key="mc_nome")
        mc_email = c2.text_input("Email", usuario['email'], key="mc_email")
        mc_senha_atual = st.text_input("Senha Atual", type="password", key="mc_sa")
        c3, c4 = st.columns(2)
        mc_nova  = c3.text_input("Nova Senha", type="password", key="mc_ns")
        mc_conf  = c4.text_input("Confirmar Nova Senha", type="password", key="mc_nc")
        if st.button("💾 Salvar Minha Conta"):
            from auth import verificar_senha
            if not verificar_senha(mc_senha_atual, usuario['senha_hash']):
                st.error("Senha atual incorreta.")
            elif mc_nova and mc_nova != mc_conf:
                st.error("Nova senha e confirmação não conferem.")
            else:
                dados = {'nome': mc_nome, 'email': mc_email.lower()}
                if mc_nova:
                    dados['senha_hash'] = hash_senha(mc_nova)
                update_usuario(usuario['id'], dados)
                st.session_state['usuario_logado'].update(dados)
                st.success("Dados atualizados com sucesso!"); st.rerun()
