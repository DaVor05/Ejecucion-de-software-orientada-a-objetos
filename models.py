class Usuario:
    def __init__(self, id_usuario, nombre, email):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email

class Tarea:
    def __init__(self, id_tarea, titulo, descripcion, prioridad, usuario_id):
        self.id_tarea = id_tarea
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.usuario_id = usuario_id