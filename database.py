import sqlite3

def create_connection(db_file):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Cria as tabelas no banco de dados."""
    sql_create_persona_table = """
        CREATE TABLE IF NOT EXISTS persona (
            id integer PRIMARY KEY AUTOINCREMENT,
            nome text NOT NULL,
            descricao text
        );
    """

    sql_create_historico_table = """
        CREATE TABLE IF NOT EXISTS historico (
            id integer PRIMARY KEY AUTOINCREMENT,
            persona_id integer NOT NULL,
            caminho_arquivo text NOT NULL,
            FOREIGN KEY (persona_id) REFERENCES persona (id)
        );
    """

    sql_create_palavra_chave_table = """
        CREATE TABLE IF NOT EXISTS palavra_chave (
            id integer PRIMARY KEY AUTOINCREMENT,
            palavra text NOT NULL
        );
    """

    try:
        c = conn.cursor()
        c.execute(sql_create_persona_table)
        c.execute(sql_create_historico_table)
        c.execute(sql_create_palavra_chave_table)
    except sqlite3.Error as e:
        print(e)

def create_persona(conn, persona):
    """Cria uma nova persona no banco de dados."""
    sql = """
        INSERT INTO persona(nome, descricao)
        VALUES(?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, persona)
    conn.commit()
    return cur.lastrowid

def get_persona(conn, persona_id):
    """Busca uma persona pelo ID."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM persona WHERE id=?", (persona_id,))
    return cur.fetchone()

def create_historico(conn, historico):
    """Cria um novo histórico no banco de dados."""
    sql = """
        INSERT INTO historico(persona_id, caminho_arquivo)
        VALUES(?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, historico)
    conn.commit()
    return cur.lastrowid

def get_all_palavras_chave(conn):
    """Busca todas as palavras-chave."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM palavra_chave")
    return cur.fetchall()
