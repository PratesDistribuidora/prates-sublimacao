"""
database.py — Prates Sublimação
Gerencia o banco SQLite: criação das tabelas e todas as operações CRUD.
"""

import sqlite3
from datetime import datetime

DB_PATH = "prates_sublimacao.db"

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

# ─────────────────────────────────────────
# CONEXÃO
# ─────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────
# INICIALIZAÇÃO
# ─────────────────────────────────────────
def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS parametros (
        chave TEXT PRIMARY KEY,
        valor REAL
    );

    CREATE TABLE IF NOT EXISTS fornecedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tecido TEXT NOT NULL,
        cor TEXT NOT NULL,
        chave TEXT UNIQUE NOT NULL,
        f1_nome TEXT DEFAULT 'Importline',
        f1_preco REAL DEFAULT 0,
        f2_nome TEXT DEFAULT 'Fornecedor 2',
        f2_preco REAL DEFAULT 0,
        f3_nome TEXT DEFAULT 'Fornecedor 3',
        f3_preco REAL DEFAULT 0,
        fornecedor_ativo TEXT DEFAULT 'Mais Barato'
    );

    CREATE TABLE IF NOT EXISTS faccionistas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        modelo TEXT UNIQUE NOT NULL,
        f1_nome TEXT DEFAULT 'Faccionista 1',
        f1_preco REAL DEFAULT 4.0,
        f2_nome TEXT DEFAULT 'Faccionista 2',
        f2_preco REAL DEFAULT 0,
        f3_nome TEXT DEFAULT 'Faccionista 3',
        f3_preco REAL DEFAULT 0,
        faccionista_ativa TEXT DEFAULT 'Mais Barata'
    );

    CREATE TABLE IF NOT EXISTS skus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        modelo TEXT NOT NULL,
        tecido TEXT NOT NULL,
        cor TEXT NOT NULL,
        tamanho TEXT NOT NULL,
        peso_g REAL NOT NULL,
        UNIQUE(modelo, tecido, cor, tamanho)
    );

    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL,
        cliente TEXT DEFAULT '',
        data TEXT,
        faixa_preco TEXT DEFAULT 'Super Revenda',
        status TEXT DEFAULT 'Aberto',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS pedido_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER,
        modelo TEXT,
        tecido TEXT,
        cor TEXT,
        tamanho TEXT,
        qtd INTEGER,
        preco_unit REAL,
        custo_unit REAL,
        FOREIGN KEY(pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS relatorio_mensal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        numero_pedido TEXT,
        modelo TEXT,
        faixa TEXT,
        variante_faixa TEXT,
        tecido TEXT,
        qtd_pecas INTEGER,
        cor_principal TEXT,
        receita REAL DEFAULT 0,
        custo REAL DEFAULT 0,
        lucro REAL DEFAULT 0,
        observacao TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        tipo TEXT,
        tecido_modelo TEXT,
        preco_anterior REAL,
        preco_novo REAL,
        variacao_pct REAL,
        fornecedor_faccionista TEXT,
        motivo TEXT DEFAULT ''
    );
    """)

    conn.commit()

    # Parâmetros padrão
    defaults = {
        'costura_branco': 4.0, 'costura_outras': 4.0,
        'frete_pct': 0.05, 'outros_pct': 0.03,
        'embalagem': 0.0, 'margem_sr': 0.20,
        'margem_atacado': 0.35, 'margem_varejo': 0.50,
    }
    for k, v in defaults.items():
        c.execute('INSERT OR IGNORE INTO parametros VALUES (?,?)', (k, v))

    # Faccionistas padrão
    for modelo in ['Adulto','Baby Look','Infantil','Regata']:
        c.execute('INSERT OR IGNORE INTO faccionistas (modelo) VALUES (?)', (modelo,))

    # Fornecedores padrão
    for tecido, cor, preco in FORNECEDORES_PADRAO:
        chave = f"{tecido}|{cor}"
        c.execute("""INSERT OR IGNORE INTO fornecedores
                     (tecido,cor,chave,f1_nome,f1_preco,fornecedor_ativo)
                     VALUES (?,?,?,'Importline',?,'Mais Barato')""",
                  (tecido, cor, chave, preco))

    # SKUs padrão
    for row in SKUS_PADRAO:
        c.execute('INSERT OR IGNORE INTO skus (modelo,tecido,cor,tamanho,peso_g) VALUES (?,?,?,?,?)', row)

    conn.commit()
    conn.close()


# ─────────────────────────────────────────
# PARÂMETROS
# ─────────────────────────────────────────
def get_parametros():
    conn = get_conn()
    rows = conn.execute('SELECT chave, valor FROM parametros').fetchall()
    conn.close()
    return {r['chave']: r['valor'] for r in rows}

def set_parametro(chave, valor):
    conn = get_conn()
    conn.execute('INSERT OR REPLACE INTO parametros VALUES (?,?)', (chave, valor))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────
# FORNECEDORES
# ─────────────────────────────────────────
def get_fornecedores():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM fornecedores ORDER BY tecido, cor').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_fornecedor(fid, data: dict):
    """data pode conter: f1_nome, f1_preco, f2_nome, f2_preco, f3_nome, f3_preco, fornecedor_ativo"""
    campos = ', '.join(f"{k}=?" for k in data)
    conn = get_conn()
    conn.execute(f'UPDATE fornecedores SET {campos} WHERE id=?', list(data.values()) + [fid])
    conn.commit()
    conn.close()

def get_preco_kg(tecido, cor):
    conn = get_conn()
    row = conn.execute('SELECT * FROM fornecedores WHERE chave=?', (f"{tecido}|{cor}",)).fetchone()
    conn.close()
    if not row:
        return 0.0
    row = dict(row)
    fa = row['fornecedor_ativo']
    precos = {'Mais Barato': None, row['f1_nome']: row['f1_preco'],
              row['f2_nome']: row['f2_preco'], row['f3_nome']: row['f3_preco']}
    if fa == 'Mais Barato':
        validos = [p for p in [row['f1_preco'], row['f2_preco'], row['f3_preco']] if p and p > 0]
        return min(validos) if validos else 0.0
    return precos.get(fa, 0.0) or 0.0

def add_fornecedor(tecido, cor, f1_nome='Fornecedor 1', f1_preco=0.0):
    chave = f"{tecido}|{cor}"
    conn = get_conn()
    try:
        conn.execute("""INSERT INTO fornecedores (tecido,cor,chave,f1_nome,f1_preco)
                        VALUES (?,?,?,?,?)""", (tecido, cor, chave, f1_nome, f1_preco))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# ─────────────────────────────────────────
# FACCIONISTAS
# ─────────────────────────────────────────
def get_faccionistas():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM faccionistas ORDER BY modelo').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_faccionista(fid, data: dict):
    campos = ', '.join(f"{k}=?" for k in data)
    conn = get_conn()
    conn.execute(f'UPDATE faccionistas SET {campos} WHERE id=?', list(data.values()) + [fid])
    conn.commit()
    conn.close()

def get_preco_costura(modelo):
    conn = get_conn()
    row = conn.execute('SELECT * FROM faccionistas WHERE modelo=?', (modelo,)).fetchone()
    conn.close()
    if not row:
        return 4.0
    row = dict(row)
    fa = row['faccionista_ativa']
    precos_map = {row['f1_nome']: row['f1_preco'],
                  row['f2_nome']: row['f2_preco'],
                  row['f3_nome']: row['f3_preco']}
    if fa == 'Mais Barata':
        validos = [p for p in [row['f1_preco'], row['f2_preco'], row['f3_preco']] if p and p > 0]
        return min(validos) if validos else 4.0
    return precos_map.get(fa, 4.0) or 4.0


# ─────────────────────────────────────────
# SKUs
# ─────────────────────────────────────────
def get_skus(modelo=None, tecido=None, cor=None):
    conn = get_conn()
    q = 'SELECT * FROM skus WHERE 1=1'
    params = []
    if modelo:
        q += ' AND modelo=?'; params.append(modelo)
    if tecido:
        q += ' AND tecido=?'; params.append(tecido)
    if cor:
        q += ' AND cor=?'; params.append(cor)
    q += ' ORDER BY modelo, tecido, cor, tamanho'
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_peso(modelo, tecido, cor, tamanho):
    conn = get_conn()
    row = conn.execute(
        'SELECT peso_g FROM skus WHERE modelo=? AND tecido=? AND cor=? AND tamanho=?',
        (modelo, tecido, cor, tamanho)).fetchone()
    conn.close()
    return row['peso_g'] if row else None

def upsert_sku(modelo, tecido, cor, tamanho, peso_g):
    conn = get_conn()
    conn.execute("""INSERT INTO skus (modelo,tecido,cor,tamanho,peso_g) VALUES (?,?,?,?,?)
                    ON CONFLICT(modelo,tecido,cor,tamanho) DO UPDATE SET peso_g=excluded.peso_g""",
                 (modelo, tecido, cor, tamanho, peso_g))
    conn.commit()
    conn.close()

def delete_sku(sku_id):
    conn = get_conn()
    conn.execute('DELETE FROM skus WHERE id=?', (sku_id,))
    conn.commit()
    conn.close()

def update_sku_campo(ids: list, campo: str, valor):
    """Atualiza um campo específico em uma lista de SKUs pelo ID."""
    campos_permitidos = {'modelo', 'tecido', 'cor', 'tamanho', 'peso_g'}
    if campo not in campos_permitidos:
        raise ValueError(f"Campo '{campo}' não permitido.")
    conn = get_conn()
    for sku_id in ids:
        conn.execute(f'UPDATE skus SET {campo}=? WHERE id=?', (valor, sku_id))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────
# PEDIDOS
# ─────────────────────────────────────────
def criar_pedido(numero, cliente, data, faixa_preco):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO pedidos (numero,cliente,data,faixa_preco) VALUES (?,?,?,?)",
              (numero, cliente, data, faixa_preco))
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return pid

def adicionar_item_pedido(pedido_id, modelo, tecido, cor, tamanho, qtd, preco_unit, custo_unit):
    conn = get_conn()
    conn.execute("""INSERT INTO pedido_itens
                    (pedido_id,modelo,tecido,cor,tamanho,qtd,preco_unit,custo_unit)
                    VALUES (?,?,?,?,?,?,?,?)""",
                 (pedido_id, modelo, tecido, cor, tamanho, qtd, preco_unit, custo_unit))
    conn.commit()
    conn.close()

def get_pedido(pedido_id):
    conn = get_conn()
    p = conn.execute('SELECT * FROM pedidos WHERE id=?', (pedido_id,)).fetchone()
    itens = conn.execute('SELECT * FROM pedido_itens WHERE pedido_id=?', (pedido_id,)).fetchall()
    conn.close()
    if not p:
        return None, []
    return dict(p), [dict(i) for i in itens]

def get_pedidos():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM pedidos ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def deletar_pedido(pedido_id):
    conn = get_conn()
    conn.execute('DELETE FROM pedidos WHERE id=?', (pedido_id,))
    conn.commit()
    conn.close()

def deletar_item_pedido(item_id):
    conn = get_conn()
    conn.execute('DELETE FROM pedido_itens WHERE id=?', (item_id,))
    conn.commit()
    conn.close()

def proximo_numero_pedido():
    conn = get_conn()
    row = conn.execute("SELECT numero FROM pedidos ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    if not row:
        return "001"
    try:
        return str(int(row['numero']) + 1).zfill(3)
    except:
        return "001"


# ─────────────────────────────────────────
# RELATÓRIO MENSAL
# ─────────────────────────────────────────
def add_registro_mensal(data, numero_pedido, modelo, faixa, variante_faixa,
                         tecido, qtd_pecas, cor_principal, receita, custo, lucro, observacao=''):
    conn = get_conn()
    conn.execute("""INSERT INTO relatorio_mensal
                    (data,numero_pedido,modelo,faixa,variante_faixa,tecido,
                     qtd_pecas,cor_principal,receita,custo,lucro,observacao)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                 (data, numero_pedido, modelo, faixa, variante_faixa, tecido,
                  qtd_pecas, cor_principal, receita, custo, lucro, observacao))
    conn.commit()
    conn.close()

def get_relatorio_mensal(mes=None):
    conn = get_conn()
    q = 'SELECT * FROM relatorio_mensal WHERE 1=1'
    params = []
    if mes:
        q += ' AND substr(data,1,7)=?'; params.append(mes)
    q += ' ORDER BY data DESC'
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_registro_mensal(rid, data):
    campos = ', '.join(f"{k}=?" for k in data)
    conn = get_conn()
    conn.execute(f'UPDATE relatorio_mensal SET {campos} WHERE id=?', list(data.values()) + [rid])
    conn.commit()
    conn.close()

def delete_registro_mensal(rid):
    conn = get_conn()
    conn.execute('DELETE FROM relatorio_mensal WHERE id=?', (rid,))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────
# HISTÓRICO
# ─────────────────────────────────────────
def add_historico(tipo, tecido_modelo, preco_anterior, preco_novo, fornecedor_faccionista, motivo=''):
    variacao = round((preco_novo - preco_anterior) / preco_anterior, 4) if preco_anterior else 0
    conn = get_conn()
    conn.execute("""INSERT INTO historico
                    (data,tipo,tecido_modelo,preco_anterior,preco_novo,variacao_pct,
                     fornecedor_faccionista,motivo)
                    VALUES (?,?,?,?,?,?,?,?)""",
                 (datetime.today().strftime('%Y-%m-%d'), tipo, tecido_modelo,
                  preco_anterior, preco_novo, variacao, fornecedor_faccionista, motivo))
    conn.commit()
    conn.close()

def get_historico():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM historico ORDER BY data DESC, id DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_historico(hid):
    conn = get_conn()
    conn.execute('DELETE FROM historico WHERE id=?', (hid,))
    conn.commit()
    conn.close()
