import flet as ft


class SongListComponent:
    def __init__(self, on_select_song, on_refresh=None):
        self.on_select_song = on_select_song
        self.on_refresh = on_refresh
        self.list_view = ft.ListView(
            expand=True,
            spacing=8,
            padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        )

    def render(self, songs, current_path=None, is_playing=False):
        self.list_view.controls.clear()

        if not songs:
            self.list_view.controls.append(
                ft.Container(
                    padding=36,
                    margin=ft.Margin.only(top=24),
                    bgcolor="#181825",
                    border_radius=18,
                    border=ft.Border.all(1, "#26263A"),
                    alignment=ft.alignment.Alignment.CENTER,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.Container(
                                width=56,
                                height=56,
                                border_radius=28,
                                bgcolor="#24273A",
                                alignment=ft.alignment.Alignment.CENTER,
                                content=ft.Icon(
                                    ft.Icons.QUEUE_MUSIC_ROUNDED,
                                    color="#89B4FA",
                                    size=30,
                                ),
                            ),
                            ft.Text(
                                "ਕੋਈ MP3 ਗਾਣਾ ਨਹੀਂ ਮਿਲਿਆ",
                                color="#F5E0DC",
                                weight=ft.FontWeight.BOLD,
                                size=16,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Music ਜਾਂ Download ਫੋਲਡਰ ਵਿੱਚ MP3 ਫਾਈਲਾਂ ਰੱਖੋ ਅਤੇ ਸਟੋਰੇਜ ਪਰਮਿਸ਼ਨ ਚੈੱਕ ਕਰੋ।",
                                color="#A6ADC8",
                                size=13,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Button(
                                content=ft.Row(
                                    tight=True,
                                    spacing=8,
                                    controls=[
                                        ft.Icon(ft.Icons.REFRESH_ROUNDED, color="#11111B", size=18),
                                        ft.Text("ਮੁੜ ਸਕੈਨ ਕਰੋ", color="#11111B", weight=ft.FontWeight.W_600),
                                    ],
                                ),
                                bgcolor="#89B4FA",
                                on_click=self.on_refresh,
                            ),
                        ],
                    ),
                )
            )
            return

        for song in songs:
            is_current = current_path is not None and song["path"] == current_path
            active_playing = is_current and is_playing
            subtitle_parts = [song["folder"]]
            if song.get("size"):
                subtitle_parts.append(song["size"])
            subtitle_text = " • ".join(subtitle_parts)

            self.list_view.controls.append(
                ft.Container(
                    bgcolor="#24273A" if is_current else "#181825",
                    border_radius=14,
                    border=ft.Border.all(
                        1, "#A6E3A1" if active_playing else ("#45475A" if is_current else "#26263A")
                    ),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                    on_click=lambda e, s=song: self.on_select_song(s),
                    content=ft.Row(
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=42,
                                height=42,
                                border_radius=12,
                                bgcolor="#1E1E2E",
                                alignment=ft.alignment.Alignment.CENTER,
                                content=ft.Icon(
                                    ft.Icons.GRAPHIC_EQ_ROUNDED
                                    if active_playing
                                    else (ft.Icons.AUDIOTRACK_ROUNDED if is_current else ft.Icons.MUSIC_NOTE_ROUNDED),
                                    color="#A6E3A1" if is_current else "#89B4FA",
                                    size=22,
                                ),
                            ),
                            ft.Column(
                                expand=True,
                                spacing=3,
                                controls=[
                                    ft.Text(
                                        song["title"],
                                        color="#A6E3A1" if is_current else "#CDD6F4",
                                        weight=ft.FontWeight.W_600 if is_current else ft.FontWeight.W_500,
                                        size=14,
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                    ft.Text(
                                        subtitle_text,
                                        color="#9399B2",
                                        size=12,
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                ],
                            ),
                            ft.Icon(
                                ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
                                if active_playing
                                else (ft.Icons.PLAY_CIRCLE_OUTLINE_ROUNDED if is_current else ft.Icons.CHEVRON_RIGHT_ROUNDED),
                                color="#A6E3A1" if is_current else "#6C7086",
                                size=24,
                            ),
                        ],
                    ),
                )
            )

    def build(self):
        return self.list_view
