import flet as ft
from components.header import HeaderComponent
from components.player_bar import PlayerBarComponent
from components.song_list import SongListComponent
from services.scanner import scan_mp3_files


def main(page: ft.Page):
    page.title = "Simple Music"
    page.bgcolor = "#11111B"
    page.padding = 0

    state = {
        "songs": [],
        "current_index": -1,
        "is_playing": False,
    }

    status_text = ft.Text(
        "ਤਿਆਰ — ਗਾਣੇ 'ਤੇ ਕਲਿੱਕ ਕਰੋ",
        color="#A6ADC8",
        size=11,
        max_lines=1,
        overflow=ft.TextOverflow.ELLIPSIS,
    )

    async def _launch_song_url(song: dict):
        url = song["url"]
        try:
            res = page.launch_url(url)
            if hasattr(res, "__await__"):
                await res
            status_text.value = f"ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਚਾਲੂ: {song['title']}"
        except Exception as err:
            status_text.value = f"ਖੋਲ੍ਹਣ ਵਿੱਚ ਗਲਤੀ: {err}"
        page.update()

    def play_song(index):
        if not state["songs"] or index < 0 or index >= len(state["songs"]):
            return
        state["current_index"] = index
        state["is_playing"] = True
        song = state["songs"][index]

        status_text.value = f"ਖੋਲ੍ਹ ਰਿਹਾ ਹੈ: {song['title']}"
        player_bar.update_state(song["title"], True)
        song_list.render(state["songs"], state["current_index"])
        page.update()
        page.run_task(_launch_song_url, song)

    def toggle_play(e):
        if not state["songs"]:
            return
        if state["current_index"] == -1:
            play_song(0)
            return
        song = state["songs"][state["current_index"]]
        if state["is_playing"]:
            state["is_playing"] = False
            status_text.value = f"ਰੁਕਿਆ: {song['title']}"
            player_bar.update_state(song["title"], False)
            page.update()
        else:
            state["is_playing"] = True
            player_bar.update_state(song["title"], True)
            page.update()
            page.run_task(_launch_song_url, song)

    def open_in_browser(e):
        if not state["songs"]:
            return
        idx = state["current_index"] if state["current_index"] >= 0 else 0
        page.run_task(_launch_song_url, state["songs"][idx])

    def prev_song(e):
        if state["songs"]:
            new_idx = (state["current_index"] - 1) % len(state["songs"])
            play_song(new_idx)

    def next_song(e):
        if state["songs"]:
            new_idx = (state["current_index"] + 1) % len(state["songs"])
            play_song(new_idx)

    def load_songs(e=None):
        state["songs"] = scan_mp3_files()
        status_text.value = f"ਕੁੱਲ MP3: {len(state['songs'])}"
        song_list.render(state["songs"], state["current_index"])
        page.update()

    song_list = SongListComponent(on_select_song=play_song)
    player_bar = PlayerBarComponent(
        on_prev=prev_song,
        on_toggle=toggle_play,
        on_next=next_song,
    )

    page.add(
        ft.Column(
            expand=True,
            spacing=0,
            controls=[
                HeaderComponent(on_refresh=load_songs),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=16, vertical=6),
                    bgcolor="#181825",
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(expand=True, content=status_text),
                            ft.TextButton(
                                "ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਖੋਲ੍ਹੋ",
                                icon=ft.Icons.OPEN_IN_BROWSER,
                                on_click=open_in_browser,
                            ),
                        ],
                    ),
                ),
                song_list.build(),
                player_bar.build(),
            ],
        )
    )

    load_songs()


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550)
