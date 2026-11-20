import functools
import http.server
import os
import re
import socketserver
import threading
import urllib.parse


class _RangeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        ctype = self.guess_type(path)
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(http.HTTPStatus.NOT_FOUND, "File not found")
            return None

        fs = os.fstat(f.fileno())
        file_len = fs.st_size
        range_header = self.headers.get("Range")

        if range_header:
            match = re.match(r"bytes=(\d*)-(\d*)", range_header)
            if match:
                start_str, end_str = match.groups()
                start = int(start_str) if start_str else 0
                end = int(end_str) if end_str else file_len - 1
                if start >= file_len:
                    f.close()
                    self.send_error(http.HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                    return None
                end = min(end, file_len - 1)
                chunk_len = end - start + 1

                self.send_response(http.HTTPStatus.PARTIAL_CONTENT)
                self.send_header("Content-type", ctype)
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_len}")
                self.send_header("Content-Length", str(chunk_len))
                self.end_headers()
                f.seek(start)
                return f

        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(file_len))
        self.end_headers()
        return f

    def copyfile(self, source, outputfile):
        try:
            range_header = self.headers.get("Range")
            if range_header:
                match = re.match(r"bytes=(\d*)-(\d*)", range_header)
                if match:
                    path = self.translate_path(self.path)
                    file_len = os.path.getsize(path)
                    start_str, end_str = match.groups()
                    start = int(start_str) if start_str else 0
                    end = min(int(end_str) if end_str else file_len - 1, file_len - 1)
                    remaining = end - start + 1
                    bufsize = 64 * 1024
                    while remaining > 0:
                        data = source.read(min(bufsize, remaining))
                        if not data:
                            break
                        outputfile.write(data)
                        remaining -= len(data)
                    return
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass


class _LocalAudioServer:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self._httpd = None
        self.port = None

    def start(self) -> int:
        if self.port is not None:
            return self.port
        handler = functools.partial(_RangeHTTPRequestHandler, directory=self.root_dir)
        socketserver.TCPServer.allow_reuse_address = True
        self._httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
        self.port = self._httpd.server_address[1]
        thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        thread.start()
        return self.port


_server: _LocalAudioServer | None = None


def scan_mp3_files():
    global _server
    search_dirs = [
        "/sdcard/Music",
        "/sdcard/Download",
        "/sdcard/Audio",
        "/sdcard",
    ]
    songs = []
    seen_paths = set()

    root_for_server = "/sdcard" if os.path.isdir("/sdcard") else os.getcwd()
    if _server is None:
        _server = _LocalAudioServer(root_for_server)
    port = _server.start()

    for base_dir in search_dirs:
        if not os.path.exists(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "Android"]
            for file in files:
                if file.lower().endswith(".mp3"):
                    full_path = os.path.join(root, file)
                    if full_path not in seen_paths:
                        seen_paths.add(full_path)
                        try:
                            rel_path = os.path.relpath(full_path, root_for_server).replace("\\", "/")
                            stream_url = f"http://127.0.0.1:{port}/{urllib.parse.quote(rel_path)}"
                        except ValueError:
                            stream_url = full_path
                        songs.append(
                            {
                                "title": os.path.splitext(file)[0],
                                "path": full_path,
                                "url": stream_url,
                                "folder": os.path.basename(root),
                            }
                        )
            if base_dir == "/sdcard":
                break
    return sorted(songs, key=lambda x: x["title"].lower())
