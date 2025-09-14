import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader


class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_path = urlparse(self.path).path

        if url_path == "/":
            self.send_html_file("index.html")
        elif url_path == "/message":
            self.send_html_file("message.html")
        elif url_path == "/read":
            self.send_messages_page()
        elif url_path == "/style.css":
            self.send_static_file("style.css", "text/css")
        elif url_path == "/logo.png":
            self.send_static_file("logo.png", "image/png")
        else:
            self.send_html_file("error.html", 404)

    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            # Parse form data
            data = parse_qs(post_data.decode("utf-8"))
            username = data.get("username", [""])[0]
            message = data.get("message", [""])[0]

            # Save to JSON
            self.save_message(username, message)

            # Redirect to message page
            self.send_response(302)
            self.send_header("Location", "/message")
            self.end_headers()
        else:
            self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        try:
            with open(filename, "rb") as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404)

    def send_static_file(self, filename, content_type):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

        try:
            with open(filename, "rb") as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404)

    def save_message(self, username, message):
        os.makedirs("storage", exist_ok=True)

        data = {}
        if os.path.exists("storage/data.json"):
            try:
                with open("storage/data.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                data = {}

        timestamp = str(datetime.now())
        data[timestamp] = {"username": username, "message": message}

        with open("storage/data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def send_messages_page(self):
        # Load messages from JSON
        messages = {}
        if os.path.exists("storage/data.json"):
            try:
                with open("storage/data.json", "r", encoding="utf-8") as file:
                    messages = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                messages = {}

        # Render template
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("read.html")
        html_content = template.render(messages=messages)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))


def run_server():
    server_address = ("", 3000)
    httpd = HTTPServer(server_address, WebHandler)
    print(f"Server running on port 3000...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
