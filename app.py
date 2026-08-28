import html
import os
import platform

from flask import Flask, Response

app = Flask(__name__)

HELLO_WORLD_PAGE = """<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <title>Hello, World</title>
</head>
<body>
  <h1>Hello, World</h1>
  <p>The underlying operating system is {operating_system}.</p>
</body>
</html>
"""


def operating_system_description() -> str:
    try:
        return platform.freedesktop_os_release()["PRETTY_NAME"]
    except OSError:
        mac_version = platform.mac_ver()[0]
        if mac_version:
            return f"macOS {mac_version}"
        return f"{platform.system()} {platform.release()}"


@app.get("/")
def hello_world():
    page = HELLO_WORLD_PAGE.format(
        operating_system=html.escape(operating_system_description())
    )
    return Response(page, mimetype="text/html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
