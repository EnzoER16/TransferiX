import tkinter as tk
from tkinter import filedialog
from utils import get_ip

window_width = 500
window_height = 300

files = []

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
    status_label.config(text="Seleccione los archivos a enviar")

    select_files_button.pack(padx=5, pady=(5, 0))

def on_receive_click():
    # style
    send_button.config(relief="raised")
    receive_button.config(relief="sunken")

    # functionality
    ip_frame.pack(side="top", fill="x", padx=5, pady=(0, 5))
    my_ip.pack()
    status_label.config(text="Esperando archivos...")
    status_label.pack()
    content_frame.pack_forget()
    content_frame.pack(fill="both", expand=True, padx=5)

    select_files_button.pack_forget()

def select_files():
    global files
    files = filedialog.askopenfilenames(title="Seleccionar archivos", multiple=True)

# window configuration
window = tk.Tk()
window.title("TransferiX")
window.iconphoto(True, tk.PhotoImage(file="icon.png"))
window.resizable(False, False)

# ip frame
ip_frame = tk.Frame(window, bg="white", relief="groove", borderwidth=1)
ip_frame.pack(side="top", fill="x", padx=5, pady=(0, 5))

my_ip = tk.Label(ip_frame, text=f"{get_ip()}", bg="white")
my_ip.pack(pady=2)

# content frame
content_frame = tk.Frame(window, bg="white", relief="groove", borderwidth=1)
content_frame.pack(fill="both", expand=True, padx=5)

status_label = tk.Label(content_frame, text="Esperando archivos...", bg="white", wraplength=490)
status_label.pack()

select_files_button = tk.Button(window, text="Seleccionar archivos", command=select_files)

# buttons frame
buttons_frame = tk.Frame(window)
buttons_frame.pack(side="bottom", fill="x")

receive_button = tk.Button(buttons_frame, text="Recibir archivos", relief="sunken", command=lambda: on_receive_click())
receive_button.pack(side="left", expand=True, fill="x", padx=5, pady=5)

send_button = tk.Button(buttons_frame, text="Enviar archivos", command=lambda: on_send_click())
send_button.pack(side="left", expand=True, fill="x", padx=5, pady=5)

center_window(window_width, window_height)

window.mainloop()