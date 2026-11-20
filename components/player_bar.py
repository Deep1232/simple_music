import flet as ft


class PlayerBarComponent:
    def __init__(self, on_prev, on_toggle, on_next):
        self.title_text = ft.Text(
            "ਕੋਈ ਗਾਣਾ ਨਹੀਂ ਚੱਲ ਰਿਹਾ",
            color="white",
            weight=ft.FontWeight.BOLD,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        self.play_btn = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED,
            icon_size=44,
            icon_color="#A6E3A1",
            on_click=on_toggle,
        )
        self.container = ft.Container(
            bgcolor="#1E1E2E",
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            border=ft.Border.only(top=ft.BorderSide(1, "#313244")),
            content=ft.Column(
                spacing=6,
                controls=[
                    self.title_text,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.SKIP_PREVIOUS_ROUNDED,
                                icon_size=34,
                                icon_color="white",
                                on_click=on_prev,
                            ),
                            self.play_btn,
                            ft.IconButton(
                                icon=ft.Icons.SKIP_NEXT_ROUNDED,
                                icon_size=34,
                                icon_color="white",
                                on_click=on_next,
                            ),
                        ],
                    ),
                ],
            ),
        )

    def update_state(self, title, is_playing):
        self.title_text.value = title
        self.play_btn.icon = (
            ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
            if is_playing
            else ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED
        )

    def build(self):
        return self.container
