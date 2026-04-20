import platform, subprocess, os, socket, sys

def get_model():
    try:
        if platform.system() == "Windows":
            model = subprocess.check_output("wmic computersystem get model", shell=True)
            return model.decode().split('\n')[1].strip()
        elif platform.system() == "Linux":
            if "ANDROID_ROOT" in os.environ:
                model = subprocess.check_output("getprop ro.product.model", shell=True)
                return f"{model.decode().strip()}"
    except Exception as error:
        return error
    
def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except Exception as error:
        return "0.0.0.0"
    
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)