import flet as ft


def HeaderComponent(on_refresh):
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        bgcolor="#1E1E2E",
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, color="#A6E3A1", size=28),
                        ft.Text("Simple Music", size=22, weight=ft.FontWeight.BOLD, color="white"),
                    ]
                ),
                ft.IconButton(
                    icon=ft.Icons.REFRESH_ROUNDED,
                    icon_color="#89B4FA",
                    tooltip="Scan MP3",
                    on_click=on_refresh,
                ),
            ],
        ),
    )
