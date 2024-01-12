#!/usr/bin/python3
from urllib.request import Request, urlopen

# import HTTPError
from urllib.error import HTTPError


import http.server
import os
import socketserver


PORT = int(os.environ.get("GITNUFF_PORT", 8009))


class HeadRequest(Request):
    def get_method(self):
        return "HEAD"


class GitNuffHandler(http.server.BaseHTTPRequestHandler):
    # pylint: disable=invalid-name
    def do_GET(self):
        path = self.path
        # path segments is the path split on "/", but don't include the first empty string
        path_segments = path.split("/")[1:]

        if path == "/":
            self.do_text("Specify a repo in the URL like, /thavelick/gitnuff")
        elif len(path_segments) == 2:
            user_org, repo = path_segments
            self.do_readme(user_org, repo)
        else:
            self.do_text("Not Found", status_code=404)

    def do_readme(self, user_org, repo):
        base_github_url = f"https://github.com/{user_org}/{repo}"
        if not self.check_url_exists(base_github_url):
            self.do_text("Repo Not Found", status_code=404)
            return

        branch = None
        for possible_branch in ["main", "master"]:
            if self.check_url_exists(f"{base_github_url}/tree/{possible_branch}"):
                branch = possible_branch
                break

        if not branch:
            # couldn't figure out the branch, display a 404
            self.do_text("Primary Branch Not Found", status_code=404)

        for readme_filename in ["README.md", "README", "README.rst", "README.txt"]:
            readme_url = f"https://raw.githubusercontent.com/{user_org}/{repo}/{branch}/{readme_filename}"

            try:
                with urlopen(readme_url) as response:
                    readme_content = response.read().decode("utf-8")
            except HTTPError:
                # couldn't find the readme, try the next filename
                continue

            self.do_text(readme_content)
            return

        # couldn't find the readme, display a 404
        self.do_text("No README Found", status_code=404)

    def check_url_exists(self, url):
        try:
            request = HeadRequest(url)
            with urlopen(request):
                return True
        except HTTPError:
            return False

    def do_file(self, path, content_type):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.do_text(content, content_type)

    def do_text(self, text, content_type="text/plain", status_code=200):
        text = str.encode(text)
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", len(text))
        self.end_headers()
        self.wfile.write(text)


with socketserver.TCPServer(("", PORT), GitNuffHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
