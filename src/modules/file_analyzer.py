import tkinter as tk
from tkinter import messagebox, filedialog
import threading
from functools import partial
import PyPDF2
import docx
from dataclasses import dataclass

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

def load_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        document_content = ""
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            document_content += page.extract_text()
    
    return analyze_file(send_analyze_file(user_entry, chat_window, loading_label, root, pipe, document_content))

def load_docx(file_path):
    doc = docx.Document(file_path)
    document_content = ""
    for paragraph in doc.paragraphs:
        document_content += paragraph.text + "\n"

    return analyze_file(send_analyze_file(user_entry, chat_window, loading_label, root, pipe, document_content))

def upload_file(loading_label, file_path, user_entry, chat_window, root, pipe):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
    if file_path:
        file_name = file_path.split("/")[-1]
        loading_label.config(text=f"Arquivo carregado: {file_name}")
        if file_path.endswith(".pdf"):
            load_pdf(file_path)
        elif file_path.endswith(".docx"):
            load_docx(file_path)


def send_analyze_file(user_entry, chat_window, loading_label, root, pipe, document_content):
    user_input = user_entry.get("1.0", tk.END).strip()
    if user_input:
        root.update_idletasks()

        # Iniciar thread para processar a mensagem
        threading.Thread(target= partial(analyze_file, user_input, pipe, chat_window, loading_label, root)).start()

def analyze_file(user_input, pipe, chat_window, loading_label, root, document_content):

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
