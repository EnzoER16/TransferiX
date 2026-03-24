import socket, threading, struct, os, translation, time

TRANSFER_PORT = 50000
BUFFER_SIZE = 4096

def get_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip if local_ip and local_ip != "127.0.0.1" else None
    
def start_sending_files(device_ip, file_paths, status_label, cancel_button, text_input, confirm_send_button, accept_send_button, file_progress, total_progress, total_progress_label, speed_label):
    threading.Thread(target=send_files, daemon=True, args=(device_ip, file_paths, status_label, cancel_button, text_input, confirm_send_button, accept_send_button, file_progress, total_progress, total_progress_label, speed_label)).start()

def send_files(device_ip, file_paths, status_label, cancel_button, text_input, confirm_send_button, accept_send_button, file_progress, total_progress, total_progress_label, speed_label):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((device_ip, TRANSFER_PORT))
    client.sendall(struct.pack("!I", len(file_paths))) 

    total_size = sum(os.path.getsize(p) for p in file_paths)
    total_sent = 0

    start_time = time.time()
    last_update = start_time
    bytes_since_update = 0

    file_progress.pack(pady=5)
    total_progress_label.pack(pady=5)
    total_progress.pack(pady=5)
    speed_label.pack(pady=5)

    for file_path in file_paths:
        file_name = os.path.basename(file_path).encode()
        file_size = os.path.getsize(file_path)
        sent = 0

        client.sendall(struct.pack("!I", len(file_name)))
        client.sendall(file_name)
        client.sendall(struct.pack("!Q", file_size))
        status_label.config(text=translation.translate("sending_file") + f" {file_name.decode()}")

        with open(file_path, "rb") as f:
            while chunk := f.read(BUFFER_SIZE):
                client.sendall(chunk)

                chunk_size = len(chunk)
                sent += chunk_size
                total_sent += chunk_size
                bytes_since_update += chunk_size

                # file progress
                file_percent = (sent / file_size) * 100
                file_progress.after(0, file_progress.config, {"value": file_percent})

                # total progress
                total_percent = (total_sent / total_size) * 100
                total_progress.after(0, total_progress.config, {"value": total_percent})

                # speed
                now = time.time()
                elapsed = now - last_update

                if elapsed >= 0.5:
                    speed = bytes_since_update / elapsed
                    speed_mb = speed / (1024 * 1024)

                    speed_label.after(0, speed_label.config, {"text": f"{speed_mb:.2f} MB/s"})

                    last_update = now
                    bytes_since_update = 0

    client.close()

    # ui changes
    status_label.config(text=translation.translate("sent"))
    file_progress.pack_forget()
    total_progress_label.pack_forget()
    total_progress.pack_forget()
    cancel_button.pack_forget()
    text_input.pack_forget()
    confirm_send_button.pack_forget()
    accept_send_button.pack(padx=5, pady=(5, 0), side="left")

def start_receiving_files(status_label, accept_receive_button, file_progress):
    threading.Thread(target=receive_files, daemon=True, args=(status_label, accept_receive_button, file_progress)).start()

def receive_files(status_label, accept_receive_button, file_progress):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", TRANSFER_PORT))
    server.listen(1)

    connection, address = server.accept()
    num_files = struct.unpack("!I", connection.recv(4))[0]

    file_progress.pack(pady=5)

    for _ in range(num_files):
        name_len = struct.unpack("!I", connection.recv(4))[0]
        file_name = connection.recv(name_len).decode()
        file_size = struct.unpack("!Q", connection.recv(8))[0]

        status_label.config(text=translation.translate("receiving_file") + f" {file_name}")

        with open(file_name, "wb") as f:
            received = 0
            while received < file_size:
                data = connection.recv(min(BUFFER_SIZE, file_size - received))
                if not data:
                    break
                f.write(data)
                received += len(data)

                # file progress
                file_percent = (received / file_size) * 100
                file_progress.after(0, file_progress.config, {"value": file_percent})

    connection.close()
    server.close()

    # ui changes
    status_label.config(text=translation.translate("received"))
    accept_receive_button.pack(padx=5, pady=(5, 0), side="left")
    file_progress.pack_forget()