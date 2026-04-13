import customtkinter as ctk, utilities, uuid, socket, json, time, threading
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

DEVICE_ID = str(uuid.uuid4())[:8]
DEVICE_NAME = utilities.get_model()
DISCOVERY_PORT = 53000
devices = {}
device_widgets = {}

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

def send_broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket udp ipv4
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        message = json.dumps({"id": DEVICE_ID, "name": DEVICE_NAME}).encode()
        sock.sendto(message, ("255.255.255.255", DISCOVERY_PORT)) # send global broadcast
        time.sleep(2)

def receive_broadcast(on_device_add):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", DISCOVERY_PORT)) # listen on all network interfaces

    while True:
        try:
            data, address = sock.recvfrom(1024)
            ip = address[0]
            message = json.loads(data.decode())

            if message.get("id") == DEVICE_ID:
                continue

            now = time.time()
            if ip not in devices:
                devices[ip] = {"name": message["name"], "last_seen": now}
                on_device_add(ip, message["name"])
            else:
                devices[ip]["last_seen"] = now

        except Exception:
            pass

def clean_up_devices(on_device_remove):
    while True:
        now = time.time()
        for ip in list(devices.keys()):
            if now - devices[ip]["last_seen"] > 6:
                name = devices[ip]["name"]
                del devices[ip]
                on_device_remove(ip, name)

        time.sleep(1)

def on_device_add(ip, name):
    def ui():
        if ip in device_widgets:
            return

        device_button = ctk.CTkButton(devices_frame, text=f"{name} ({ip})", anchor="w", fg_color="#0B3A4B", hover_color="#005362", font=("Consolas", 15))
        device_button.pack(fill="x", padx=5, pady=2)        
        device_widgets[ip] = device_button

    window.after(0, ui)

def on_device_remove(ip, name):
    def ui():
        if ip in device_widgets:
            device_widgets[ip].destroy()
            del device_widgets[ip]
            
    window.after(0, ui)

# window setup
window = CTkDnD()
window.title("TransferiX")
window.iconbitmap("assets/icon.ico")
window.geometry("500x300")
window.resizable(False, False)
window.configure(fg_color="#0E1117")

# drag and drop
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', on_files_dropped)

# label
status_label = ctk.CTkLabel(window, text="", font=("Consolas", 15), wraplength=490)
status_label.pack(pady=(5, 0))

# frames
frame = ctk.CTkFrame(window, width=490, height=200, fg_color="transparent", border_width=2, border_color="#092E3C")
frame.pack(fill="both", expand=True, padx=5)

devices_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
devices_frame.pack(fill="both", expand=True, padx=5, pady=5)

# buttons
buttons_frame = ctk.CTkFrame(window, fg_color="transparent")
buttons_frame.pack(side="bottom", fill="x")

select_files_button = ctk.CTkButton(buttons_frame, corner_radius=10, fg_color="#092E3C", hover_color="#0B3A4B", text="Select files", font=("Consolas", 15), command=on_files_selected)
select_files_button.pack(side="left", expand=True, fill="x", padx=(5, 2.5), pady=5)

send_files_button = ctk.CTkButton(buttons_frame, corner_radius=10, fg_color="#092E3C", hover_color="#0B3A4B", text="Send files", font=("Consolas", 15))
send_files_button.pack(side="left", expand=True, fill="x", padx=(2.5, 5), pady=5)

center_window()
threading.Thread(target=send_broadcast, daemon=True).start()
threading.Thread(target=receive_broadcast, args=(on_device_add,), daemon=True).start()
threading.Thread(target=clean_up_devices, args=(on_device_remove,), daemon=True).start()

window.mainloop()