import customtkinter as ctk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Configuración de la ventana principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Pokedex Mejorada")
ventana.geometry("400x500")

def obtener_datos_pokemon():
    nombre_pokemon = entrada_nombre.get().lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()

        # Obtener los datos del Pokémon
        nombre = datos['name'].capitalize()
        altura = datos['height']
        peso = datos['weight']
        tipos = ', '.join([tipo['type']['name'].capitalize() for tipo in datos['types']])

        # Mostrar los datos
        etiqueta_resultado.configure(text=f"Nombre: {nombre}\nAltura: {altura} dm\nPeso: {peso} hg\nTipo: {tipos}")

        # Obtener y mostrar la imagen del Pokémon
        url_imagen = datos['sprites']['front_default']
        imagen_respuesta = requests.get(url_imagen)
        imagen_pokemon = Image.open(BytesIO(imagen_respuesta.content))
        imagen_pokemon = imagen_pokemon.resize((150, 150), Image.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(imagen_pokemon)
        etiqueta_imagen.configure(image=imagen_tk)
        etiqueta_imagen.image = imagen_tk

    except requests.exceptions.HTTPError:
        messagebox.showerror("Error", "Pokémon no encontrado. Verifica el nombre e intenta de nuevo.")

# Etiqueta e ingreso de nombre del Pokémon
etiqueta_nombre = ctk.CTkLabel(ventana, text="Ingresa el nombre del Pokémon:")
etiqueta_nombre.pack(pady=10)

entrada_nombre = ctk.CTkEntry(ventana, width=200)
entrada_nombre.pack(pady=5)

boton_buscar = ctk.CTkButton(ventana, text="Buscar", command=obtener_datos_pokemon)
boton_buscar.pack(pady=10)

etiqueta_imagen = ctk.CTkLabel(ventana, text="")
etiqueta_imagen.pack(pady=10)

etiqueta_resultado = ctk.CTkLabel(ventana, text="", font=("Helvetica", 12))
etiqueta_resultado.pack(pady=10)

ventana.mainloop()
API