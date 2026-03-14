import tkinter as tk
from utils import get_ip

window = tk.Tk()
window.title("TransferiX")
window.iconphoto(True, tk.PhotoImage(file="icon.png"))
window.geometry("500x300")
window.resizable(False, False)

my_ip = tk.Label(window, text=f"{get_ip()}")
my_ip.pack()

window.mainloop()