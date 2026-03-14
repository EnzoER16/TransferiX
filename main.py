import tkinter as tk
from utils import get_ip

window = tk.Tk()
window.title("TransferiX")
window.iconphoto(True, tk.PhotoImage(file="icon.png"))
window.geometry("500x300")
window.resizable(False, False)

ip_frame = tk.Frame(window, bg="white", relief="groove", borderwidth=1)
ip_frame.pack(side="top", fill="x", padx=5, pady=(0, 5))

my_ip = tk.Label(ip_frame, text=f"{get_ip()}", bg="white")
my_ip.pack(pady=2)

buttons_frame = tk.Frame(window)
buttons_frame.pack(side="bottom", fill="x")

receive_button = tk.Button(buttons_frame, text="Recibir archivos")
receive_button.pack()

send_button = tk.Button(buttons_frame, text="Enviar archivos")
send_button.pack()

window.mainloop()