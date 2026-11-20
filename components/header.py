import flet as ft


def HeaderComponent(song_count: int, on_refresh, search_value: str, on_search_change):
    return ft.Container(
        bgcolor="#181825",
        padding=ft.Padding.only(left=18, right=14, top=14, bottom=12),
        border=ft.Border.only(bottom=ft.BorderSide(1, "#26263A")),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.Container(
                                    width=38,
                                    height=38,
                                    border_radius=12,
                                    bgcolor="#24273A",
                                    alignment=ft.alignment.Alignment.CENTER,
                                    content=ft.Icon(
                                        ft.Icons.LIBRARY_MUSIC_ROUNDED,
                                        color="#A6E3A1",
                                        size=22,
                                    ),
                                ),
                                ft.Column(
                                    spacing=1,
                                    controls=[
                                        ft.Text(
                                            "Simple Music",
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color="#F5E0DC",
                                        ),
                                        ft.Text(
                                            f"{song_count} MP3 ਗਾਣੇ ਉਪਲਬਧ",
                                            size=12,
                                            color="#A6ADC8",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Container(
                            bgcolor="#24273A",
                            border_radius=12,
                            content=ft.IconButton(
                                icon=ft.Icons.REFRESH_ROUNDED,
                                icon_color="#89B4FA",
                                icon_size=22,
                                tooltip="ਮੁੜ ਸਕੈਨ ਕਰੋ",
                                on_click=on_refresh,
                            ),
                        ),
                    ],
                ),
                ft.TextField(
                    value=search_value,
                    hint_text="ਗਾਣਾ ਜਾਂ ਫੋਲਡਰ ਖੋਜੋ...",
                    hint_style=ft.TextStyle(color="#6C7086", size=13),
                    text_style=ft.TextStyle(color="#CDD6F4", size=14),
                    prefix_icon=ft.Icons.SEARCH_ROUNDED,
                    bgcolor="#1E1E2E",
                    border_color="#313244",
                    focused_border_color="#89B4FA",
                    border_radius=14,
                    content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    on_change=on_search_change,
                ),
            ],
        ),
    )
