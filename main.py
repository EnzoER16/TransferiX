import flet as ft, device_info

def main(page: ft.Page):
    page.title = "TransferiX"

    files_selected = []

    async def select_files():
        files = await ft.FilePicker().pick_files(dialog_title="Select files", allow_multiple=True)
        if files:
            for file in files:
                files_selected.append(file.path)

    my_ip = device_info.get_local_ip()

if __name__ == "__main__":
    ft.run(main)