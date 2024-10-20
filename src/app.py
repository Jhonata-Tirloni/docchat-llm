import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline
from modules.message_handler import send_message
from modules.get_model import call_update_window
from functools import partial
from os import listdir


# Configuração do modelo
if len(listdir(r"../docchat-llm/src/models")) > 1: 
    modelPath = r"../docchat-llm/src/models"
    pipe = pipeline(
        "text-generation",
        model=modelPath,
        device_map='auto'
    )

else:
    pipe = ""
    tk.messagebox.showwarning(title="Atenção",
                            message="Não foi encontrado nenhum modelo na pasta /src/models.\
                                Baixe algum através da opção Menu > Atualizar na barra superior.")

# Configuração da interface Tkinter
root = tk.Tk()
root.title("docchat-llm")
root.resizable(False, False)
root.geometry("400x650")

menu_bar = tk.Menu()
analysis_menu = tk.Menu(menu_bar, tearoff=False)
analysis_menu.add_command(label="Pesquisar em documento (em desenvolvimento)",
                          accelerator="Ctrl+O",
                          command="",
                          state='disabled')
model_menu = tk.Menu(menu_bar, tearoff=False)
model_menu.add_command(label="Atualizar/baixar modelo",
                       accelerator="Ctrl+U",
                       command=partial(call_update_window, root))

chat_window = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
chat_window.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
chat_window.tag_config("blue_text", foreground="blue")

user_entry = tk.Text(root, height=3)
user_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

loading_label = tk.Label(root, text="", fg="blue")
loading_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

send_button = tk.Button(root,
                        text="Enviar mensagem",
                        command= partial(send_message,
                                         user_entry, 
                                         chat_window, 
                                         loading_label, 
                                         root,
                                         pipe))
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

menu_bar.add_cascade(menu=model_menu, label="Modelo")
menu_bar.add_cascade(menu=analysis_menu, label="Analisar")
root.config(menu=menu_bar)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_rowconfigure(0, weight=1)


root.mainloop()
