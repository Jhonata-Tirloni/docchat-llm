import tkinter as tk
from tkinter import messagebox
import threading
from functools import partial
from file_analyzer import send_analyze_file

# Reads the config files in ../src/configs
# The model_behavior.txt contains essencial text for the app to work, remember
# to fill it! The api_consume.txt is optional
model_behavior_file = open(r"../docchat-llm/src/configs/model_behavior.txt",
                           encoding='utf-8')
model_behavior = model_behavior_file.read()
model_behavior_file.close()

api_configs_file = open(r"../docchat-llm/src/configs/api_consume.txt",
                        encoding='utf-8')
api_configs = api_configs_file.read()
api_configs_file.close()

def send_message(user_entry, chat_window, loading_label, root, pipe, analyze):
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
        if analyze is False:
            threading.Thread(target= partial(process_message, user_input, pipe, chat_window, loading_label, root)).start()
        else:
            threading.Thread(target= partial(send_analyze_file, user_input, pipe, chat_window, loading_label, root)).start()
def process_message(user_input, pipe, chat_window, loading_label, root):

    messages = [
        {
            "role": "system",
            "content": model_behavior
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
