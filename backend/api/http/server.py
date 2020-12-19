# coding=utf-8
# author: Lan_zhijiang
# description: http server (build by flask)
# date: 2020/12/12

from flask import Flask
from flask import request
from backend.api.http.http_handler import HttpHandler
import json
import socket

setting = json.load(open("./backend/data/json/setting.json", "r", encoding="utf-8"))
flask_app = Flask(__name__)


def get_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def run_server(class_log, setting):

    """
    启动服务器
    :return:
    """
    class_log.add_log("HttpServer: Start http server...", 1)

    try:
        if type(setting["hostIp"]) is not str:
            raise KeyError
    except KeyError:
        setting["HostIp"] = str(get_ip())
        json.dump(setting, open("./backend/data/json/setting.json", "w", encoding="utf-8"))

    global achhc
    achhc = HttpHandler(class_log, setting)

    flask_app.run(host=setting["hostIp"], port=setting["httpPort"])
    class_log.add_log("HttpServer: ServerAddr: " + setting["hostIp"] + str(setting["httpPort"]), 1)


@flask_app.route('/api', methods=["POST", "GET"])
def route_api():

    """
    处理请求到/api路径下的请求
    :return:
    """
    return json.dumps(achhc.handle_request(request.get_json(force=True)))


class HttpServer:

    def __init__(self, log, setting):

        self.log = log
        self.setting = setting

    def run_server(self):

        """
        启动服务器
        :return
        """
        run_server(self.log, self.setting)
