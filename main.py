import os
import flet as ft
import flet_audio as fta
from components.header import HeaderComponent
from components.player_bar import PlayerBarComponent
from components.song_list import SongListComponent
from services.scanner import scan_mp3_files


def main(page: ft.Page):
    page.title = "Simple Music"
    page.bgcolor = "#11111B"
    page.padding = 0

    state = {
        "all_songs": [],
        "filtered_songs": [],
        "current_path": None,
        "is_playing": False,
        "search_query": "",
    }

    audio_player = fta.Audio(
        src="",
        autoplay=False,
    )
    page.overlay.append(audio_player)

    def _call_audio(method_name: str, *args):
        fn = getattr(audio_player, method_name, None)
        if callable(fn):
            res = fn(*args)
            if hasattr(res, "__await__"):
                page.run_task(lambda: res)

    def _get_filtered_songs():
        q = state["search_query"].strip().lower()
        if not q:
            return list(state["all_songs"])
        return [
            s
            for s in state["all_songs"]
            if q in s["title"].lower() or q in s["folder"].lower()
        ]

    def _refresh_ui():
        state["filtered_songs"] = _get_filtered_songs()
        header_holder.content = HeaderComponent(
            song_count=len(state["all_songs"]),
            on_refresh=load_songs,
            search_value=state["search_query"],
            on_search_change=on_search_change,
        )
        song_list.render(
            state["filtered_songs"],
            current_path=state["current_path"],
            is_playing=state["is_playing"],
        )
        page.update()

    def play_song_item(song: dict):
        if not song or not os.path.exists(song["path"]):
            return
        state["current_path"] = song["path"]
        state["is_playing"] = True
        audio_player.src = song["path"]
        audio_player.autoplay = True
        player_bar.update_state(song["title"], song["folder"], True)
        _refresh_ui()
        _call_audio("play")

    def toggle_play(e):
        if not state["filtered_songs"] and not state["all_songs"]:
            return
        pool = state["filtered_songs"] if state["filtered_songs"] else state["all_songs"]
        if state["current_path"] is None:
            play_song_item(pool[0])
            return

        current_song = next((s for s in state["all_songs"] if s["path"] == state["current_path"]), None)
        if not current_song:
            play_song_item(pool[0])
            return

        if state["is_playing"]:
            state["is_playing"] = False
            player_bar.update_state(current_song["title"], current_song["folder"], False)
            _call_audio("pause")
            _refresh_ui()
        else:
            state["is_playing"] = True
            player_bar.update_state(current_song["title"], current_song["folder"], True)
            _call_audio("resume")
            _refresh_ui()

    def _step_song(delta: int):
        pool = state["filtered_songs"] if state["filtered_songs"] else state["all_songs"]
        if not pool:
            return
        idx = next((i for i, s in enumerate(pool) if s["path"] == state["current_path"]), -1)
        next_idx = (idx + delta) % len(pool) if idx != -1 else 0
        play_song_item(pool[next_idx])

    def prev_song(e):
        _step_song(-1)

    def next_song(e):
        _step_song(1)

    def on_search_change(e):
        state["search_query"] = e.control.value or ""
        _refresh_ui()

    def load_songs(e=None):
        state["all_songs"] = scan_mp3_files()
        _refresh_ui()

    header_holder = ft.Container(
        content=HeaderComponent(
            song_count=0,
            on_refresh=load_songs,
            search_value="",
            on_search_change=on_search_change,
        )
    )
    song_list = SongListComponent(on_select_song=play_song_item, on_refresh=load_songs)
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
                header_holder,
                song_list.build(),
                player_bar.build(),
            ],
        )
    )

    load_songs()


if __name__ == "__main__":
    ft.run(main)
