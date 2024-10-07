import tkinter as tk
from tkinter import messagebox
import threading
from functools import partial

def send_message(user_entry, chat_window, loading_label, root, pipe):
    user_input = user_entry.get("1.0", tk.END).strip()
    if user_input:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "Eu: " + user_input + "\n")
        chat_window.config(state=tk.DISABLED)
        user_entry.delete("1.0", tk.END)

        # Mostrar animação de carregamento
        loading_label.config(text="Refletindo sobre a resposta...")
        root.update_idletasks()

        # Iniciar thread para processar a mensagem
        threading.Thread(target= partial(process_message, user_input, pipe, chat_window, loading_label, root)).start()

def process_message(user_input, pipe, chat_window, loading_label, root):
    messages = [
        {
            "role": "system",
            "content": "Você se chama Rogerio, e é um excelente resolvedor de problemas e criador de raciocinio lógico. Todo problema apresentado a você é dividido em partes para seu raciocinio, e entregue da forma mais sintetizada e clara possível ao usuário."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    try:
        # Obter a resposta do modelo
        output = pipe(messages, max_new_tokens=950)
        response = output[0]["generated_text"][2]['content']

        # Mostrar a resposta no chat
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "Modelo: " + response + "\n", "blue_text")
        chat_window.config(state=tk.DISABLED)

        loading_label.config(text="")
        root.update_idletasks()

    except Exception as e:
        messagebox.showwarning("Attention, unexpected error",
                               message=str(e))
