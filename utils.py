import socket, threading, struct, os

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
        return local_ip if local_ip and local_ip != "127.0.0.1" else "Desconocido"
    
def start_sending_files(device_ip, file_paths, status_label, cancel_button, text_input, confirm_send_button, accept_send_button, language):
    threading.Thread(target=send_files, daemon=True, args=(device_ip, file_paths, status_label, cancel_button, text_input, confirm_send_button, accept_send_button, language)).start()

def send_files(device_ip, file_paths, status_label, cancel_button, text_input, confirm_send_button, accept_send_button, language):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((device_ip, TRANSFER_PORT))
    client.sendall(struct.pack("!I", len(file_paths))) 

    for file_path in file_paths:
        file_name = os.path.basename(file_path).encode()
        file_size = os.path.getsize(file_path)

        client.sendall(struct.pack("!I", len(file_name)))
        client.sendall(file_name)
        client.sendall(struct.pack("!Q", file_size))

        with open(file_path, "rb") as f:
            while chunk := f.read(BUFFER_SIZE):
                client.sendall(chunk)

    client.close()

    # ui changes
    if language == "es":
        status_label.config(text="Archivo/s enviado/s")
    else:
        status_label.config(text="File/s sended")
    cancel_button.pack_forget()
    text_input.pack_forget()
    confirm_send_button.pack_forget()
    accept_send_button.pack(padx=5, pady=(5, 0), side="left")

def start_receiving_files(status_label, accept_receive_button, language):
    threading.Thread(target=receive_files, daemon=True, args=(status_label, accept_receive_button, language)).start()

def receive_files(status_label, accept_receive_button, language):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", TRANSFER_PORT))
    server.listen(1)

    connection, address = server.accept()
    num_files = struct.unpack("!I", connection.recv(4))[0]

    for _ in range(num_files):
        name_len = struct.unpack("!I", connection.recv(4))[0]
        file_name = connection.recv(name_len).decode()
        file_size = struct.unpack("!Q", connection.recv(8))[0]

        with open(file_name, "wb") as f:
            received = 0
            while received < file_size:
                data = connection.recv(min(BUFFER_SIZE, file_size - received))
                if not data:
                    break
                f.write(data)
                received += len(data)

    connection.close()
    server.close()

    # ui changes
    if language == "es":
        status_label.config(text="Archivo/s recibido/s")
    else:
        status_label.config(text="File/s received")
    accept_receive_button.pack(padx=5, pady=(5, 0), side="left")