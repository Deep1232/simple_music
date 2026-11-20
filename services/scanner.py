import os


def scan_mp3_files():
    search_dirs = [
        "/sdcard/Music",
        "/sdcard/Download",
        "/sdcard/Downloads",
        "/sdcard/Audio",
        "/sdcard/Recordings",
        "/sdcard/Podcasts",
        "/sdcard/WhatsApp/Media/WhatsApp Audio",
        "/storage/emulated/0/Music",
        "/storage/emulated/0/Download",
        "/sdcard",
    ]
    songs = []
    seen_paths = set()

    for base_dir in search_dirs:
        if not os.path.exists(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and d not in ("Android", "cache", "tmp")
            ]
            for file in files:
                if file.lower().endswith(".mp3"):
                    full_path = os.path.join(root, file)
                    real_path = os.path.realpath(full_path)
                    if real_path in seen_paths:
                        continue
                    seen_paths.add(real_path)
                    try:
                        size_mb = os.path.getsize(full_path) / (1024 * 1024)
                        size_label = f"{size_mb:.1f} MB" if size_mb >= 0.1 else ""
                    except OSError:
                        size_label = ""

                    folder_name = os.path.basename(root) or "Storage"
                    raw_title = os.path.splitext(file)[0]
                    clean_title = raw_title.replace("_", " ").replace("-", " - ").strip()
                    songs.append(
                        {
                            "title": clean_title or raw_title,
                            "path": full_path,
                            "folder": folder_name,
                            "size": size_label,
                        }
                    )
            if base_dir in ("/sdcard", "/storage/emulated/0"):
                break

    return sorted(songs, key=lambda x: x["title"].lower())
