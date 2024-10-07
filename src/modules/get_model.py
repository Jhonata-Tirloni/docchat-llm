from huggingface_hub import snapshot_download, configure_http_backend
import requests
import urllib3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from functools import partial

# By default, we disable ssl verification when connecting to Huggingface hubs
# because of intranet incompatibility. If you want to enable ssl on your connection
# comment/remove the function below and comment the "configure_http_backend" invocation
# right before it.

# Disable warnings about disabling the ssl verification.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Comment/remove to enable warnings related to ssl

def backendFactory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session

configure_http_backend(backend_factory=backendFactory) # Comment/remove to enable ssl

# Script start
def confirm_update(root):
    response = messagebox.askyesno("Confirm update",
                                   "Are you sure you want to update the model? This action cannot be undone!")
    if response:
        request_auth_key(root)
    elif response is False:
        root.destroy()

def request_auth_key(root):
    auth_window = tk.Toplevel(root)
    auth_window.title("Auth Key")
    auth_window.geometry("300x150")

    label = tk.Label(auth_window,
                     text="Enter your Hugging Face Auth Key:",
                     font=("Helvetica", 12))
    label.pack(pady=10)

    auth_key_entry = tk.Entry(auth_window,
                              show="*")
    auth_key_entry.pack(pady=5)

    submit_button = tk.Button(auth_window,
                              text="Submit",
                              command= partial(start_download, auth_key_entry.get(), auth_window, root)
                            )
    submit_button.pack(pady=10)

def start_download(auth_token, auth_window, root):
    print('hi')

def download_model(auth_token, progress_window, progress_bar):
    try:
        snapshot_download(repo_id="meta-llama/Llama-3.2-1B-Instruct",
                          use_auth_token=auth_token,
                          local_dir=r'../sim-mathica/src/models')
        progress_bar.stop()
        progress_window.destroy()
        messagebox.showinfo("Success", "Model updated successfully!")
    except Exception as e:
        progress_bar.stop()
        progress_window.destroy()
        messagebox.showwarning("Attention, unexpected error",
                               message=str(e))

def call_update_window(root):
    # Obter a posição da janela principal
    x = root.winfo_x()
    y = root.winfo_y()

    new_window = tk.Toplevel(root)

    new_window.geometry(f"+{x}+{y}")

    new_window.resizable(False, False)

    info_label = tk.Label(new_window,
                        text="Attention: This action will update the Llamma model used in the application. It will download +2.5gb worth of data, and replace the model in the folder src/models.",
                        font=("Helvetica", 12),
                        wraplength=250,
                        justify="center")
    info_label.pack(pady=20)

    exit_button = tk.Button(new_window,
                            text="Update model",
                            command=partial(confirm_update, new_window))
    exit_button.pack(padx=10, pady=10)
