import tkinter as tk 
from tkinter import filedialog, scrolledtext,messagebox
import requests

API_URL = "http://127.0.0.1:8000"

# Función para analizar texto escrito por el usuario
def analyze_text():
    text = text_area.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Aviso", "Escribe algo primero.")
        return

    try:
        response = requests.post(
            f"{API_URL}/analyze-text",
            json={"text": text}
        )

        data = response.json()
        result_area.delete("1.0", tk.END)

        if "error" in data:
            result_area.insert(tk.END, data["error"])
            return

        result_area.insert(tk.END, f"Emoción dominante: {data['dominant_emotion']}\n\n")
        result_area.insert(tk.END, f"{data['summary']}\n\n")
        result_area.insert(tk.END, "Detalle por bloques:\n")

        for i, block in enumerate(data["timeline"], start=1):
            result_area.insert(
                tk.END,
                f"Bloque {i}: {block['emotion']} ({round(block['score']*100, 2)}%)\n"
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))
# Función para subir un archivo 
def upload_file():
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[
            ("Todos los soportados", "*.txt *.pdf *.docx *.xlsx"),
            ("Archivos de texto", "*.txt"),
            ("PDF", "*.pdf"),
            ("Word", "*.docx"),
            ("Excel", "*.xlsx")
        ]
    )

    if not file_path:
        return

    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{API_URL}/upload", files=files)

        data = response.json()
        result_area.delete("1.0", tk.END)

        if "error" in data:
            result_area.insert(tk.END, data["error"])
            return

        result_area.insert(tk.END, f"Emoción dominante: {data['dominant_emotion']}\n\n")
        result_area.insert(tk.END, f"{data['summary']}\n\n")
        result_area.insert(tk.END, "Detalle por bloques:\n")

        for i, block in enumerate(data["timeline"], start=1):
            result_area.insert(
                tk.END,
                f"Bloque {i}: {block['emotion']} ({round(block['score']*100, 2)}%)\n"
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))

#Ventana principal
ventana=tk.Tk()
ventana.title("Analizador Emocional")
ventana.geometry("1029x1080")

#Titulo 
titulo= tk.Label(ventana,text="Analizador de Emociones",font=("Arial",30,"bold"))
titulo.pack(pady=10)

# Cuadro de texto 
text_area=scrolledtext.ScrolledText(ventana,wrap=tk.WORD,width=80,height=15)
text_area.pack(padx=10,pady=70)

#Frame de botones 
button_frame=tk.Frame(ventana)
button_frame.pack(pady=5)

analyze_btn=tk.Button(button_frame,text="Analizar texto",width=20,command=analyze_text)

analyze_btn.grid(row=0,column=0,padx=5)

upload_btn=tk.Button(button_frame,text="Subir archivo",width=20,command=upload_file)
upload_btn.grid(row=0,column=1,padx=5)
#Area de resultados

result_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=80, height=10)
result_area.pack(padx=10, pady=10)

ventana.mainloop()
