import flet as ft


class PlayerBarComponent:
    def __init__(self, on_prev, on_toggle, on_next):
        self.title_text = ft.Text(
            "ਕੋਈ ਗਾਣਾ ਨਹੀਂ ਚੱਲ ਰਿਹਾ",
            color="#F5E0DC",
            weight=ft.FontWeight.BOLD,
            size=14,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        self.subtitle_text = ft.Text(
            "ਲਿਸਟ ਵਿੱਚੋਂ ਕੋਈ MP3 ਚੁਣੋ",
            color="#A6ADC8",
            size=12,
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
            bgcolor="#181825",
            padding=ft.Padding.only(left=14, right=10, top=10, bottom=12),
            border=ft.Border.only(top=ft.BorderSide(1, "#313244")),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Row(
                        expand=True,
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=42,
                                height=42,
                                border_radius=12,
                                bgcolor="#24273A",
                                alignment=ft.alignment.Alignment.CENTER,
                                content=ft.Icon(
                                    ft.Icons.HEADPHONES_ROUNDED,
                                    color="#89B4FA",
                                    size=22,
                                ),
                            ),
                            ft.Column(
                                expand=True,
                                spacing=2,
                                controls=[self.title_text, self.subtitle_text],
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=0,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.SKIP_PREVIOUS_ROUNDED,
                                icon_size=28,
                                icon_color="#CDD6F4",
                                on_click=on_prev,
                            ),
                            self.play_btn,
                            ft.IconButton(
                                icon=ft.Icons.SKIP_NEXT_ROUNDED,
                                icon_size=28,
                                icon_color="#CDD6F4",
                                on_click=on_next,
                            ),
                        ],
                    ),
                ],
            ),
        )

    def update_state(self, title: str, folder: str, is_playing: bool):
        self.title_text.value = title
        self.subtitle_text.value = "ਚੱਲ ਰਿਹਾ ਹੈ" if is_playing else f"ਰੁਕਿਆ • {folder}"
        self.play_btn.icon = (
            ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
            if is_playing
            else ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED
        )

    def build(self):
        return self.container
