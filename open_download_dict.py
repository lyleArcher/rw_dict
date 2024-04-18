import http.server
import os
import socketserver

PORT = 50001
DOWNLOAD_PATH = "download"


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # 处理浏览器默认的图标请求
        if self.path.__contains__("favicon.ico"):
            return os.path.join("templates", "favicon.ico")
        path = super().translate_path(path)
        relative_path = os.path.relpath(path, os.getcwd())
        # 检查路径是否在指定目录下
        if not relative_path.startswith(DOWNLOAD_PATH):
            self.send_error(403, "Forbidden")
            return None
        return path


with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
