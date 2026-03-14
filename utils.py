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
    
def start_sending_files(device_ip, file_paths):
    threading.Thread(target=send_files, daemon=True, args=(device_ip, file_paths)).start()

def send_files(device_ip, file_paths):
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