import customtkinter as ctk
from tkinter import filedialog

def center_window():
    window.update_idletasks()

    window_width = window.winfo_width()
    window_height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    window.geometry(f"+{x_position}+{y_position}")

def update_status(text):
    status_label.configure(text=text)
    window.update_idletasks()

def select_files():
    global files
    files = filedialog.askopenfilenames(title="Select files")
    if files:
        update_status(f"{len(files)} file{'s' if len(files) != 1 else ''} selected")

window = ctk.CTk()
window.title("TransferiX")
window.iconbitmap("assets/icon.ico")
window.geometry("500x300")
window.resizable(False, False)
window.configure(fg_color="#0E1117")

status_label = ctk.CTkLabel(window, text="", font=("Consolas", 15), wraplength=490)
status_label.pack(pady=(5, 0))

frame = ctk.CTkFrame(window, width=490, height=200, fg_color="transparent", border_width=2, border_color="#005362")
frame.pack(fill="both", expand=True, padx=5)

buttons_frame = ctk.CTkFrame(window, fg_color="transparent")
buttons_frame.pack(side="bottom", fill="x")

select_files_button = ctk.CTkButton(buttons_frame, corner_radius=10, fg_color="#092E3C", hover_color="#0B3A4B", text="Select files", font=("Consolas", 15), command=select_files)
select_files_button.pack(side="left", expand=True, fill="x", padx=(5, 2.5), pady=5)

send_files_button = ctk.CTkButton(buttons_frame, corner_radius=10, fg_color="#092E3C", hover_color="#0B3A4B", text="Send files", font=("Consolas", 15))
send_files_button.pack(side="left", expand=True, fill="x", padx=(2.5, 5), pady=5)

center_window()

window.mainloop()