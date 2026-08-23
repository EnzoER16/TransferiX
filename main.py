import flet as ft, device_info

def main(page: ft.Page):
    page.title = "TransferiX"

    my_ip = device_info.get_local_ip()

if __name__ == "__main__":
    ft.run(main)