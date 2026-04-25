import customtkinter as ctk, utilities, uuid, socket, json, time, threading, os, struct
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

# discovery config
DEVICE_ID = str(uuid.uuid4())[:8]
DEVICE_NAME = utilities.get_model()
DISCOVERY_PORT = 53000
devices = {}
device_widgets = {}

# trasnfer config
TRANSFER_PORT = 50000
BUFFER_SIZE = 4 * 1024 * 1024
files = []
selected_ip = None

# custom tkinter with drag and drop support
class CTkDnD(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

# discovery functions

def send_udp_message(message_dict):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock: # socket udp ipv4
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        message = json.dumps(message_dict).encode()

        local_ip = utilities.get_local_ip()
        # calculate the specific broadcast for the subnetwork
        if local_ip != "0.0.0.0":
            parts = local_ip.split('.')
            broadcast_ip = f"{parts[0]}.{parts[1]}.{parts[2]}.255"
        else:
            broadcast_ip = "255.255.255.255"

        try:
            # send to calculated broadcast ip address
            sock.sendto(message, (broadcast_ip, DISCOVERY_PORT))
        except:
            pass

def send_broadcast():
    while True:
        send_udp_message({"id": DEVICE_ID, "name": DEVICE_NAME, "alive": True})
        time.sleep(2)

def receive_broadcast(on_device_add, on_device_remove):
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

            if message.get("alive") == False:
                if ip in devices:
                    name = devices[ip]["name"]
                    del devices[ip]
                    on_device_remove(ip, name)
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

def send_exit():
    send_udp_message({"id": DEVICE_ID, "name": DEVICE_NAME, "alive": False})

# transfer functions

def recv_all(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet: return None
        data.extend(packet)
    return data

def start_sending_files(device_ip):
    threading.Thread(target=send_files, args=(device_ip,), daemon=True).start()

def send_files(device_ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            client.connect((device_ip, TRANSFER_PORT))
            for file_path in files:
                file_name = os.path.basename(file_path)

                name = os.path.basename(file_path).encode()
                size = os.path.getsize(file_path)
                header = struct.pack(f"!I{len(name)}sQ", len(name), name, size)
                client.sendall(header)

                sent = 0
                start_time = time.time()
                last_update_time = start_time
                progress_bar.pack(pady=(0, 5))

                update_status_label(f"Sending: {file_name}")

                with open(file_path, "rb") as f:
                    while True:
                        chunk = f.read(BUFFER_SIZE)
                        if not chunk:
                            break
                        client.sendall(chunk)

                        sent += len(chunk)
                        progress = sent / size
                        progress_bar.after(0, lambda p=progress: progress_bar.set(p))

                        now = time.time()
                        if now - last_update_time >= 0.5:
                            elapsed = now - start_time
                            if elapsed > 0:
                                speed_mbps = (sent / (1024 * 1024)) / elapsed
                                update_status_label(f"Sending: {file_name} - {speed_mbps:.1f} MB/s")
                            last_update_time = now

                progress_bar.after(0, lambda p=progress: progress_bar.set(1))

            progress_bar.pack_forget()
            update_status_label("Files sent successfully")
    except Exception as error:
        update_status_label(error)

def start_receiving_files():
    update_status_label("Waiting for connections")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", TRANSFER_PORT))
        server.listen()
        while True:
            connection, _ = server.accept()
            threading.Thread(target=receive_files, args=(connection,), daemon=True).start()

def receive_files(connection):
    with connection:
        try:
            while True:
                header_len_raw = recv_all(connection, 4)
                if not header_len_raw: break
                
                name_len = struct.unpack("!I", header_len_raw)[0]
                name = recv_all(connection, name_len).decode()
                file_size = struct.unpack("!Q", recv_all(connection, 8))[0]

                progress_bar.pack(pady=(0, 5))
                update_status_label(f"Receiving: {name}")

                with open(name, "wb") as f:
                    remaining = file_size
                    received = 0

                    start_time = time.time()
                    last_update_time = start_time

                    while remaining > 0:
                        chunk = connection.recv(min(remaining, BUFFER_SIZE))
                        if not chunk: break
                        f.write(chunk)

                        len_chunk = len(chunk)
                        remaining -= len(chunk)

                        received += len_chunk
                        progress = received / file_size
                        progress_bar.after(0, lambda p=progress: progress_bar.set(p))

                        now = time.time()
                        if now - last_update_time >= 0.5:
                            elapsed = now - start_time
                            if elapsed > 0:
                                speed_mbps = (received / (1024 * 1024)) / elapsed
                                update_status_label(f"Receiving: {name} - {speed_mbps:.1f} MB/s")
                            last_update_time = now

                progress_bar.after(0, lambda: progress_bar.set(1))

            progress_bar.pack_forget()
            update_status_label("Files received successfully")
        except Exception as error:
            update_status_label(error)

# ui functions

def center_window():
    window.update_idletasks()

    window_width = window.winfo_width()
    window_height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    window.geometry(f"+{x_position}+{y_position}")

def update_status_label(message):
    status_label.after(0, lambda: status_label.configure(text=str(message)))

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

def on_device_add(ip, name):
    def ui():
        if ip in device_widgets:
            return

        device_button = ctk.CTkButton(devices_frame, text=f"{name} ({ip})", anchor="w", fg_color="#0B3A4B", hover_color="#005362", font=("Consolas", 15), command=lambda: select_device(ip))
        device_button.pack(fill="x", padx=(0, 5), pady=2)        
        device_widgets[ip] = device_button

    window.after(0, ui)

def on_device_remove(ip, name):
    def ui():
        if ip in device_widgets:
            device_widgets[ip].destroy()
            del device_widgets[ip]
            
    window.after(0, ui)

def on_close():
    send_exit()
    window.destroy()

def on_send_click():
    global files, selected_ip
    if not files:
        update_status_label("Select files first")
        return
    if not selected_ip:
        update_status_label("Select a device to send")
        return

    start_sending_files(selected_ip)

def select_device(ip):
    global selected_ip
    selected_ip = ip
    update_status_label(f"Device selected: {devices[ip]['name']}")
    
    for d_ip, widget in device_widgets.items():
        if d_ip == ip:
            widget.configure(fg_color="#008B8B", hover_color="#008B8B")
        else:
            widget.configure(fg_color="#0B3A4B")

# window setup
window = CTkDnD()
window.title("TransferiX")
window.iconbitmap(utilities.resource_path("assets/icon.ico"))
window.geometry("500x300")
window.resizable(False, False)
window.configure(fg_color="#0E1117")

# drag and drop
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', on_files_dropped)

# info frame
info_frame = ctk.CTkFrame(window, width=490, height=25, fg_color="transparent")
info_frame.pack()

status_label = ctk.CTkLabel(info_frame, text="", font=("Consolas", 15), text_color="white", wraplength=490)
status_label.pack(pady=(5, 0))

progress_bar = ctk.CTkProgressBar(info_frame, width=300, progress_color="#0095B0", fg_color="#0B3A4B")
progress_bar.set(0)

# frames
frame = ctk.CTkFrame(window, width=490, height=200, fg_color="transparent", border_width=2, border_color="#092E3C")
frame.pack(fill="both", expand=True, padx=5)

devices_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
devices_frame._scrollbar.configure(width=0)
devices_frame.pack(fill="both", expand=True, padx=5, pady=5)

# buttons
buttons_frame = ctk.CTkFrame(window, fg_color="transparent")
buttons_frame.pack(side="bottom", fill="x")

select_files_button = ctk.CTkButton(buttons_frame, corner_radius=10, fg_color="#092E3C", hover_color="#0B3A4B", text="Select files", font=("Consolas", 15), command=on_files_selected)
select_files_button.pack(side="left", expand=True, fill="x", padx=(5, 2.5), pady=5)

send_files_button = ctk.CTkButton(buttons_frame, corner_radius=10, fg_color="#092E3C", hover_color="#0B3A4B", text="Send files", font=("Consolas", 15), command=on_send_click)
send_files_button.pack(side="left", expand=True, fill="x", padx=(2.5, 5), pady=5)

center_window()
threading.Thread(target=send_broadcast, daemon=True).start()
threading.Thread(target=receive_broadcast, args=(on_device_add, on_device_remove), daemon=True).start()
threading.Thread(target=clean_up_devices, args=(on_device_remove,), daemon=True).start()
threading.Thread(target=start_receiving_files, daemon=True).start()

window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()