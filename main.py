import tkinter as tk, os
from tkinter import filedialog
from utils import get_ip, start_sending_files, start_receiving_files

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300

files = []
language = "es"

def center_window(window_width, window_height):
    # get screen size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate positions to center
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)

    # set window size and position
    window.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

def on_send_click():
    # style
    send_button.config(relief="sunken")
    receive_button.config(relief="raised")

    # functionality
    my_ip.pack_forget()
    ip_frame.pack_forget()
    if language == "es":
        status_label.config(text="Seleccione los archivos a enviar")
    else:
        status_label.config(text="Select files to send")

    # extra functionality
    extra_buttons_frame.pack()
    select_files_button.pack(padx=5, pady=(5, 0))

def on_receive_click():
    # style
    send_button.config(relief="raised")
    receive_button.config(relief="sunken")

    # functionality
    ip_frame.pack(side="top", fill="x", padx=5, pady=(0, 5))
    my_ip.pack()
    if language == "es":
        status_label.config(text="Esperando archivos...")
    else:
        status_label.config(text="Waiting for files")
    status_label.pack()
    content_frame.pack_forget()
    content_frame.pack(fill="both", expand=True, padx=5)

    # extra functionality
    select_files_button.pack_forget()
    cancel_button.pack_forget()

    text_input.pack_forget()
    confirm_send_button.pack_forget()
    accept_receive_button.pack_forget()

    extra_buttons_frame.pack_forget()

def select_files():
    # open file dialog
    global files
    files = filedialog.askopenfilenames(title="Seleccionar archivos", multiple=True)

    # ui update
    if files:
        if language == "es":
            status_label.config(text="Archivos seleccionados:\n" + " / ".join(os.path.basename(f) for f in files))
        else:
            status_label.config(text="Files selected:\n" + " / ".join(os.path.basename(f) for f in files))
        select_files_button.pack_forget()
        cancel_button.pack(padx=5, pady=(5, 0), side="left")

        text_input.pack(padx=5, side="left")
        text_input.focus_set()
        confirm_send_button.pack(padx=5, side="left")

def cancel_selection():
    if language == "es":
        status_label.config(text="Seleccione los archivos a enviar")
    else:
        status_label.config(text="Select files to send")
    cancel_button.pack_forget()
    select_files_button.pack(padx=5, pady=(5, 0))

    text_input.delete(0, tk.END)
    text_input.pack_forget() 
    confirm_send_button.pack_forget()

    accept_send_button.pack_forget()

def to_send_files():
    send_ip = text_input.get()
    paths = files

    start_sending_files(send_ip, paths, status_label, cancel_button, text_input, confirm_send_button, accept_send_button, language)

def update_texts():
    if language == "es":
        status_label.config(text="Esperando archivos...")
        send_button.config(text="Enviar archivos")
        receive_button.config(text="Recibir archivos")
        select_files_button.config(text="Seleccionar archivos")
        cancel_button.config(text="Cancelar seleccion")
        confirm_send_button.config(text="Enviar archivos")
        accept_send_button.config(text="Aceptar")
        accept_receive_button.config(text="Aceptar")

    elif language == "en":
        status_label.config(text="Waiting for files")
        send_button.config(text="Send files")
        receive_button.config(text="Receive files")
        select_files_button.config(text="Select files")
        cancel_button.config(text="Cancel selection")
        confirm_send_button.config(text="Send files")
        accept_send_button.config(text="Accept")
        accept_receive_button.config(text="Accept")

def change_language():
    global language
    if language == "es":
        language = "en"
    else:
        language = "es"
    update_texts()

# window configuration
window = tk.Tk()
window.title("TransferiX")
window.iconphoto(True, tk.PhotoImage(file="assets/icon.png"))
window.resizable(False, False)

# ip frame
ip_frame = tk.Frame(window, bg="white", relief="groove", borderwidth=1)
ip_frame.pack(side="top", fill="x", padx=5, pady=(0, 5))

my_ip = tk.Label(ip_frame, text=f"{get_ip()}", bg="white")
my_ip.pack(pady=2)

language_button_image = tk.PhotoImage(file="assets/language.png")
language_button = tk.Button(ip_frame, image=language_button_image, command=change_language)
language_button.place(relx=1.0, x=-3, y=2, anchor="ne")

# content frame
content_frame = tk.Frame(window, bg="white", relief="groove", borderwidth=1)
content_frame.pack(fill="both", expand=True, padx=5)

status_label = tk.Label(content_frame, text="Esperando archivos...", bg="white", wraplength=490)
status_label.pack()

# extra buttons frame
extra_buttons_frame = tk.Frame(window)
extra_buttons_frame.pack()

select_files_button = tk.Button(extra_buttons_frame, text="Seleccionar archivos", command=select_files)
cancel_button = tk.Button(extra_buttons_frame, text="Cancelar seleccion", command=cancel_selection)

text_input = tk.Entry(extra_buttons_frame)
confirm_send_button = tk.Button(extra_buttons_frame, text="Enviar archivos", command=to_send_files)

accept_send_button = tk.Button(extra_buttons_frame, text="Aceptar", command=cancel_selection)
accept_receive_button = tk.Button(extra_buttons_frame, text="Aceptar", command=on_receive_click)

# buttons frame
buttons_frame = tk.Frame(window)
buttons_frame.pack(side="bottom", fill="x")

receive_button = tk.Button(buttons_frame, text="Recibir archivos", relief="sunken", command=lambda: on_receive_click())
receive_button.pack(side="left", expand=True, fill="x", padx=5, pady=5)

send_button = tk.Button(buttons_frame, text="Enviar archivos", command=lambda: on_send_click())
send_button.pack(side="left", expand=True, fill="x", padx=5, pady=5)

center_window(WINDOW_WIDTH, WINDOW_HEIGHT)

start_receiving_files(status_label, accept_receive_button, language)

window.mainloop()