import sqlite3

DB_NAME = "tareas.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    con = get_connection()
    cur = con.cursor()

    # Tabla Usuarios
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    # Tabla Tareas (Relacionada con Usuarios)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Tareas (
        id_tarea INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        prioridad TEXT,
        usuario_id INTEGER,
        FOREIGN KEY(usuario_id) REFERENCES Usuarios(id_usuario)
    )
    """)

    con.commit()
    con.close()