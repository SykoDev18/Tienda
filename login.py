import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import subprocess
import json
import os

# Crear ventana principal con tema
root = ttk.Window(themename='flatly')
root.title('Punto de Venta - Login/Registro')
root.geometry("400x400")
root.iconbitmap("gg.ico")

# Variables de usuarios en archivo JSON
users_db_file = "users_db.json"

# Cargar o crear el archivo de usuarios
if not os.path.exists(users_db_file):
    with open(users_db_file, "w") as file:
        json.dump({}, file)

# Función para iniciar sesión
def iniciar_sesion():
    cuenta = cuenta_entry.get()
    contrasena = contrasena_entry.get()

    with open(users_db_file, "r") as file:
        usuarios = json.load(file)

    if cuenta in usuarios and usuarios[cuenta] == contrasena:
        Messagebox.show_info("Inicio de sesión exitoso", "Éxito")
        root.destroy()
        subprocess.Popen(["python", "main.py"])
    else:
        Messagebox.show_error("Cuenta o contraseña incorrecta", "Error")

# Función para registrarse
def registrar_usuario():
    cuenta = cuenta_entry.get()
    contrasena = contrasena_entry.get()

    with open(users_db_file, "r") as file:
        usuarios = json.load(file)

    if cuenta in usuarios:
        Messagebox.show_error("La cuenta ya existe", "Error")
    else:
        usuarios[cuenta] = contrasena
        with open(users_db_file, "w") as file:
            json.dump(usuarios, file)
        Messagebox.show_info("Registro exitoso. Ahora puedes iniciar sesión.", "Éxito")

# Configurar interfaz de login y registro
frame = ttk.Frame(root, padding=20)
frame.pack(fill=BOTH, expand=True)

# Título
titulo_label = ttk.Label(frame, text="Bienvenido", font=("Helvetica", 20))
titulo_label.pack(pady=10)

# Imagen (opcional)
try:
    candado_img = Image.open("Hehe.png").resize((80, 80))
    candado_photo = ImageTk.PhotoImage(candado_img)
    imagen_label = ttk.Label(frame, image=candado_photo)
    imagen_label.pack(pady=10)
except Exception as e:
    print(f"No se pudo cargar la imagen: {e}")

# Campo de entrada para Cuenta
cuenta_label = ttk.Label(frame, text="Cuenta:")
cuenta_label.pack(anchor=W)
cuenta_entry = ttk.Entry(frame)
cuenta_entry.pack(fill=X, pady=5)

# Campo de entrada para Contraseña
contrasena_label = ttk.Label(frame, text="Contraseña:")
contrasena_label.pack(anchor=W)
contrasena_entry = ttk.Entry(frame, show="*")
contrasena_entry.pack(fill=X, pady=5)

# Frame para los botones
button_frame = ttk.Frame(frame)
button_frame.pack(fill=X, pady=10)

iniciar_button = ttk.Button(button_frame, text="Iniciar Sesión", command=iniciar_sesion, bootstyle="primary")
iniciar_button.pack(side=LEFT, expand=True, fill=X, padx=5)

registrar_button = ttk.Button(button_frame, text="Registrar", command=registrar_usuario, bootstyle="success")
registrar_button.pack(side=LEFT, expand=True, fill=X, padx=5)

root.mainloop()
