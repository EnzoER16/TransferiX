import flet as ft, device_info

def main(page: ft.Page):
    page.title = "TransferiX"

    destination_ip = None
    files_selected = []

    async def on_submit():
        nonlocal destination_ip
        destination_ip = ip_input.value

    async def select_files():
        files = await ft.FilePicker().pick_files(dialog_title="Select files", allow_multiple=True)
        files_selected.extend(file.path for file in files)

    my_ip = device_info.get_local_ip()

    ip_input = ft.TextField(
            label="Destination IP",
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.BLUE_200,
            on_submit=on_submit)

if __name__ == "__main__":
    ft.run(main)