import customtkinter as ctk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

class CTkDnD(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

def center_window():
    window.update_idletasks()

    window_width = window.winfo_width()
    window_height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    window.geometry(f"+{x_position}+{y_position}")

def update_status_label(text):
    status_label.configure(text=text)
    window.update_idletasks()

def handle_files_selected(selected_files):
    global files
    if selected_files:
        files = selected_files
        update_status_label(f"{len(files)} file{'s' if len(files) != 1 else ''} selected")

def on_files_selected():
    files = filedialog.askopenfilenames(title="Select files")
    handle_files_selected(files)

def on_files_dropped(event):
    files = window.tk.splitlist(event.data)
    handle_files_selected(files)

window = CTkDnD()
window.title("TransferiX")
window.iconbitmap("assets/icon.ico")
window.geometry("500x300")
window.resizable(False, False)
window.configure(fg_color="#0E1117")

window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', on_files_dropped)

status_label = ctk.CTkLabel(window, text="", font=("Consolas", 15), wraplength=490)
status_label.pack(pady=(5, 0))

frame = ctk.CTkFrame(window, width=490, height=200, fg_color="transparent", border_width=2, border_color="#005362")
frame.pack(fill="both", expand=True, padx=5)

devices_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
devices_frame.pack(fill="both", expand=True, padx=5, pady=5)

buttons_frame = ctk.CTkFrame(window, fg_color="transparent")
buttons_frame.pack(side="bottom", fill="x")

select_files_button = ctk.CTkButton(buttons_frame, corner_radius=10, fg_color="#092E3C", hover_color="#0B3A4B", text="Select files", font=("Consolas", 15), command=on_files_selected)
select_files_button.pack(side="left", expand=True, fill="x", padx=(5, 2.5), pady=5)

send_files_button = ctk.CTkButton(buttons_frame, corner_radius=10, fg_color="#092E3C", hover_color="#0B3A4B", text="Send files", font=("Consolas", 15))
send_files_button.pack(side="left", expand=True, fill="x", padx=(2.5, 5), pady=5)

center_window()

window.mainloop()