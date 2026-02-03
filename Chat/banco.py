import sqlite3

def conectar_db():
    return sqlite3.connect("assistente_saude.db", check_same_thread=False)

def criar_tabelas():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER UNIQUE,
        nome TEXT,
        senha TEXT,
        logado INTEGER DEFAULT 0,
        estado TEXT,
        temp TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        medicamento TEXT,
        horario TEXT
    )
    """)

    conn.commit()
    conn.close()

def criar_usuario_se_nao_existir(chat_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (chat_id) VALUES (?)",
        (chat_id,)
    )
    conn.commit()
    conn.close()

def definir_estado(chat_id, estado):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET estado = ? WHERE chat_id = ?",
        (estado, chat_id)
    )
    conn.commit()
    conn.close()

def obter_estado(chat_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT estado FROM usuarios WHERE chat_id = ?",
        (chat_id,)
    )
    r = cursor.fetchone()
    conn.close()
    return r[0] if r else None

def salvar_temp(chat_id, valor):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET temp = ? WHERE chat_id = ?",
        (valor, chat_id)
    )
    conn.commit()
    conn.close()

def obter_temp(chat_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT temp FROM usuarios WHERE chat_id = ?",
        (chat_id,)
    )
    r = cursor.fetchone()
    conn.close()
    return r[0] if r else None

def cadastrar_usuario(chat_id, nome, senha):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nome = ?, senha = ?, logado = 1, estado = NULL, temp = NULL
        WHERE chat_id = ?
    """, (nome, senha, chat_id))
    conn.commit()
    conn.close()

def usuario_logado(chat_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM usuarios WHERE chat_id = ? AND logado = 1",
        (chat_id,)
    )
    r = cursor.fetchone()
    conn.close()
    return r[0] if r else None

def cadastrar_medicamento(usuario_id, medicamento, horario):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medicamentos (usuario_id, medicamento, horario) VALUES (?, ?, ?)",
        (usuario_id, medicamento.lower(), horario)
    )
    conn.commit()
    conn.close()

def listar_medicamentos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT usuarios.chat_id, medicamentos.medicamento, medicamentos.horario
        FROM medicamentos
        JOIN usuarios ON usuarios.id = medicamentos.usuario_id
        WHERE usuarios.logado = 1
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados
