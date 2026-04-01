"""
calculadora.py — Prates Sublimação
Toda a lógica de negócio: cálculos de custo e preço de venda.
Sem dependência de Streamlit — funções puras e reutilizáveis.
"""

from database import get_parametros, get_preco_kg, get_preco_costura, get_peso


def calcular_custo(modelo, tecido, cor, tamanho, peso_g=None):
    """
    Calcula o custo completo de uma peça.
    Se peso_g não for fornecido, busca no banco pelo SKU.
    Retorna dict com todos os componentes de custo.
    """
    params = get_parametros()

    if peso_g is None:
        peso_g = get_peso(modelo, tecido, cor, tamanho)
        if peso_g is None:
            return None  # SKU não encontrado

    preco_kg = get_preco_kg(tecido, cor)
    costura = get_preco_costura(modelo)
    frete_pct = params.get('frete_pct', 0.05)
    outros_pct = params.get('outros_pct', 0.03)
    embalagem = params.get('embalagem', 0.0)

    custo_tecido = round(peso_g / 1000 * preco_kg, 2)
    subtotal = round(custo_tecido + costura, 2)
    frete = round(subtotal * frete_pct, 2)
    outros = round(subtotal * outros_pct, 2)
    custo_final = round(subtotal + frete + outros + embalagem, 2)

    return {
        'modelo': modelo, 'tecido': tecido, 'cor': cor, 'tamanho': tamanho,
        'peso_g': peso_g,
        'preco_kg': preco_kg,
        'custo_tecido': custo_tecido,
        'costura': costura,
        'subtotal': subtotal,
        'frete': frete,
        'outros': outros,
        'embalagem': embalagem,
        'custo_final': custo_final,
    }


def calcular_precos_venda(custo_final):
    """
    A partir do custo final, retorna os 3 preços de venda.
    """
    params = get_parametros()
    sr = round(custo_final * (1 + params.get('margem_sr', 0.20)), 2)
    at = round(custo_final * (1 + params.get('margem_atacado', 0.35)), 2)
    vr = round(custo_final * (1 + params.get('margem_varejo', 0.50)), 2)
    return {'super_revenda': sr, 'atacado': at, 'varejo': vr}


def calcular_sku_completo(modelo, tecido, cor, tamanho, peso_g=None):
    """
    Combina custo + preços de venda. Retorna None se SKU não existir.
    """
    custo = calcular_custo(modelo, tecido, cor, tamanho, peso_g)
    if custo is None:
        return None
    precos = calcular_precos_venda(custo['custo_final'])
    return {**custo, **precos}


def calcular_manual(peso_g, preco_kg, costura, embalagem=None, outros_pct=None):
    """
    Modo B do Simulador: cálculo livre sem SKU cadastrado.
    """
    params = get_parametros()
    frete_pct = params.get('frete_pct', 0.05)
    if outros_pct is None:
        outros_pct = params.get('outros_pct', 0.03)
    if embalagem is None:
        embalagem = params.get('embalagem', 0.0)

    custo_tecido = round(peso_g / 1000 * preco_kg, 2)
    subtotal = round(custo_tecido + costura, 2)
    frete = round(subtotal * frete_pct, 2)
    outros = round(subtotal * outros_pct, 2)
    custo_final = round(subtotal + frete + outros + embalagem, 2)

    precos = calcular_precos_venda(custo_final)
    return {
        'peso_g': peso_g, 'preco_kg': preco_kg, 'costura': costura,
        'custo_tecido': custo_tecido, 'subtotal': subtotal,
        'frete': frete, 'outros': outros, 'embalagem': embalagem,
        'custo_final': custo_final, **precos
    }


def calcular_lote(tecido, cor, modelo, tamanho, kg_comprar):
    """
    Simulador de Lote: dado X kg, calcula qtd de peças, custo e lucro.
    """
    peso_g = get_peso(modelo, tecido, cor, tamanho)
    if not peso_g or peso_g == 0:
        return None

    preco_kg = get_preco_kg(tecido, cor)
    sku = calcular_sku_completo(modelo, tecido, cor, tamanho)
    if not sku:
        return None

    qtd = int(kg_comprar * 1000 / peso_g)
    custo_tecido_lote = round(kg_comprar * preco_kg, 2)
    custo_total_lote = round(qtd * sku['custo_final'], 2)
    faturamento_sr = round(qtd * sku['super_revenda'], 2)
    lucro = round(faturamento_sr - custo_total_lote, 2)
    markup = round(lucro / custo_total_lote, 4) if custo_total_lote else 0
    margem = round(lucro / faturamento_sr, 4) if faturamento_sr else 0

    return {
        'descricao': f"{tecido} | {cor} | {modelo} {tamanho}",
        'kg': kg_comprar,
        'peso_peca_g': peso_g,
        'qtd_pecas': qtd,
        'custo_tecido_lote': custo_tecido_lote,
        'custo_final_peca': sku['custo_final'],
        'custo_total_lote': custo_total_lote,
        'faturamento_sr': faturamento_sr,
        'lucro': lucro,
        'markup_pct': markup,
        'margem_pct': margem,
    }


def preco_por_faixa(custo_final, faixa):
    """Retorna o preço correto para a faixa escolhida."""
    p = calcular_precos_venda(custo_final)
    mapa = {
        'Super Revenda': p['super_revenda'],
        'Atacado': p['atacado'],
        'Varejo': p['varejo'],
    }
    return mapa.get(faixa, p['super_revenda'])


def gerar_tabela_catalogo():
    """
    Gera a tabela completa de preços para todos os SKUs cadastrados.
    Equivalente ao GERADOR_CLIENTE da planilha.
    """
    from database import get_skus
    skus = get_skus()
    resultado = []
    for s in skus:
        calc = calcular_sku_completo(s['modelo'], s['tecido'], s['cor'], s['tamanho'], s['peso_g'])
        if calc:
            resultado.append({
                'Modelo': s['modelo'],
                'Tecido': s['tecido'],
                'Cor': s['cor'],
                'Tamanho': s['tamanho'],
                'Peso (g)': s['peso_g'],
                'Custo Final': calc['custo_final'],
                'Super Revenda': calc['super_revenda'],
                'Atacado': calc['atacado'],
                'Varejo': calc['varejo'],
            })
    return resultado


def resumo_dashboard():
    """KPIs gerais para o Dashboard."""
    catalogo = gerar_tabela_catalogo()
    if not catalogo:
        return {}
    params = get_parametros()
    custos = [r['Custo Final'] for r in catalogo]
    srs = [r['Super Revenda'] for r in catalogo]
    return {
        'total_skus': len(catalogo),
        'menor_custo': min(custos),
        'maior_custo': max(custos),
        'menor_sr': min(srs),
        'maior_sr': max(srs),
        'margem_sr_media': round(sum(srs)/len(srs) - sum(custos)/len(custos), 2),
        'embalagem': params.get('embalagem', 0),
        'margem_sr_pct': params.get('margem_sr', 0.20),
    }
