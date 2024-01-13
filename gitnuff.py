#!/usr/bin/python3
from collections import namedtuple
from urllib.request import Request, urlopen

from urllib.error import HTTPError

import http.server
import os
import socketserver


PORT = int(os.environ.get("GITNUFF_PORT", 8009))


class HeadRequest(Request):
    def get_method(self):
        return "HEAD"


REPO_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GitNuff - {user_org}/{repo}</title>
</head>
<body>

<pre>
<b>GitNuff - {user_org}/{repo}</b>

<a href="https://github.com/{user_org}/{repo}">View on GitHub</a>
<a href="https://codeload.github.com/thavelick/gitnuff/zip/refs/heads/{branch}">Download Zip Archive</a>
HTTP Clone URL: https://github.com/{user_org}/{repo}.git
Git Clone URL: git://github.com/{user_org}/{repo}.git
GitHub CLI: gh repo clone {user_org}/{repo}

<b>README</b>
{readme_content}
</pre>

</body>
</html>
"""

RepoInfo = namedtuple("RepoInfo", ["user_org", "repo", "branch", "readme_content"])


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
            self.do_repo_info_page(user_org, repo)
        else:
            self.do_text("Not Found", status_code=404)

    def do_repo_info_page(self, user_org, repo):
        repo_info = self.get_repo_info_by_guessing(user_org, repo)

        if not repo_info.readme_content:
            repo_info = repo_info._replace(readme_content="[No README found]")

        html = REPO_PAGE_TEMPLATE.format(**repo_info._asdict())
        self.do_text(html, content_type="text/html")

    def check_url_exists(self, url):
        try:
            request = HeadRequest(url)
            with urlopen(request):
                return True
        except HTTPError:
            return False

    def get_repo_info_by_guessing(self, user_org, repo):
        base_github_url = f"https://github.com/{user_org}/{repo}"

        branch = None
        for possible_branch in ["main", "master"]:
            if self.check_url_exists(f"{base_github_url}/tree/{possible_branch}"):
                branch = possible_branch
                break

        if not branch:
            # couldn't figure out the branch, display a 404
            self.do_text("Primary Branch Not Found", status_code=404)

        readme_content = None
        for readme_filename in ["README.md", "README", "README.rst", "README.txt"]:
            readme_url = f"https://raw.githubusercontent.com/{user_org}/{repo}/{branch}/{readme_filename}"

            try:
                with urlopen(readme_url) as response:
                    readme_content = response.read().decode("utf-8")
            except HTTPError:
                # couldn't find the readme, try the next filename
                continue

        return RepoInfo(user_org, repo, branch, readme_content)

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
