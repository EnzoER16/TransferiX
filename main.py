import tkinter as tk, os
import translation
from tkinter import filedialog, ttk
from utils import get_ip, start_sending_files, start_receiving_files

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300

files = []

def center_window(win, window_width, window_height):
    # get screen size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate positions to center
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)

    # set window size and position
    win.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

def on_send_click():
    # style
    send_button.config(relief="sunken")
    receive_button.config(relief="raised")

    # functionality
    my_ip.pack_forget()
    ip_frame.pack_forget()
    status_label.config(text=translation.translate("select_to_send"))

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
    status_label.config(text=translation.translate("waiting_files"))
    status_label.pack()
    content_frame.pack_forget()
    content_frame.pack(fill="both", expand=True, padx=5)

    # extra functionality
    select_files_button.pack_forget()
    cancel_button.pack_forget()

    text_input.pack_forget()
    confirm_send_button.pack_forget()
    accept_send_button.pack_forget()
    accept_receive_button.pack_forget()

    extra_buttons_frame.pack_forget()

def select_files():
    # open file dialog
    global files
    files = filedialog.askopenfilenames(title=translation.translate("select_files"), multiple=True)

    # ui update
    if files:
        status_label.config(text=translation.translate("files_selected") + ":\n" + " / ".join(os.path.basename(f) for f in files))
        select_files_button.pack_forget()
        cancel_button.pack(padx=5, pady=(5, 0), side="left")

        text_input.pack(padx=5, side="left")
        text_input.focus_set()
        confirm_send_button.pack(padx=5, side="left")

def cancel_selection():
    status_label.config(text=translation.translate("select_to_send"))
    cancel_button.pack_forget()
    select_files_button.pack(padx=5, pady=(5, 0))

    text_input.delete(0, tk.END)
    text_input.pack_forget() 
    confirm_send_button.pack_forget()

    accept_send_button.pack_forget()

def to_send_files():
    send_ip = text_input.get()
    paths = files

    start_sending_files(send_ip, paths, status_label, cancel_button, text_input, confirm_send_button, accept_send_button, file_progress, total_progress)

def switch_lang(language):
    translation.set_language(language)
    translation.refresh_ui()

    if hasattr(window, "settings_window") and window.settings_window.winfo_exists():
        window.settings_window.title(translation.translate("settings"))

def open_settings():
    window.settings_window = tk.Toplevel(window)
    settings = window.settings_window
    settings.attributes("-toolwindow", True)
    settings.title(translation.translate("settings"))
    settings.geometry("450x250")
    settings.resizable(False, False)

    center_window(settings, 450, 250)

    settings.language_button_image = tk.PhotoImage(file="assets/language.png")
    language_button = tk.Menubutton(settings, relief=tk.RAISED, text=translation.translate("language"), image=settings.language_button_image, compound="left")
    language_button.menu = tk.Menu(language_button, tearoff=0)
    language_button["menu"] = language_button.menu
    language_button.menu.add_command(label="English", command=lambda: switch_lang("en"))
    language_button.menu.add_command(label="Español", command=lambda: switch_lang("es"))
    translation.register_widget(language_button, "language")
    language_button.pack(pady=5)

# window configuration
window = tk.Tk()
window.title("TransferiX")
window.iconphoto(True, tk.PhotoImage(file="assets/icon.png"))
window.resizable(False, False)

# ip frame
ip_frame = tk.Frame(window, bg="white", relief="groove", borderwidth=1)
ip_frame.pack(side="top", fill="x", padx=5, pady=(0, 5))

my_ip = tk.Label(ip_frame, text=f"{get_ip()}", bg="white")
unknown_ip = tk.Label(ip_frame, text=translation.translate("unknown"), bg="white")
unknown_ip.pack(pady=2) if get_ip() is None else my_ip.pack(pady=2)

settings_button_image = tk.PhotoImage(file="assets/configuration.png")
settings_button = tk.Button(ip_frame, image=settings_button_image, command=open_settings)
settings_button.place(relx=1.0, x=-3, y=2, anchor="ne")

# content frame
content_frame = tk.Frame(window, bg="white", relief="groove", borderwidth=1)
content_frame.pack(fill="both", expand=True, padx=5)

status_label = tk.Label(content_frame, text=translation.translate("waiting_files"), bg="white", wraplength=490)
status_label.pack()

file_progress = ttk.Progressbar(content_frame, maximum=100, length=460)
total_progress = ttk.Progressbar(content_frame, maximum=100, length=460)

# extra buttons frame
extra_buttons_frame = tk.Frame(window)
extra_buttons_frame.pack()

select_files_button = tk.Button(extra_buttons_frame, text=translation.translate("select_files"), command=select_files)
cancel_button = tk.Button(extra_buttons_frame, text=translation.translate("cancel_button"), command=cancel_selection)

text_input = tk.Entry(extra_buttons_frame)
confirm_send_button = tk.Button(extra_buttons_frame, text=translation.translate("send_button"), command=to_send_files)

accept_send_button = tk.Button(extra_buttons_frame, text=translation.translate("accept"), command=cancel_selection)
accept_receive_button = tk.Button(extra_buttons_frame, text=translation.translate("accept"), command=on_receive_click)

# buttons frame
buttons_frame = tk.Frame(window)
buttons_frame.pack(side="bottom", fill="x")

receive_button = tk.Button(buttons_frame, text=translation.translate("receive_button"), relief="sunken", command=lambda: on_receive_click())
receive_button.pack(side="left", expand=True, fill="x", padx=5, pady=5)

send_button = tk.Button(buttons_frame, text=translation.translate("send_button"), command=lambda: on_send_click())
send_button.pack(side="left", expand=True, fill="x", padx=5, pady=5)

translation.register_widget(receive_button, "receive_button")
translation.register_widget(send_button, "send_button")
translation.register_widget(unknown_ip, "unknown")
translation.register_widget(status_label, "waiting_files")
translation.register_widget(select_files_button, "select_files")
translation.register_widget(cancel_button, "cancel_button")
translation.register_widget(confirm_send_button, "send_button")
translation.register_widget(accept_send_button, "accept")
translation.register_widget(accept_receive_button, "accept")

center_window(window, WINDOW_WIDTH, WINDOW_HEIGHT)

start_receiving_files(status_label, accept_receive_button, file_progress)

window.mainloop()