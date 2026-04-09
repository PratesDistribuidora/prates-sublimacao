"""
calculadora.py — Prates Sublimação
Lógica de negócio: cálculos de custo e preço de venda.
Otimizado: busca todos os dados do Supabase de uma vez (sem loop de chamadas).
"""

from database import (
    get_parametros, get_preco_kg, get_preco_costura, get_peso,
    get_skus, get_fornecedores, get_faccionistas
)


def _carregar_dados_base():
    """Carrega todos os dados necessários de uma vez só."""
    params      = get_parametros()
    fornecedores = get_fornecedores()
    faccionistas = get_faccionistas()
    skus         = get_skus()

    # Índices para lookup rápido
    preco_kg_idx = {}
    for f in fornecedores:
        ativo = f.get('fornecedor_ativo', 'Mais Barato')
        if ativo == 'Mais Barato':
            precos = [f['f1_preco'], f['f2_preco'], f['f3_preco']]
            preco = min(p for p in precos if p > 0) if any(p > 0 for p in precos) else 0
        elif ativo == f.get('f1_nome'): preco = f['f1_preco']
        elif ativo == f.get('f2_nome'): preco = f['f2_preco']
        elif ativo == f.get('f3_nome'): preco = f['f3_preco']
        else: preco = f['f1_preco']
        preco_kg_idx[(f['tecido'], f['cor'])] = preco

    costura_idx = {}
    for fac in faccionistas:
        ativo = fac.get('faccionista_ativa', 'Mais Barata')
        if ativo == 'Mais Barata':
            precos = [fac['f1_preco'], fac['f2_preco'], fac['f3_preco']]
            preco = min(p for p in precos if p > 0) if any(p > 0 for p in precos) else 0
        elif ativo == fac.get('f1_nome'): preco = fac['f1_preco']
        elif ativo == fac.get('f2_nome'): preco = fac['f2_preco']
        elif ativo == fac.get('f3_nome'): preco = fac['f3_preco']
        else: preco = fac['f1_preco']
        costura_idx[fac['modelo']] = preco

    return params, preco_kg_idx, costura_idx, skus


def _calcular_custo_rapido(peso_g, preco_kg, costura, params):
    """Calcula custo sem chamar o banco."""
    frete_pct  = params.get('frete_pct', 0.05)
    outros_pct = params.get('outros_pct', 0.03)
    embalagem  = params.get('embalagem', 0.0)

    custo_tecido = round(peso_g / 1000 * preco_kg, 2)
    subtotal     = round(custo_tecido + costura, 2)
    frete        = round(subtotal * frete_pct, 2)
    outros       = round(subtotal * outros_pct, 2)
    custo_final  = round(subtotal + frete + outros + embalagem, 2)
    return custo_tecido, subtotal, frete, outros, embalagem, custo_final


def _calcular_precos(custo_final, params):
    sr = round(custo_final * (1 + params.get('margem_sr', 0.20)), 2)
    at = round(custo_final * (1 + params.get('margem_atacado', 0.35)), 2)
    vr = round(custo_final * (1 + params.get('margem_varejo', 0.50)), 2)
    return sr, at, vr


def calcular_custo(modelo, tecido, cor, tamanho, peso_g=None):
    params   = get_parametros()
    if peso_g is None:
        peso_g = get_peso(modelo, tecido, cor, tamanho)
        if peso_g is None:
            return None
    preco_kg = get_preco_kg(tecido, cor)
    costura  = get_preco_costura(modelo)
    custo_tecido, subtotal, frete, outros, embalagem, custo_final = _calcular_custo_rapido(peso_g, preco_kg, costura, params)
    return {
        'modelo': modelo, 'tecido': tecido, 'cor': cor, 'tamanho': tamanho,
        'peso_g': peso_g, 'preco_kg': preco_kg, 'custo_tecido': custo_tecido,
        'costura': costura, 'subtotal': subtotal, 'frete': frete,
        'outros': outros, 'embalagem': embalagem, 'custo_final': custo_final,
    }


def calcular_precos_venda(custo_final):
    params = get_parametros()
    sr, at, vr = _calcular_precos(custo_final, params)
    return {'super_revenda': sr, 'atacado': at, 'varejo': vr}


def calcular_sku_completo(modelo, tecido, cor, tamanho, peso_g=None):
    custo = calcular_custo(modelo, tecido, cor, tamanho, peso_g)
    if custo is None:
        return None
    precos = calcular_precos_venda(custo['custo_final'])
    return {**custo, **precos}


def calcular_manual(peso_g, preco_kg, costura, embalagem=None, outros_pct=None):
    params = get_parametros()
    frete_pct = params.get('frete_pct', 0.05)
    if outros_pct is None: outros_pct = params.get('outros_pct', 0.03)
    if embalagem is None:  embalagem  = params.get('embalagem', 0.0)
    custo_tecido = round(peso_g / 1000 * preco_kg, 2)
    subtotal     = round(custo_tecido + costura, 2)
    frete        = round(subtotal * frete_pct, 2)
    outros       = round(subtotal * outros_pct, 2)
    custo_final  = round(subtotal + frete + outros + embalagem, 2)
    precos = calcular_precos_venda(custo_final)
    return {
        'peso_g': peso_g, 'preco_kg': preco_kg, 'costura': costura,
        'custo_tecido': custo_tecido, 'subtotal': subtotal,
        'frete': frete, 'outros': outros, 'embalagem': embalagem,
        'custo_final': custo_final, **precos
    }


def calcular_lote(tecido, cor, modelo, tamanho, kg_comprar):
    peso_g = get_peso(modelo, tecido, cor, tamanho)
    if not peso_g or peso_g == 0:
        return None
    preco_kg = get_preco_kg(tecido, cor)
    sku = calcular_sku_completo(modelo, tecido, cor, tamanho)
    if not sku:
        return None
    qtd = int(kg_comprar * 1000 / peso_g)
    custo_tecido_lote = round(kg_comprar * preco_kg, 2)
    custo_total_lote  = round(qtd * sku['custo_final'], 2)
    faturamento_sr    = round(qtd * sku['super_revenda'], 2)
    lucro  = round(faturamento_sr - custo_total_lote, 2)
    markup = round(lucro / custo_total_lote, 4) if custo_total_lote else 0
    margem = round(lucro / faturamento_sr, 4) if faturamento_sr else 0
    return {
        'descricao': f"{tecido} | {cor} | {modelo} {tamanho}",
        'kg': kg_comprar, 'peso_peca_g': peso_g, 'qtd_pecas': qtd,
        'custo_tecido_lote': custo_tecido_lote,
        'custo_final_peca': sku['custo_final'],
        'custo_total_lote': custo_total_lote,
        'faturamento_sr': faturamento_sr,
        'lucro': lucro, 'markup_pct': markup, 'margem_pct': margem,
    }


def preco_por_faixa(custo_final, faixa):
    p = calcular_precos_venda(custo_final)
    return {'Super Revenda': p['super_revenda'], 'Atacado': p['atacado'], 'Varejo': p['varejo']}.get(faixa, p['super_revenda'])


def gerar_tabela_catalogo():
    """
    Gera tabela completa — busca TUDO de uma vez, sem loop de chamadas ao banco.
    """
    params, preco_kg_idx, costura_idx, skus = _carregar_dados_base()
    resultado = []
    for s in skus:
        pk  = preco_kg_idx.get((s['tecido'], s['cor']), 0)
        cos = costura_idx.get(s['modelo'], 4.0)
        _, _, _, _, _, custo_final = _calcular_custo_rapido(s['peso_g'], pk, cos, params)
        sr, at, vr = _calcular_precos(custo_final, params)
        resultado.append({
            'Modelo': s['modelo'], 'Tecido': s['tecido'],
            'Cor': s['cor'], 'Tamanho': s['tamanho'],
            'Peso (g)': s['peso_g'], 'Custo Final': custo_final,
            'Super Revenda': sr, 'Atacado': at, 'Varejo': vr,
        })
    return resultado


def resumo_dashboard():
    """KPIs — usa gerar_tabela_catalogo que já é otimizado."""
    catalogo = gerar_tabela_catalogo()
    if not catalogo:
        return {}
    params = get_parametros()
    custos = [r['Custo Final'] for r in catalogo]
    srs    = [r['Super Revenda'] for r in catalogo]
    return {
        'total_skus':    len(catalogo),
        'menor_custo':   min(custos),
        'maior_custo':   max(custos),
        'menor_sr':      min(srs),
        'maior_sr':      max(srs),
        'margem_sr_media': round(sum(srs)/len(srs) - sum(custos)/len(custos), 2),
        'embalagem':     params.get('embalagem', 0),
        'margem_sr_pct': params.get('margem_sr', 0.20),
    }
