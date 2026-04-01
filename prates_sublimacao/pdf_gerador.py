"""
pdf_gerador.py — Prates Sublimação
Gera PDFs profissionais: Tabela de Preços e Ficha de Custo.
"""

import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, HRFlowable, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

LOGO_PATH = "logo.png"

# Cores da marca
COR_PRIMARIA   = colors.HexColor("#1a1f2e")   # fundo escuro
COR_DESTAQUE   = colors.HexColor("#00c04b")   # verde Prates
COR_LARANJA    = colors.HexColor("#ff6b1a")   # laranja vibrante
COR_CINZA_ESC  = colors.HexColor("#2d3748")
COR_CINZA_MED  = colors.HexColor("#4a5568")
COR_CINZA_CLR  = colors.HexColor("#edf2f7")
COR_BRANCO     = colors.white
COR_AMARELO    = colors.HexColor("#f6c90e")


def _cabecalho(story, titulo_extra=""):
    """Bloco de cabeçalho com logo + título."""
    import os
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image(LOGO_PATH, width=5*cm, height=3.2*cm)
            logo.hAlign = 'LEFT'
        except:
            logo = None
    else:
        logo = None

    estilo_titulo = ParagraphStyle(
        'titulo', fontName='Helvetica-Bold', fontSize=18,
        textColor=COR_PRIMARIA, alignment=TA_RIGHT, spaceAfter=0,
        leading=22,
    )
    estilo_sub = ParagraphStyle(
        'sub', fontName='Helvetica', fontSize=10,
        textColor=COR_CINZA_MED, alignment=TA_RIGHT, spaceAfter=0,
    )
    estilo_data = ParagraphStyle(
        'data', fontName='Helvetica', fontSize=9,
        textColor=COR_CINZA_MED, alignment=TA_RIGHT,
    )

    p_titulo = Paragraph("Prates Sublimação", estilo_titulo)
    p_sub    = Paragraph(titulo_extra, estilo_sub) if titulo_extra else Paragraph("Macaé / RJ", estilo_sub)
    p_data   = Paragraph(f"Emitido em: {date.today().strftime('%d/%m/%Y')}", estilo_data)

    col_logo = [[logo]] if logo else [[Paragraph("", estilo_titulo)]]
    col_texto = [[p_titulo], [p_sub], [p_data]]

    tabela_cab = Table(
        [[col_logo[0][0], [p_titulo, p_sub, p_data]]],
        colWidths=[5.5*cm, 12*cm]
    )
    tabela_cab.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN',  (1,0), (1,0),  'RIGHT'),
    ]))
    story.append(tabela_cab)
    story.append(HRFlowable(width="100%", thickness=2, color=COR_DESTAQUE, spaceAfter=8))


def _fmt(val):
    return f"R$ {val:,.2f}".replace(",","X").replace(".",",").replace("X",".")


# ─────────────────────────────────────────
# PDF — TABELA DE PREÇOS
# ─────────────────────────────────────────
def gerar_pdf_tabela_precos(dados, filtro_desc="Todos os produtos"):
    """
    dados: lista de dicts SEM custo — apenas preços de venda.
    Retorna bytes do PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=2*cm,
        title="Tabela de Preços — Prates Sublimação",
    )
    story = []
    _cabecalho(story, "Tabela de Preços")

    est_filtro = ParagraphStyle('filtro', fontName='Helvetica-Oblique', fontSize=9,
                                 textColor=COR_CINZA_MED, spaceAfter=10)
    story.append(Paragraph(f"Filtro: {filtro_desc}", est_filtro))

    # Detecta modo: faixa única ou todas as faixas
    tem_todas = dados and 'Super Revenda' in dados[0] and 'Atacado' in dados[0]

    if tem_todas:
        cabecalho = ["Modelo", "Tecido", "Cor", "Tam.", "Super\nRevenda", "Atacado", "Varejo"]
        linhas = [cabecalho]
        for d in dados:
            linhas.append([
                d['Modelo'], d['Tecido'], d['Cor'], d['Tamanho'],
                _fmt(d['Super Revenda']),
                _fmt(d['Atacado']),
                _fmt(d['Varejo']),
            ])
        col_w = [3.0*cm, 2.2*cm, 3.8*cm, 1.6*cm, 2.6*cm, 2.4*cm, 2.4*cm]
    else:
        faixa_nome = dados[0].get('Faixa','Preço') if dados else 'Preço'
        cabecalho = ["Modelo", "Tecido", "Cor", "Tamanho", faixa_nome]
        linhas = [cabecalho]
        for d in dados:
            linhas.append([
                d['Modelo'], d['Tecido'], d['Cor'], d['Tamanho'],
                _fmt(d['Preço']),
            ])
        col_w = [3.5*cm, 2.5*cm, 4.5*cm, 2.5*cm, 5.0*cm]

    tabela = Table(linhas, colWidths=col_w, repeatRows=1)

    estilo_tab = TableStyle([
        # Cabeçalho
        ('BACKGROUND',   (0,0), (-1,0), COR_PRIMARIA),
        ('TEXTCOLOR',    (0,0), (-1,0), COR_BRANCO),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0), 8),
        ('ALIGN',        (0,0), (-1,0), 'CENTER'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        # Dados
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',     (0,1), (-1,-1), 7.5),
        ('ALIGN',        (4,1), (-1,-1), 'RIGHT'),
        ('ALIGN',        (0,1), (3,-1), 'LEFT'),
        # Destaque preço Super Revenda (col 4 quando tem_todas)
        ('TEXTCOLOR',    (4,1), (4,-1), COR_DESTAQUE),
        ('FONTNAME',     (4,1), (4,-1), 'Helvetica-Bold'),
        # Grid
        ('GRID',         (0,0), (-1,-1), 0.3, colors.HexColor("#d0d7de")),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('LEFTPADDING',  (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ])

    # Linhas alternadas
    for i in range(1, len(linhas)):
        bg = COR_BRANCO if i % 2 == 0 else COR_CINZA_CLR
        estilo_tab.add('BACKGROUND', (0,i), (-1,i), bg)

    tabela.setStyle(estilo_tab)
    story.append(tabela)

    # Rodapé
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=COR_CINZA_MED))
    est_rod = ParagraphStyle('rod', fontName='Helvetica', fontSize=8,
                              textColor=COR_CINZA_MED, alignment=TA_CENTER, spaceBefore=6)
    story.append(Paragraph(
        "Prates Sublimação — Macaé / RJ  |  Pix ou Dinheiro  |  Retirada local 😊  |  Preços sujeitos a alteração sem aviso prévio",
        est_rod
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()


# ─────────────────────────────────────────
# PDF — FICHA DE CUSTO
# ─────────────────────────────────────────
def gerar_pdf_ficha_custo(calc):
    """
    calc: dict retornado por calcular_sku_completo()
    Retorna bytes do PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=2*cm,
        title="Ficha de Custo — Prates Sublimação",
    )
    story = []
    _cabecalho(story, "Ficha de Custo")

    # Título do produto
    est_prod = ParagraphStyle('prod', fontName='Helvetica-Bold', fontSize=15,
                               textColor=COR_PRIMARIA, spaceBefore=10, spaceAfter=4)
    est_sub = ParagraphStyle('subp', fontName='Helvetica', fontSize=10,
                              textColor=COR_CINZA_MED, spaceAfter=12)

    nome = f"{calc['modelo']} — {calc['tecido']} {calc['cor']} ({calc['tamanho']})"
    story.append(Paragraph(nome, est_prod))
    story.append(Paragraph(f"Peso: {calc['peso_g']}g  |  Tecido: {calc['preco_kg']:.2f} R$/kg", est_sub))

    # Tabela de custo detalhado
    def linha(label, valor, negrito=False, destaque=False):
        fn = 'Helvetica-Bold' if negrito else 'Helvetica'
        return [label, _fmt(valor)]

    linhas_custo = [
        ["COMPONENTE", "VALOR"],
        ["Custo do Tecido\n(peso × preço/kg)", _fmt(calc['custo_tecido'])],
        ["Costura", _fmt(calc['costura'])],
        ["Subtotal (tecido + costura)", _fmt(calc['subtotal'])],
        ["Frete (5% sobre subtotal)", _fmt(calc['frete'])],
        ["Outros Custos (3% sobre subtotal)", _fmt(calc['outros'])],
        ["Embalagem", _fmt(calc['embalagem'])],
    ]

    tabela_custo = Table(linhas_custo, colWidths=[11*cm, 5*cm])
    tabela_custo.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), COR_PRIMARIA),
        ('TEXTCOLOR',    (0,0), (-1,0), COR_BRANCO),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0), 9),
        ('ALIGN',        (0,0), (-1,0), 'CENTER'),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',     (0,1), (-1,-1), 9),
        ('ALIGN',        (1,1), (1,-1), 'RIGHT'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('GRID',         (0,0), (-1,-1), 0.3, colors.HexColor("#d0d7de")),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
    ]))
    for i in range(1, len(linhas_custo)):
        bg = COR_BRANCO if i % 2 == 0 else COR_CINZA_CLR
        tabela_custo.setStyle(TableStyle([('BACKGROUND', (0,i), (-1,i), bg)]))

    story.append(tabela_custo)
    story.append(Spacer(1, 0.3*cm))

    # Bloco de custo final — destaque
    tab_cf = Table(
        [["CUSTO FINAL / PEÇA", _fmt(calc['custo_final'])]],
        colWidths=[11*cm, 5*cm]
    )
    tab_cf.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), COR_PRIMARIA),
        ('TEXTCOLOR',    (0,0), (-1,-1), COR_DESTAQUE),
        ('FONTNAME',     (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (0,0),   10),
        ('FONTSIZE',     (1,0), (1,0),   13),
        ('ALIGN',        (1,0), (1,0),   'RIGHT'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0), (-1,-1), 8),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tab_cf)
    story.append(Spacer(1, 0.5*cm))

    # Tabela de preços de venda
    est_sec = ParagraphStyle('sec', fontName='Helvetica-Bold', fontSize=11,
                              textColor=COR_PRIMARIA, spaceBefore=6, spaceAfter=6)
    story.append(Paragraph("Preços de Venda", est_sec))

    linhas_pv = [
        ["FAIXA", "PREÇO", "MARGEM (R$)", "MARKUP"],
        ["🟢  Super Revenda (+20%)",
         _fmt(calc['super_revenda']),
         _fmt(calc['super_revenda'] - calc['custo_final']),
         "20%"],
        ["🔵  Atacado (+35%)",
         _fmt(calc['atacado']),
         _fmt(calc['atacado'] - calc['custo_final']),
         "35%"],
        ["🔴  Varejo (+50%)",
         _fmt(calc['varejo']),
         _fmt(calc['varejo'] - calc['custo_final']),
         "50%"],
    ]
    tab_pv = Table(linhas_pv, colWidths=[8*cm, 3*cm, 3*cm, 2*cm])
    tab_pv.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), COR_CINZA_ESC),
        ('TEXTCOLOR',    (0,0), (-1,0), COR_BRANCO),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0), 9),
        ('ALIGN',        (0,0), (-1,0), 'CENTER'),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',     (0,1), (-1,-1), 9),
        ('ALIGN',        (1,1), (-1,-1), 'RIGHT'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('GRID',         (0,0), (-1,-1), 0.3, colors.HexColor("#d0d7de")),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        # Destaque linha Super Revenda
        ('TEXTCOLOR',    (1,1), (1,1), COR_DESTAQUE),
        ('FONTNAME',     (1,1), (1,1), 'Helvetica-Bold'),
    ]))
    for i in range(1, 4):
        bg = COR_BRANCO if i % 2 == 0 else COR_CINZA_CLR
        tab_pv.setStyle(TableStyle([('BACKGROUND', (0,i), (-1,i), bg)]))
    story.append(tab_pv)

    # Rodapé
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=COR_CINZA_MED))
    est_rod = ParagraphStyle('rod', fontName='Helvetica', fontSize=8,
                              textColor=COR_CINZA_MED, alignment=TA_CENTER, spaceBefore=6)
    story.append(Paragraph(
        f"Prates Sublimação — Macaé / RJ  |  Ficha gerada em {date.today().strftime('%d/%m/%Y')}",
        est_rod
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
