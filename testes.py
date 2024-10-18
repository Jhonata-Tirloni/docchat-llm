import tkinter as tk
from tkinter import scrolledtext, filedialog
from transformers import pipeline
from modules.message_handler import send_message
from modules.get_model import call_update_window
from functools import partial
import PyPDF2
import docx

# Configuração do modelo
modelPath = r"../docchat-llm/src/models"
pipe = pipeline(
    "text-generation",
    model=modelPath,
    device_map='auto'
)

# Variável global para armazenar o conteúdo do documento
document_content = ""

# Função para carregar o conteúdo do arquivo PDF
def load_pdf(file_path):
    global document_content
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        document_content = ""
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            document_content += page.extract_text()

# Função para carregar o conteúdo do arquivo Word
def load_docx(file_path):
    global document_content
    doc = docx.Document(file_path)
    document_content = ""
    for paragraph in doc.paragraphs:
        document_content += paragraph.text + "\n"

# Função para abrir a janela de upload e carregar o arquivo
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
    if file_path:
        file_name = file_path.split("/")[-1]
        loading_label.config(text=f"Arquivo carregado: {file_name}")
        if file_path.endswith(".pdf"):
            load_pdf(file_path)
        elif file_path.endswith(".docx"):
            load_docx(file_path)

# Função modificada para enviar mensagem com o conteúdo do documento
def send_message_with_context(user_entry, chat_window, loading_label, root, pipe):
    user_message = user_entry.get("1.0", tk.END).strip()
    if user_message:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, f"Você: {user_message}\n", "blue_text")
        chat_window.config(state=tk.DISABLED)
        root.update_idletasks()
        
        # Adiciona o conteúdo do documento ao contexto
        context = document_content + "\n\n" + user_message
        response = pipe(context, max_length=500, num_return_sequences=1)['generated_text']
        
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, f"Modelo: {response}\n")
        chat_window.config(state=tk.DISABLED)
        root.update_idletasks()
        
        user_entry.delete("1.0", tk.END)

# Configuração da interface Tkinter
root = tk.Tk()
root.title("Rogerio")
root.resizable(False, False)
root.geometry("400x650")

menu_bar = tk.Menu()
analysis_menu = tk.Menu(menu_bar, tearoff=False)
analysis_menu.add_command(label="Pesquisar em documento",
                          accelerator="Ctrl+O",
                          command=upload_file)
model_menu = tk.Menu(menu_bar, tearoff=False)
model_menu.add_command(label="Atualizar",
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
                        command= partial(send_message_with_context,
                                         user_entry, chat_window, loading_label, root, pipe))
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

menu_bar.add_cascade(menu=model_menu, label="Modelo")
menu_bar.add_cascade(menu=analysis_menu, label="Analisar")
root.config(menu=menu_bar)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
