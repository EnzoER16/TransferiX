import socket

def get_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip if local_ip and local_ip != "127.0.0.1" else "Desconocido"