import flet as ft


class SongListComponent:
    def __init__(self, on_select_song):
        self.on_select_song = on_select_song
        self.list_view = ft.ListView(expand=True, spacing=6, padding=12)

    def render(self, songs, current_index):
        self.list_view.controls.clear()
        if not songs:
            self.list_view.controls.append(
                ft.Container(
                    padding=30,
                    alignment=ft.alignment.Alignment.CENTER,
                    content=ft.Text(
                        "ਕੋਈ MP3 ਗਾਣਾ ਨਹੀਂ ਮਿਲਿਆ।\nMusic ਜਾਂ Download ਫੋਲਡਰ ਵਿੱਚ MP3 ਰੱਖੋ।",
                        color="#CDD6F4",
                        text_align=ft.TextAlign.CENTER,
                        size=15,
                    ),
                )
            )
            return

        for idx, song in enumerate(songs):
            is_playing = idx == current_index
            self.list_view.controls.append(
                ft.Container(
                    bgcolor="#313244" if is_playing else "#181825",
                    border_radius=10,
                    padding=10,
                    on_click=lambda e, i=idx: self.on_select_song(i),
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.EQUALIZER_ROUNDED if is_playing else ft.Icons.AUDIOTRACK_ROUNDED,
                                color="#A6E3A1" if is_playing else "#89B4FA",
                            ),
                            ft.Column(
                                expand=True,
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        song["title"],
                                        color="#A6E3A1" if is_playing else "white",
                                        weight=ft.FontWeight.W_600,
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                    ft.Text(
                                        song["folder"],
                                        color="#A6ADC8",
                                        size=12,
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )

    def build(self):
        return self.list_view
