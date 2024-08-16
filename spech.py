import webbrowser
import pyautogui    
from time import sleep
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import messagebox, PhotoImage, ttk

# Inicialización de voz
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen(microphone_index):
    rec = ""  # Valor predeterminado
    try:
        with sr.Microphone(device_index=microphone_index) as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language='es-ES')
            rec = rec.lower()
    except sr.UnknownValueError:
        talk("No entendí lo que dijiste. Por favor intenta de nuevo.")
    except sr.RequestError as e:
        talk(f"No se pudo conectar al servicio de reconocimiento de voz; {e}")
    return rec

def run_mike():
    microphone_index = microphone_combobox.current()
    talk("¿Qué video quieres buscar en YouTube?")
    rec = listen(microphone_index)
    if rec:
        talk(f"Buscando {rec} en YouTube.")
        webbrowser.open("https://www.youtube.com/results?search_query=" + str(rec))
    else:
        talk("No se detectó ningún comando de búsqueda. Por favor intenta de nuevo.")

def on_button_click():
    try:
        run_mike()
        messagebox.showinfo("Éxito", "Búsqueda realizada con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def setup_audio_devices():
    # Configuración de dispositivos de entrada
    devices = sr.Microphone.list_microphone_names()
    microphone_combobox['values'] = devices
    if devices:
        microphone_combobox.current(0)  # Seleccionar el primer micrófono por defecto

# Configuración de la ventana principal
root = tk.Tk()
root.title("Asistente Virtual de Búsqueda de Videos")
root.geometry("400x300")
root.configure(bg='#f0f0f0')  # Color de fondo

# Cargar ícono de micrófono
microphone_icon = PhotoImage(file="microfono.png")  # Asegúrate de que la imagen esté en el directorio adecuado

frame = tk.Frame(root, bg='#ffffff', padx=20, pady=20, borderwidth=2, relief="groove")
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

label = tk.Label(frame, text="Presiona el ícono para buscar por voz.", font=('Arial', 12), bg='#ffffff')
label.pack(pady=10)

button = tk.Button(frame, image=microphone_icon, command=on_button_click, bd=0, relief="flat")
button.pack(pady=10)

# Configuración de dispositivos de entrada
microphone_label = tk.Label(frame, text="Selecciona el micrófono:", font=('Arial', 10), bg='#ffffff')
microphone_label.pack(pady=5)

microphone_combobox = ttk.Combobox(frame)
microphone_combobox.pack(pady=5, fill=tk.X)
setup_audio_devices()

root.mainloop()
