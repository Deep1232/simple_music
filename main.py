import os
import flet as ft
from components.header import HeaderComponent
from components.player_bar import PlayerBarComponent
from components.song_list import SongListComponent
from services.scanner import scan_mp3_files

try:
    import flet_audio as fta
except Exception:
    fta = None

try:
    import flet_permission_handler as fph
except Exception:
    fph = None


def _request_android_storage_permissions(page: ft.Page, perm_handler=None):
    perms = [
        "android.permission.READ_MEDIA_AUDIO",
        "android.permission.READ_EXTERNAL_STORAGE",
    ]

    if perm_handler is not None:
        for method_name in ("request_permission", "request_permissions"):
            fn = getattr(perm_handler, method_name, None)
            if callable(fn):
                try:
                    res = fn(perms if method_name == "request_permissions" else perms[0])
                    if hasattr(res, "__await__"):
                        page.run_task(lambda r=res: r)
                    return
                except Exception:
                    pass

    if hasattr(page, "request_permission"):
        for p in perms:
            try:
                res = page.request_permission(p)
                if hasattr(res, "__await__"):
                    page.run_task(lambda r=res: r)
            except Exception:
                pass
    elif hasattr(page, "request_permissions"):
        try:
            res = page.request_permissions(perms)
            if hasattr(res, "__await__"):
                page.run_task(lambda r=res: r)
        except Exception:
            pass


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
        "menu_open": False,
        "active_filter": "all",
    }

    perm_handler = None
    if fph is not None:
        for cls_name in ("PermissionHandler",):
            cls = getattr(fph, cls_name, None)
            if callable(cls):
                try:
                    perm_handler = cls()
                    if hasattr(page, "overlay") and isinstance(page.overlay, list):
                        page.overlay.append(perm_handler)
                    break
                except Exception:
                    perm_handler = None

    audio_player = None
    if fta is not None and hasattr(fta, "Audio"):
        try:
            audio_player = fta.Audio(src="", autoplay=False)
        except Exception:
            audio_player = None

    def _call_audio(method_name: str, *args):
        if audio_player is None:
            return
        fn = getattr(audio_player, method_name, None)
        if callable(fn):
            try:
                res = fn(*args)
                if hasattr(res, "__await__"):
                    page.run_task(lambda: res)
            except Exception:
                pass

    def _get_filtered_songs():
        q = state["search_query"].strip().lower()
        base = list(state["all_songs"])
        if state["active_filter"] == "downloads":
            base = [s for s in base if "download" in s["folder"].lower()]
        elif state["active_filter"] == "music":
            base = [s for s in base if "music" in s["folder"].lower()]
        if not q:
            return base
        return [
            s
            for s in base
            if q in s["title"].lower() or q in s["folder"].lower()
        ]

    def _menu_item(icon, label, badge_text="", active=False, on_tap=None):
        return ft.Container(
            bgcolor="#24273A" if active else "transparent",
            border_radius=12,
            border=ft.Border.all(1, "#45475A" if active else "transparent"),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            on_click=on_tap,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=12,
                        controls=[
                            ft.Icon(
                                icon,
                                color="#A6E3A1" if active else "#89B4FA",
                                size=20,
                            ),
                            ft.Text(
                                label,
                                color="#F5E0DC" if active else "#CDD6F4",
                                size=14,
                                weight=ft.FontWeight.W_600 if active else ft.FontWeight.W_500,
                            ),
                        ],
                    ),
                    ft.Text(
                        badge_text,
                        color="#A6ADC8",
                        size=12,
                    ),
                ],
            ),
        )

    def _build_drawer_overlay():
        if not state["menu_open"]:
            return ft.Container(visible=False)

        def close_menu(e=None):
            state["menu_open"] = False
            _refresh_ui()

        def select_filter(mode):
            def _handler(e):
                state["active_filter"] = mode
                state["menu_open"] = False
                _refresh_ui()
            return _handler

        def clear_search_and_close(e):
            state["search_query"] = ""
            state["active_filter"] = "all"
            state["menu_open"] = False
            _refresh_ui()

        def request_perms_and_scan(e):
            state["menu_open"] = False
            _request_android_storage_permissions(page, perm_handler)
            load_songs(e)

        def scan_and_close(e):
            state["menu_open"] = False
            load_songs(e)

        drawer_panel = ft.Container(
            width=285,
            bgcolor="#181825",
            border=ft.Border.only(right=ft.BorderSide(1, "#313244")),
            padding=ft.Padding.only(left=16, right=16, top=18, bottom=24),
            content=ft.Column(
                expand=True,
                spacing=10,
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
                                            ft.Icons.MUSIC_NOTE_ROUNDED,
                                            color="#A6E3A1",
                                            size=22,
                                        ),
                                    ),
                                    ft.Column(
                                        spacing=1,
                                        controls=[
                                            ft.Text(
                                                "Simple Music",
                                                size=17,
                                                weight=ft.FontWeight.BOLD,
                                                color="#F5E0DC",
                                            ),
                                            ft.Text(
                                                "Features & Library",
                                                size=11,
                                                color="#A6ADC8",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE_ROUNDED,
                                icon_color="#CDD6F4",
                                on_click=close_menu,
                            ),
                        ],
                    ),
                    ft.Divider(color="#26263A", height=10),
                    ft.Text("LIBRARY", size=11, color="#9399B2", weight=ft.FontWeight.BOLD),
                    _menu_item(
                        ft.Icons.QUEUE_MUSIC_ROUNDED,
                        "All Songs",
                        str(len(state["all_songs"])),
                        active=state["active_filter"] == "all",
                        on_tap=select_filter("all"),
                    ),
                    _menu_item(
                        ft.Icons.ALBUM_ROUNDED,
                        "Music Folder",
                        active=state["active_filter"] == "music",
                        on_tap=select_filter("music"),
                    ),
                    _menu_item(
                        ft.Icons.DOWNLOAD_ROUNDED,
                        "Download Folder",
                        active=state["active_filter"] == "downloads",
                        on_tap=select_filter("downloads"),
                    ),
                    ft.Divider(color="#26263A", height=10),
                    ft.Text("ACTIONS", size=11, color="#9399B2", weight=ft.FontWeight.BOLD),
                    _menu_item(
                        ft.Icons.LOCK_OPEN_ROUNDED,
                        "Request Audio Permission",
                        on_tap=request_perms_and_scan,
                    ),
                    _menu_item(
                        ft.Icons.REFRESH_ROUNDED,
                        "Rescan Songs",
                        on_tap=scan_and_close,
                    ),
                    _menu_item(
                        ft.Icons.CLEAR_ALL_ROUNDED,
                        "Clear Search & Filter",
                        on_tap=clear_search_and_close,
                    ),
                    ft.Container(expand=True),
                    ft.Container(
                        bgcolor="#24273A",
                        border_radius=12,
                        padding=12,
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(
                                    "Auto Scan & Audio Player",
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color="#A6E3A1",
                                ),
                                ft.Text(
                                    "Scans Music, Download, and audio folders for MP3 files.",
                                    size=11,
                                    color="#A6ADC8",
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

        return ft.Container(
            expand=True,
            bgcolor="#99000000",
            content=ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    drawer_panel,
                    ft.Container(expand=True, on_click=close_menu),
                ],
            ),
        )

    def _refresh_ui():
        state["filtered_songs"] = _get_filtered_songs()
        header_holder.content = HeaderComponent(
            song_count=len(state["all_songs"]),
            on_menu_click=toggle_menu,
            on_refresh=load_songs,
            search_value=state["search_query"],
            on_search_change=on_search_change,
        )
        song_list.render(
            state["filtered_songs"],
            current_path=state["current_path"],
            is_playing=state["is_playing"],
        )
        drawer_holder.content = _build_drawer_overlay()
        page.update()

    def toggle_menu(e=None):
        state["menu_open"] = not state["menu_open"]
        _refresh_ui()

    def play_song_item(song: dict):
        if not song or not os.path.exists(song["path"]):
            return
        state["current_path"] = song["path"]
        state["is_playing"] = True
        if audio_player is not None:
            audio_player.src = song["path"]
            audio_player.autoplay = True
        player_bar.update_state(song["title"], song["folder"], True)
        _refresh_ui()
        _call_audio("play")

    def toggle_play(e):
        pool = state["filtered_songs"] if state["filtered_songs"] else state["all_songs"]
        if not pool:
            return
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
            on_menu_click=toggle_menu,
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
    drawer_holder = ft.Container(expand=True, visible=False)

    main_layout = ft.SafeArea(
        expand=True,
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        header_holder,
                        song_list.build(),
                        player_bar.build(),
                    ],
                ),
                drawer_holder,
            ],
        ),
    )

    def _sync_drawer_visibility():
        drawer_holder.visible = state["menu_open"]

    orig_refresh = _refresh_ui

    def _refresh_with_drawer():
        orig_refresh()
        _sync_drawer_visibility()
        page.update()

    _refresh_ui = _refresh_with_drawer

    page.add(main_layout)
    _request_android_storage_permissions(page, perm_handler)
    load_songs()


if __name__ == "__main__":
    ft.run(main)
