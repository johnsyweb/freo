import os

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
</body>
</html>
"""


@app.get("/")
def hello_world():
    return Response(HELLO_WORLD_PAGE, mimetype="text/html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
