import os
import json
import http.client
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
IP_API = os.environ.get('IP_API', '127.0.0.1')


def http_client(url):
    conn = http.client.HTTPConnection(IP_API, 8000, timeout=10)
    conn.request("GET", url)
    resp = conn.getresponse()
    body = resp.read().decode()
    conn.close()
    return body


@app.route("/", endpoint="home")
def home():
    tz = request.args.get("timezone")
    return render_template(
        "index.html",
        timezone=tz
    )


@app.route("/api/timezone", methods=['POST'], endpoint="timezone")
def timezone():
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    url = f'/timezone?latitude={latitude}&longitude={longitude}'
    body = json.loads(http_client(url))
    return redirect(url_for("home", timezone=body['timezone']))
