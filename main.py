#      <one line to give the program's name and a brief idea of what it does.>
#      Copyright (C) <2021>  <coolrc>
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import base64
import os
import platform

from flask import Flask
from flask import request, send_from_directory
from waitress import serve
import atexit

from rayso import RaySo

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/raysopic", methods=["GET"])
def capture_rayso_pic():
    content = request_parse(request)
    args = {
        "content": content.get("content"),
        "font": content.get("font"),
        "padding": parse_float(content.get("padding")),
        "title": content.get("title"),
        "size": parse_float(content.get("size")),
    }

    for k in list(args.keys()):
        if args[k] is None:
            del args[k]

    if not args["content"]:
        return {"ok": 400, "msg": "no content!", "data": None}

    args["content"] = base64.b64decode(args["content"]).decode("utf-8")

    print(args["content"] + "\n")

    global rayso

    rayso.capture_img(**args)
    return send_from_directory("./", "screenshot.png")


@app.route("/rayso", methods=["POST", "GET"])
def capture_rayso():
    content = request_parse(request)

    try:
        args = {
            "content": content.get("content"),
            "font": content.get("font"),
            "padding": parse_float(content.get("padding")),
            "title": content.get("title"),
            "size": parse_float(content.get("size")),
        }

        for k in list(args.keys()):
            if args[k] is None:
                del args[k]

        if not args["content"]:
            return {"ok": 400, "msg": "no content!", "data": None}

        args["content"] = base64.b64decode(args["content"]).decode("utf-8")

        print(args["content"] + "\n")

        global rayso

        base64_img = rayso.capture(**args)
        return {"ok": 200, "msg": "OK", "data": base64_img}

    except Exception as e:
        return {"ok": 500, "msg": format(e), "data": None}


def on_exit_app():  # 由于quit() 执行有问题，所以退出时候直接杀死浏览器进程
    sys = platform.system()
    if sys == "Windows":
        command = "taskkill /F /T /IM "
        command = command + "chromium-browser.exe"
        os.system(command)  # nosec
    else:
        command = "pkill chromedriver && pkill chromium-browser"
        os.system(command)  # nosec


def request_parse(req_data):
    """解析请求数据并以json形式返回"""
    data = {}
    if req_data.method == "POST":
        data = req_data.json
    elif req_data.method == "GET":
        data = req_data.args
    return data


def parse_float(data):
    if data is None:
        return None
    return float(data)


if __name__ == "__main__":
    print("starting...")
    rayso = RaySo()
    atexit.register(on_exit_app)
    rayso.connect()
    port = 5567
    print("running on http://127.0.0.1:" + str(port) + "/")
    serve(app, port=port)
    # # rayso.__del__()
