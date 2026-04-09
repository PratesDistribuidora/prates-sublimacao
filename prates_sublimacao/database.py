import streamlit as st
"""
database.py — Prates Sublimação
Banco de dados Supabase (PostgreSQL).
"""

from supabase import create_client, Client
from datetime import datetime

SUPABASE_URL = "https://fqzttkinxevjmnvszggm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZxenR0a2lueGV2am1udnN6Z2dtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTY5MDIzNSwiZXhwIjoyMDkxMjY2MjM1fQ.of53M2fXu9a8bo4FrpvmusF-ypHa8opIcyRmzRoWXrk"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

SKUS_PADRAO = [
    ('Adulto','PP','Amarelo Canário','P-GG',235.0),('Adulto','PP','Amarelo Canário','XGG',309.0),
    ('Adulto','PP','Amarelo Ouro','P-GG',235.0),('Adulto','PP','Amarelo Ouro','XGG',309.0),
    ('Adulto','PP','Azul Bebê','P-GG',235.0),('Adulto','PP','Azul Bebê','XGG',309.0),
    ('Adulto','PP','Azul Marinho','P-GG',235.0),('Adulto','PP','Azul Marinho','XGG',309.0),
    ('Adulto','PP','Azul Royal Bic','P-GG',235.0),('Adulto','PP','Azul Royal Bic','XGG',309.0),
    ('Adulto','PP','Azul Turquesa','P-GG',235.0),('Adulto','PP','Azul Turquesa','XGG',309.0),
    ('Adulto','PP','Branco','P-GG',220.0),('Adulto','PP','Branco','XGG',290.0),
    ('Adulto','PP','Charmute','P-GG',235.0),('Adulto','PP','Charmute','XGG',309.0),
    ('Adulto','PP','Cinza Mescla','P-GG',235.0),('Adulto','PP','Cinza Mescla','XGG',309.0),
    ('Adulto','PP','Lavanda','P-GG',235.0),('Adulto','PP','Lavanda','XGG',309.0),
    ('Adulto','PP','Preto','P-GG',235.0),('Adulto','PP','Preto','XGG',309.0),
    ('Adulto','PP','Rosa Bebê','P-GG',235.0),('Adulto','PP','Rosa Bebê','XGG',309.0),
    ('Adulto','PP','Rosa Pink','P-GG',235.0),('Adulto','PP','Rosa Pink','XGG',309.0),
    ('Adulto','PP','Verde Bandeira','P-GG',235.0),('Adulto','PP','Verde Bandeira','XGG',309.0),
    ('Adulto','PP','Verde Bebê','P-GG',235.0),('Adulto','PP','Verde Bebê','XGG',309.0),
    ('Adulto','PP','Verde Musgo','P-GG',235.0),('Adulto','PP','Verde Musgo','XGG',309.0),
    ('Adulto','PP','Vermelho','P-GG',235.0),('Adulto','PP','Vermelho','XGG',309.0),
    ('Baby Look','PP','Amarelo Canário','P-GG',172.0),('Baby Look','PP','Amarelo Canário','XGG',220.0),
    ('Baby Look','PP','Amarelo Ouro','P-GG',172.0),('Baby Look','PP','Amarelo Ouro','XGG',220.0),
    ('Baby Look','PP','Azul Bebê','P-GG',172.0),('Baby Look','PP','Azul Bebê','XGG',220.0),
    ('Baby Look','PP','Azul Marinho','P-GG',172.0),('Baby Look','PP','Azul Marinho','XGG',220.0),
    ('Baby Look','PP','Azul Royal Bic','P-GG',172.0),('Baby Look','PP','Azul Royal Bic','XGG',220.0),
    ('Baby Look','PP','Azul Turquesa','P-GG',172.0),('Baby Look','PP','Azul Turquesa','XGG',220.0),
    ('Baby Look','PP','Branco','P-GG',172.0),('Baby Look','PP','Branco','XGG',220.0),
    ('Baby Look','PP','Charmute','P-GG',172.0),('Baby Look','PP','Charmute','XGG',220.0),
    ('Baby Look','PP','Cinza Mescla','P-GG',172.0),('Baby Look','PP','Cinza Mescla','XGG',220.0),
    ('Baby Look','PP','Lavanda','P-GG',172.0),('Baby Look','PP','Lavanda','XGG',220.0),
    ('Baby Look','PP','Preto','P-GG',172.0),('Baby Look','PP','Preto','XGG',220.0),
    ('Baby Look','PP','Rosa Bebê','P-GG',172.0),('Baby Look','PP','Rosa Bebê','XGG',220.0),
    ('Baby Look','PP','Rosa Pink','P-GG',172.0),('Baby Look','PP','Rosa Pink','XGG',220.0),
    ('Baby Look','PP','Verde Bandeira','P-GG',172.0),('Baby Look','PP','Verde Bandeira','XGG',220.0),
    ('Baby Look','PP','Verde Bebê','P-GG',172.0),('Baby Look','PP','Verde Bebê','XGG',220.0),
    ('Baby Look','PP','Verde Musgo','P-GG',172.0),('Baby Look','PP','Verde Musgo','XGG',220.0),
    ('Baby Look','PP','Vermelho','P-GG',172.0),('Baby Look','PP','Vermelho','XGG',220.0),
    ('Infantil','PP','Amarelo Canário','1-14',149.0),('Infantil','PP','Amarelo Ouro','1-14',149.0),
    ('Infantil','PP','Azul Bebê','1-14',149.0),('Infantil','PP','Azul Marinho','1-14',149.0),
    ('Infantil','PP','Azul Royal Bic','1-14',149.0),('Infantil','PP','Azul Turquesa','1-14',149.0),
    ('Infantil','PP','Branco','1-14',149.0),('Infantil','PP','Charmute','1-14',149.0),
    ('Infantil','PP','Cinza Mescla','1-14',149.0),('Infantil','PP','Lavanda','1-14',149.0),
    ('Infantil','PP','Preto','1-14',149.0),('Infantil','PP','Rosa Bebê','1-14',149.0),
    ('Infantil','PP','Rosa Pink','1-14',149.0),('Infantil','PP','Verde Bandeira','1-14',149.0),
    ('Infantil','PP','Verde Bebê','1-14',149.0),('Infantil','PP','Verde Musgo','1-14',149.0),
    ('Infantil','PP','Vermelho','1-14',149.0),
    ('Regata','PP','Amarelo Canário','P-GG',235.0),('Regata','PP','Amarelo Canário','XGG',309.0),
    ('Regata','PP','Amarelo Ouro','P-GG',235.0),('Regata','PP','Amarelo Ouro','XGG',309.0),
    ('Regata','PP','Azul Bebê','P-GG',235.0),('Regata','PP','Azul Bebê','XGG',309.0),
    ('Regata','PP','Azul Marinho','P-GG',235.0),('Regata','PP','Azul Marinho','XGG',309.0),
    ('Regata','PP','Azul Royal Bic','P-GG',235.0),('Regata','PP','Azul Royal Bic','XGG',309.0),
    ('Regata','PP','Azul Turquesa','P-GG',235.0),('Regata','PP','Azul Turquesa','XGG',309.0),
    ('Regata','PP','Branco','P-GG',220.0),('Regata','PP','Branco','XGG',290.0),
    ('Regata','PP','Charmute','P-GG',235.0),('Regata','PP','Charmute','XGG',309.0),
    ('Regata','PP','Cinza Mescla','P-GG',235.0),('Regata','PP','Cinza Mescla','XGG',309.0),
    ('Regata','PP','Lavanda','P-GG',235.0),('Regata','PP','Lavanda','XGG',309.0),
    ('Regata','PP','Preto','P-GG',235.0),('Regata','PP','Preto','XGG',309.0),
    ('Regata','PP','Rosa Bebê','P-GG',235.0),('Regata','PP','Rosa Bebê','XGG',309.0),
    ('Regata','PP','Rosa Pink','P-GG',235.0),('Regata','PP','Rosa Pink','XGG',309.0),
    ('Regata','PP','Verde Bandeira','P-GG',235.0),('Regata','PP','Verde Bandeira','XGG',309.0),
    ('Regata','PP','Verde Bebê','P-GG',235.0),('Regata','PP','Verde Bebê','XGG',309.0),
    ('Regata','PP','Verde Musgo','P-GG',235.0),('Regata','PP','Verde Musgo','XGG',309.0),
    ('Regata','PP','Vermelho','P-GG',235.0),('Regata','PP','Vermelho','XGG',309.0),
    ('Adulto','PV','Bege','P-GG',249.0),('Adulto','PV','Bege','XGG',353.0),
    ('Adulto','PV','Branco','P-GG',249.0),('Adulto','PV','Branco','XGG',353.0),
    ('Adulto','PV','Marrom','P-GG',249.0),('Adulto','PV','Marrom','XGG',353.0),
    ('Adulto','PV','Preto','P-GG',249.0),('Adulto','PV','Preto','XGG',353.0),
    ('Baby Look','PV','Bege','P-GG',185.0),('Baby Look','PV','Bege','XGG',265.0),
    ('Baby Look','PV','Marrom','P-GG',185.0),('Baby Look','PV','Marrom','XGG',265.0),
    ('Baby Look','PV','Preto','P-GG',185.0),('Baby Look','PV','Preto','XGG',265.0),
    ('Adulto','Dry Fit','Branco','P-GG',193.0),('Adulto','Dry Fit','Branco','XGG',273.0),
    ('Adulto','Dry Fit','Preto','P-GG',193.0),('Adulto','Dry Fit','Preto','XGG',273.0),
    ('Baby Look','Dry Fit','Branco','P-GG',140.0),('Baby Look','Dry Fit','Branco','XGG',184.0),
    ('Baby Look','Dry Fit','Preto','P-GG',140.0),('Baby Look','Dry Fit','Preto','XGG',184.0),
    ('Regata','Dry Fit','Branco','P-GG',162.0),('Regata','Dry Fit','Branco','XGG',230.0),
    ('Regata','Dry Fit','Preto','P-GG',162.0),('Regata','Dry Fit','Preto','XGG',230.0),
    ('Adulto','Algodão','Branco','P-GG',195.0),
]

FORNECEDORES_PADRAO = [
    ('Dry Fit','Preto',36.0),('Dry Fit','Branco',31.5),
    ('Algodão','Branco',37.99),
    ('PV','Branco',29.99),('PV','Preto',30.9),('PV','Marrom',30.9),('PV','Bege',30.9),
    ('PP','Branco',23.5),('PP','Rosa Bebê',30.63),('PP','Azul Bebê',28.37),
    ('PP','Verde Bebê',31.3),('PP','Preto',25.6),('PP','Azul Marinho',31.23),
    ('PP','Amarelo Canário',25.59),('PP','Amarelo Ouro',24.44),('PP','Lavanda',30.75),
    ('PP','Verde Musgo',31.4),('PP','Azul Turquesa',29.2),('PP','Rosa Pink',31.22),
    ('PP','Azul Royal Bic',30.73),('PP','Verde Bandeira',25.6),('PP','Vermelho',31.83),
    ('PP','Charmute',24.44),('PP','Cinza Mescla',24.46),
]


@st.cache_resource(show_spinner=False)
def init_db():
    try:
        defaults = {
            'costura_branco': 4.0, 'costura_outras': 4.0,
            'frete_pct': 0.05, 'outros_pct': 0.03,
            'embalagem': 0.0, 'margem_sr': 0.20,
            'margem_atacado': 0.35, 'margem_varejo': 0.50,
        }
        existentes = supabase.table('parametros').select('chave').execute().data
        chaves_existentes = {r['chave'] for r in existentes}
        for k, v in defaults.items():
            if k not in chaves_existentes:
                supabase.table('parametros').insert({'chave': k, 'valor': v}).execute()

        fac_existentes = supabase.table('faccionistas').select('modelo').execute().data
        modelos_existentes = {r['modelo'] for r in fac_existentes}
        for modelo in ['Adulto', 'Baby Look', 'Infantil', 'Regata']:
            if modelo not in modelos_existentes:
                supabase.table('faccionistas').insert({'modelo': modelo}).execute()

        forn_existentes = supabase.table('fornecedores').select('chave').execute().data
        chaves_forn = {r['chave'] for r in forn_existentes}
        for tecido, cor, preco in FORNECEDORES_PADRAO:
            chave = f"{tecido}|{cor}"
            if chave not in chaves_forn:
                supabase.table('fornecedores').insert({
                    'tecido': tecido, 'cor': cor, 'chave': chave,
                    'f1_nome': 'Importline', 'f1_preco': preco,
                    'fornecedor_ativo': 'Mais Barato'
                }).execute()

        skus_existentes = supabase.table('skus').select('id').execute().data
        if not skus_existentes:
            batch = [{'modelo': m, 'tecido': t, 'cor': c, 'tamanho': ta, 'peso_g': p} for m,t,c,ta,p in SKUS_PADRAO]
            supabase.table('skus').insert(batch).execute()
    except Exception as e:
        pass


def get_parametros():
    rows = supabase.table('parametros').select('*').execute().data
    return {r['chave']: r['valor'] for r in rows}

def set_parametro(chave, valor):
    existing = supabase.table('parametros').select('chave').eq('chave', chave).execute().data
    if existing:
        supabase.table('parametros').update({'valor': valor}).eq('chave', chave).execute()
    else:
        supabase.table('parametros').insert({'chave': chave, 'valor': valor}).execute()


def get_fornecedores():
    return supabase.table('fornecedores').select('*').order('tecido').order('cor').execute().data

def update_fornecedor(fid, data: dict):
    supabase.table('fornecedores').update(data).eq('id', fid).execute()

def get_preco_kg(tecido, cor):
    chave = f"{tecido}|{cor}"
    rows = supabase.table('fornecedores').select('*').eq('chave', chave).execute().data
    if not rows:
        return 0.0
    row = rows[0]
    fa = row['fornecedor_ativo']
    if fa == 'Mais Barato':
        validos = [p for p in [row['f1_preco'], row['f2_preco'], row['f3_preco']] if p and p > 0]
        return min(validos) if validos else 0.0
    precos = {row['f1_nome']: row['f1_preco'], row['f2_nome']: row['f2_preco'], row['f3_nome']: row['f3_preco']}
    return precos.get(fa, 0.0) or 0.0

def add_fornecedor(tecido, cor, f1_nome='Fornecedor 1', f1_preco=0.0):
    chave = f"{tecido}|{cor}"
    try:
        supabase.table('fornecedores').insert({
            'tecido': tecido, 'cor': cor, 'chave': chave,
            'f1_nome': f1_nome, 'f1_preco': f1_preco
        }).execute()
        return True
    except:
        return False


def get_faccionistas():
    return supabase.table('faccionistas').select('*').order('modelo').execute().data

def update_faccionista(fid, data: dict):
    supabase.table('faccionistas').update(data).eq('id', fid).execute()

def get_preco_costura(modelo):
    rows = supabase.table('faccionistas').select('*').eq('modelo', modelo).execute().data
    if not rows:
        return 4.0
    row = rows[0]
    fa = row['faccionista_ativa']
    if fa == 'Mais Barata':
        validos = [p for p in [row['f1_preco'], row['f2_preco'], row['f3_preco']] if p and p > 0]
        return min(validos) if validos else 4.0
    precos = {row['f1_nome']: row['f1_preco'], row['f2_nome']: row['f2_preco'], row['f3_nome']: row['f3_preco']}
    return precos.get(fa, 4.0) or 4.0


def get_skus(modelo=None, tecido=None, cor=None):
    q = supabase.table('skus').select('*')
    if modelo: q = q.eq('modelo', modelo)
    if tecido: q = q.eq('tecido', tecido)
    if cor:    q = q.eq('cor', cor)
    return q.order('modelo').order('tecido').order('cor').order('tamanho').execute().data

def get_peso(modelo, tecido, cor, tamanho):
    rows = supabase.table('skus').select('peso_g').eq('modelo', modelo).eq('tecido', tecido).eq('cor', cor).eq('tamanho', tamanho).execute().data
    return rows[0]['peso_g'] if rows else None

def upsert_sku(modelo, tecido, cor, tamanho, peso_g):
    existing = supabase.table('skus').select('id').eq('modelo', modelo).eq('tecido', tecido).eq('cor', cor).eq('tamanho', tamanho).execute().data
    if existing:
        supabase.table('skus').update({'peso_g': peso_g}).eq('id', existing[0]['id']).execute()
    else:
        supabase.table('skus').insert({'modelo': modelo, 'tecido': tecido, 'cor': cor, 'tamanho': tamanho, 'peso_g': peso_g}).execute()

def delete_sku(sku_id):
    supabase.table('skus').delete().eq('id', sku_id).execute()

def update_sku_campo(ids: list, campo: str, valor):
    campos_permitidos = {'modelo', 'tecido', 'cor', 'tamanho', 'peso_g'}
    if campo not in campos_permitidos:
        raise ValueError(f"Campo '{campo}' nao permitido.")
    for sku_id in ids:
        supabase.table('skus').update({campo: valor}).eq('id', sku_id).execute()


def add_registro_mensal(data, numero_pedido, modelo, faixa, variante_faixa,
                         tecido, qtd_pecas, cor_principal, receita, custo, lucro, observacao=''):
    supabase.table('relatorio_mensal').insert({
        'data': data, 'numero_pedido': numero_pedido, 'modelo': modelo,
        'faixa': faixa, 'variante_faixa': variante_faixa, 'tecido': tecido,
        'qtd_pecas': qtd_pecas, 'cor_principal': cor_principal,
        'receita': receita, 'custo': custo, 'lucro': lucro, 'observacao': observacao
    }).execute()

def get_relatorio_mensal(mes=None):
    q = supabase.table('relatorio_mensal').select('*')
    if mes:
        q = q.gte('data', f'{mes}-01').lte('data', f'{mes}-31')
    return q.order('data', desc=True).execute().data

def delete_registro_mensal(rid):
    supabase.table('relatorio_mensal').delete().eq('id', rid).execute()


def add_historico(tipo, tecido_modelo, preco_anterior, preco_novo, fornecedor_faccionista, motivo=''):
    variacao = round((preco_novo - preco_anterior) / preco_anterior, 4) if preco_anterior else 0
    supabase.table('historico').insert({
        'data': datetime.today().strftime('%Y-%m-%d'),
        'tipo': tipo, 'tecido_modelo': tecido_modelo,
        'preco_anterior': preco_anterior, 'preco_novo': preco_novo,
        'variacao_pct': variacao, 'fornecedor_faccionista': fornecedor_faccionista,
        'motivo': motivo
    }).execute()

def get_historico():
    return supabase.table('historico').select('*').order('data', desc=True).order('id', desc=True).execute().data

def delete_historico(hid):
    supabase.table('historico').delete().eq('id', hid).execute()


def get_usuarios():
    return supabase.table('usuarios').select('id,nome,email,nivel,ativo,criado_em').order('criado_em').execute().data

def get_usuario_por_email(email: str):
    rows = supabase.table('usuarios').select('*').eq('email', email).execute().data
    return rows[0] if rows else None

def add_usuario(nome, email, senha_hash, nivel):
    try:
        supabase.table('usuarios').insert({
            'nome': nome, 'email': email.lower(),
            'senha_hash': senha_hash, 'nivel': nivel, 'ativo': True
        }).execute()
        return True
    except:
        return False

def update_usuario(uid, data: dict):
    supabase.table('usuarios').update(data).eq('id', uid).execute()

def delete_usuario(uid):
    supabase.table('usuarios').delete().eq('id', uid).execute()


# ─────────────────────────────────────────
# TOKENS DE RECUPERAÇÃO DE SENHA
# ─────────────────────────────────────────
def add_token_recuperacao(email: str, codigo: str, expira_em: str):
    # Remove token anterior se existir
    supabase.table('recovery_tokens').delete().eq('email', email).execute()
    supabase.table('recovery_tokens').insert({
        'email': email,
        'codigo': codigo,
        'expira_em': expira_em
    }).execute()

def get_token_recuperacao(email: str, codigo: str):
    rows = supabase.table('recovery_tokens').select('*').eq('email', email).eq('codigo', codigo).execute().data
    return rows[0] if rows else None

def deletar_token_recuperacao(email: str):
    supabase.table('recovery_tokens').delete().eq('email', email).execute()
