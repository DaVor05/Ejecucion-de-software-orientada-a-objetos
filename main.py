import tkinter as tk
from tkinter import messagebox, simpledialog
from crud import (
    registrar_usuario, editar_usuario, eliminar_usuario, obtener_usuarios,
    registrar_tarea, editar_tarea, eliminar_tarea, obtener_tareas,
    filtrar_tareas_por_usuario, resumen_tareas_por_usuario, existe_usuario
)
from db import init_db

# Inicializar base de datos
init_db()

# ===== Funciones auxiliares =====
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_titulo.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)
    entry_prioridad.delete(0, tk.END)
    entry_usuario_id.delete(0, tk.END)

def mostrar_usuarios_gui():
    registros = obtener_usuarios()
    lista.delete(0, tk.END)
    for r in registros:
        lista.insert(tk.END, f"ID:{r[0]} | Nombre:{r[1]} | Email:{r[2]}")

def mostrar_tareas_gui():
    registros = obtener_tareas()
    lista.delete(0, tk.END)
    for r in registros:
        lista.insert(tk.END, f"ID:{r[0]} | Tarea:{r[1]} | Prioridad:{r[2]} | Usuario:{r[3]}")

# ===== Eventos GUI de Usuarios =====
def registrar_usuario_gui():
    if entry_nombre.get() and entry_email.get():
        registrar_usuario(entry_nombre.get(), entry_email.get())
        limpiar_campos()
        mostrar_usuarios_gui()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
    else:
        messagebox.showwarning("Advertencia", "Debes ingresar nombre y correo.")

def editar_usuario_gui():
    id_usuario = simpledialog.askinteger("Editar Usuario", "Ingresa el ID exacto del usuario a editar:")
    if id_usuario:
        nombre = entry_nombre.get()
        email = entry_email.get()
        if nombre and email:
            editar_usuario(id_usuario, nombre, email)
            limpiar_campos()
            mostrar_usuarios_gui()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Llena los campos 'Nombre' y 'Email' en el formulario para actualizar.")

def eliminar_usuario_gui():
    id_usuario = simpledialog.askinteger("Eliminar Usuario", "Ingresa el ID del usuario a eliminar:")
    if id_usuario:
        eliminar_usuario(id_usuario)
        mostrar_usuarios_gui()
        messagebox.showinfo("Éxito", "Usuario eliminado.")

# ===== Eventos GUI de Tareas =====
def registrar_tarea_gui():
    titulo = entry_titulo.get().strip()
    usuario_id_str = entry_usuario_id.get().strip()
    
    if titulo and usuario_id_str.isdigit():
        usuario_id = int(usuario_id_str)
        
        # Validamos si el usuario realmente existe antes de guardar
        if not existe_usuario(usuario_id):
            messagebox.showerror("Error", f"El ID de usuario '{usuario_id}' no existe en la base de datos.")
            return
        
        registrar_tarea(titulo, entry_descripcion.get(), entry_prioridad.get(), usuario_id)
        limpiar_campos()
        mostrar_tareas_gui()
        messagebox.showinfo("Éxito", "Tarea registrada correctamente.")
    else:
        messagebox.showwarning("Advertencia", "Debes ingresar un Título y un ID de usuario numérico válido.")

def editar_tarea_gui():
    id_tarea = simpledialog.askinteger("Editar Tarea", "Ingresa el ID exacto de la tarea a editar:")
    if id_tarea:
        titulo = entry_titulo.get().strip()
        descripcion = entry_descripcion.get()
        prioridad = entry_prioridad.get()
        usuario_id_str = entry_usuario_id.get().strip()
        
        if titulo and usuario_id_str.isdigit():
            usuario_id = int(usuario_id_str)
            if not existe_usuario(usuario_id):
                messagebox.showerror("Error", f"El ID de usuario '{usuario_id}' no existe.")
                return
            
            editar_tarea(id_tarea, titulo, descripcion, prioridad, usuario_id)
            limpiar_campos()
            mostrar_tareas_gui()
            messagebox.showinfo("Éxito", "Tarea actualizada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Llena 'Título' e 'ID Usuario' numérico en el formulario para actualizar.")

def eliminar_tarea_gui():
    id_tarea = simpledialog.askinteger("Eliminar Tarea", "Ingresa el ID de la tarea a eliminar:")
    if id_tarea:
        eliminar_tarea(id_tarea)
        mostrar_tareas_gui()
        messagebox.showinfo("Éxito", "Tarea eliminada.")

def filtrar_tareas_gui():
    usuario_id_str = entry_usuario_id.get().strip()
    if not usuario_id_str.isdigit():
        messagebox.showwarning("Advertencia", "Debes ingresar un ID de usuario numérico en su campo.")
        return
    
    usuario_id = int(usuario_id_str)
    if not existe_usuario(usuario_id):
        messagebox.showwarning("Advertencia", f"El usuario con ID '{usuario_id}' no existe.")
        return

    registros = filtrar_tareas_por_usuario(usuario_id)
    lista.delete(0, tk.END)
    if not registros:
        messagebox.showinfo("Información", "El usuario no tiene tareas registradas.")
        return
        
    for r in registros:
        lista.insert(tk.END, f"Filtro - Tarea: {r[0]} | Prioridad: {r[1]}")

def resumen_tareas_gui():
    registros = resumen_tareas_por_usuario()
    lista.delete(0, tk.END)
    for r in registros:
        lista.insert(tk.END, f"Resumen - Usuario: {r[0]} | Total de tareas: {r[1]}")

# ===== Configuración de la Ventana Principal =====
ventana = tk.Tk()
ventana.title("Gestión de Usuarios y Tareas - EC0835")
ventana.geometry("700x630")

# ---- Frame Usuarios ----
frame_usuarios = tk.LabelFrame(ventana, text="Gestión de Usuarios", padx=10, pady=10)
frame_usuarios.grid(row=0, column=0, padx=10, pady=10, sticky="n")

tk.Label(frame_usuarios, text="Nombre:").grid(row=0, column=0, sticky="w")
entry_nombre = tk.Entry(frame_usuarios, width=22); entry_nombre.grid(row=0, column=1, pady=2)

tk.Label(frame_usuarios, text="Email:").grid(row=1, column=0, sticky="w")
entry_email = tk.Entry(frame_usuarios, width=22); entry_email.grid(row=1, column=1, pady=2)

tk.Button(frame_usuarios, text="Registrar Usuario", command=registrar_usuario_gui, width=20).grid(row=2, column=0, columnspan=2, pady=3)
tk.Button(frame_usuarios, text="Editar Usuario", command=editar_usuario_gui, width=20).grid(row=3, column=0, columnspan=2, pady=3)
tk.Button(frame_usuarios, text="Eliminar Usuario", command=eliminar_usuario_gui, width=20).grid(row=4, column=0, columnspan=2, pady=3)
tk.Button(frame_usuarios, text="Mostrar Usuarios", command=mostrar_usuarios_gui, width=20).grid(row=5, column=0, columnspan=2, pady=3)

# ---- Frame Tareas ----
frame_tareas = tk.LabelFrame(ventana, text="Gestión de Tareas", padx=10, pady=10)
frame_tareas.grid(row=0, column=1, padx=10, pady=10, sticky="n")

tk.Label(frame_tareas, text="Título:").grid(row=0, column=0, sticky="w")
entry_titulo = tk.Entry(frame_tareas, width=22); entry_titulo.grid(row=0, column=1, pady=2)

tk.Label(frame_tareas, text="Descripción:").grid(row=1, column=0, sticky="w")
entry_descripcion = tk.Entry(frame_tareas, width=22); entry_descripcion.grid(row=1, column=1, pady=2)

tk.Label(frame_tareas, text="Prioridad:").grid(row=2, column=0, sticky="w")
entry_prioridad = tk.Entry(frame_tareas, width=22); entry_prioridad.grid(row=2, column=1, pady=2)

tk.Label(frame_tareas, text="ID Usuario:").grid(row=3, column=0, sticky="w")
entry_usuario_id = tk.Entry(frame_tareas, width=22); entry_usuario_id.grid(row=3, column=1, pady=2)

tk.Button(frame_tareas, text="Registrar Tarea", command=registrar_tarea_gui, width=22).grid(row=4, column=0, columnspan=2, pady=2)
tk.Button(frame_tareas, text="Editar Tarea", command=editar_tarea_gui, width=22).grid(row=5, column=0, columnspan=2, pady=2)
tk.Button(frame_tareas, text="Eliminar Tarea", command=eliminar_tarea_gui, width=22).grid(row=6, column=0, columnspan=2, pady=2)
tk.Button(frame_tareas, text="Mostrar Tareas", command=mostrar_tareas_gui, width=22).grid(row=7, column=0, columnspan=2, pady=2)
tk.Button(frame_tareas, text="Filtrar por Usuario", command=filtrar_tareas_gui, width=22).grid(row=8, column=0, columnspan=2, pady=2)
tk.Button(frame_tareas, text="Resumen por Usuario", command=resumen_tareas_gui, width=22).grid(row=9, column=0, columnspan=2, pady=2)

# ---- Frame Resultados ----
frame_resultados = tk.LabelFrame(ventana, text="Resultados / Listado", padx=10, pady=10)
frame_resultados.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

lista = tk.Listbox(frame_resultados, width=105, height=11)
lista.pack()

ventana.mainloop()