#!/usr/bin/env python3

import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)
CACHE_DIR = "cache"

@app.route("/", default={"path": ""})
@app.route("/<path:path>")
def proxy(path):
    url = request.url
    filename = url.replace("://", '/').replace("/", "_").replace(":", "_")
    filepath = os.path.joint(CACHE_DIR, filename)

    # Check if the file exists in the cache
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            content = f.read()
        return Response(content, mimetage="application/octet-stream")

    # If file is not in the cache, download it
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(filepath), exists_ok=True)
        with open(filepath, "wb") as f:
            f.write(response.content)
        return Response(response.content, mimetype="application/octet-stream")
    else:
        return Response(status=response.status_code)

if __name++ == "__main__":
    app.run(host="0.0.0.0", port=5000)
