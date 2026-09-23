#!/usr/bin/env python3
"""本地启动 1f6s Studio：在仓库根起一个 http 服务并打开浏览器。

python3 tools/serve_studio.py [端口]     # 默认 8765

走 http 而非 file:// 的原因：站内示例拉取 / Service 类 fetch 需要；
Studio 本身仍可双击 studio.html 直接用（file:// 下仅「站内示例」不可用）。
"""
import http.server
import socketserver
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


socketserver.TCPServer.allow_reuse_address = True


def main() -> int:
    import os
    os.chdir(ROOT)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://127.0.0.1:{PORT}/studio.html"
        print(f"1f6s Studio → {url}   （Ctrl+C 退出）")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
