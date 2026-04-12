import platform, subprocess, os

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