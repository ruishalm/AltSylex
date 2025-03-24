import sqlite3

def create_connection(db_file):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conexão com o banco de dados {db_file} estabelecida com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn

def create_tables(conn):
    """Cria as tabelas no banco de dados."""
    try:
        cursor = conn.cursor()

        # Tabela personas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT
            )
        """)

        # Tabela historicos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                persona_id INTEGER NOT NULL,
                caminho_arquivo TEXT NOT NULL,
                FOREIGN KEY (persona_id) REFERENCES personas(id)
            )
        """)

        # Tabela palavras_chave
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS palavras_chave (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                palavra TEXT NOT NULL
            )
        """)

        conn.commit()
        print("Tabelas criadas com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar as tabelas: {e}")

# Funções de CRUD para a tabela personas

def create_persona(conn, persona):
    """Cria uma nova persona."""
    sql = ''' INSERT INTO personas(nome,descricao)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, persona)
    conn.commit()
    return cur.lastrowid

def get_persona(conn, id):
    """Busca uma persona pelo ID."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM personas WHERE id=?", (id,))
    return cur.fetchone()

def get_all_personas(conn):
    """Busca todas as personas."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM personas")
    return cur.fetchall()

def update_persona(conn, persona):
    """Atualiza uma persona."""
    sql = '''
            UPDATE personas
            SET nome = ? ,
                descricao = ?
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, persona)
    conn.commit()

def delete_persona(conn, id):
    """Deleta uma persona pelo ID."""
    sql = 'DELETE FROM personas WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

# Funções de CRUD para a tabela historicos

def create_historico(conn, historico):
    """Cria um novo histórico."""
    sql = ''' INSERT INTO historicos(persona_id, caminho_arquivo)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, historico)
    conn.commit()
    return cur.lastrowid

def get_historico(conn, id):
    """Busca um histórico pelo ID."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM historicos WHERE id=?", (id,))
    return cur.fetchone()

def get_all_historicos(conn):
    """Busca todos os históricos."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM historicos")
    return cur.fetchall()

def update_historico(conn, historico):
    """Atualiza um histórico."""
    sql = '''
            UPDATE historicos
            SET persona_id = ? ,
                caminho_arquivo = ?
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, historico)
    conn.commit()

def delete_historico(conn, id):
    """Deleta um histórico pelo ID."""
    sql = 'DELETE FROM historicos WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

# Funções de CRUD para a tabela palavras_chave

def create_palavra_chave(conn, palavra_chave):
    """Cria uma nova palavra-chave."""
    sql = ''' INSERT INTO palavras_chave(palavra)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (palavra_chave,))
    conn.commit()
    return cur.lastrowid

def get_palavra_chave(conn, id):
    """Busca uma palavra-chave pelo ID."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM palavras_chave WHERE id=?", (id,))
    return cur.fetchone()

def get_all_palavras_chave(conn):
    """Busca todas as palavras-chave."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM palavras_chave")
    return cur.fetchall()

def update_palavra_chave(conn, palavra_chave):
    """Atualiza uma palavra-chave."""
    sql = '''
            UPDATE palavras_chave
            SET palavra = ?
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, palavra_chave)
    conn.commit()

def delete_palavra_chave(conn, id):
    """Deleta uma palavra-chave pelo ID."""
    sql = 'DELETE FROM palavras_chave WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

# Caminho do banco de dados
db_file = "altsylex.db"

# Criar a conexão
conn = create_connection(db_file)

# Criar as tabelas
if conn is not None:
    create_tables(conn)

# Fechar a conexão
if conn is not None:
    conn.close()
