from db import get_connection

# ============ USUARIOS ============
def registrar_usuario(nombre, email):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO Usuarios (nombre, email) VALUES (?, ?)", (nombre, email))
    con.commit()
    con.close()

def editar_usuario(id_usuario, nombre, email):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE Usuarios SET nombre=?, email=? WHERE id_usuario=?", (nombre, email, id_usuario))
    con.commit()
    con.close()

def eliminar_usuario(id_usuario):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM Usuarios WHERE id_usuario=?", (id_usuario,))
    con.commit()
    con.close()

def obtener_usuarios():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id_usuario, nombre, email FROM Usuarios")
    datos = cur.fetchall()
    con.close()
    return datos

def existe_usuario(id_usuario):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id_usuario FROM Usuarios WHERE id_usuario = ?", (id_usuario,))
    res = cur.fetchone()
    con.close()
    return res is not None

# ============ TAREAS ============
def registrar_tarea(titulo, descripcion, prioridad, usuario_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO Tareas (titulo, descripcion, prioridad, usuario_id) VALUES (?, ?, ?, ?)",
                (titulo, descripcion, prioridad, usuario_id))
    con.commit()
    con.close()

def editar_tarea(id_tarea, titulo, descripcion, prioridad, usuario_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE Tareas SET titulo=?, descripcion=?, prioridad=?, usuario_id=? WHERE id_tarea=?",
                (titulo, descripcion, prioridad, usuario_id, id_tarea))
    con.commit()
    con.close()

def eliminar_tarea(id_tarea):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM Tareas WHERE id_tarea=?", (id_tarea,))
    con.commit()
    con.close()

def obtener_tareas():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT T.id_tarea, T.titulo, T.prioridad, U.nombre
        FROM Tareas T
        JOIN Usuarios U ON T.usuario_id = U.id_usuario
    """)
    datos = cur.fetchall()
    con.close()
    return datos

def filtrar_tareas_por_usuario(usuario_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT titulo, prioridad FROM Tareas
        WHERE usuario_id=?
    """, (usuario_id,))
    datos = cur.fetchall()
    con.close()
    return datos

def resumen_tareas_por_usuario():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT U.nombre, COUNT(T.id_tarea) 
        FROM Usuarios U
        LEFT JOIN Tareas T ON U.id_usuario = T.usuario_id
        GROUP BY U.nombre
    """)
    datos = cur.fetchall()
    con.close()
    return datos