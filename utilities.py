import platform, subprocess, os, socket, sys, pathlib

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

def get_download_directory():
    if "android" in platform.platform().lower() or "ANDROID_STORAGE" in os.environ:
        return "/storage/emulated/0/Download"
    else:
        return str(pathlib.Path.home() / "Downloads")

def generate_unique_filename(base_dir, filename):
    full_path = os.path.join(base_dir, filename)

    if not os.path.exists(full_path):
        return full_path

    name, extension = os.path.splitext(filename)
    counter = 1

    new_full_path = os.path.join(base_dir, f"{name} ({counter}){extension}")
    while os.path.exists(new_full_path):
        counter += 1
        new_full_path = os.path.join(base_dir, f"{name} ({counter}){extension}")
        
    return new_full_path