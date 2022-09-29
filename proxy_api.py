# -*- coding: utf-8 -*-
# @Author: GXR
# @CreateTime: 2022-01-20
# @UpdateTime: 2022-09-29

import json
import logging
import random
import traceback

from flask import Flask

import config

app = Flask(__name__)
app.debug = False
app.logger.setLevel(logging.INFO)


# 功能列表
@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    try:
        return {
            "/get_one": "获取一个IP",
            "/get_all": "获取所有IP",
            "/get_status": "代理池状态",
            "/user_agent": "获取一个UA",
        }
    except:
        app.logger.error(traceback.format_exc())
        return {"respCode": 0, "respMsg": "服务异常", "result": {}}


# 随机获取一个可用代理
@app.route("/get_one", methods=["GET"], strict_slashes=False)
def get_one():
    try:
        proxy = json.loads(config.RED.srandmember(config.REDIS_KEY_PROXY_USEFUL))
        return {"respCode": 0, "respMsg": "成功", "result": proxy}
    except:
        app.logger.error(traceback.format_exc())
        return {"respCode": 1, "respMsg": "no proxy!", "result": {}}


# 获取所有可用代理
@app.route("/get_all", methods=["GET"], strict_slashes=False)
def get_all():
    try:
        proxy_list = []
        proxy_all = config.RED.smembers(config.REDIS_KEY_PROXY_USEFUL)
        for proxy in proxy_all:
            proxy_list.append(json.loads(proxy))
        return {"respCode": 0, "respMsg": "成功", "result": proxy_list}
    except:
        app.logger.error(traceback.format_exc())
        return {"respCode": 1, "respMsg": "no proxy!", "result": {}}


# 代理池代理数量统计
@app.route("/get_status", methods=["GET"], strict_slashes=False)
def get_status():
    try:
        status = {
            config.REDIS_KEY_PROXY_FREE: config.RED.scard(config.REDIS_KEY_PROXY_FREE),
            config.REDIS_KEY_PROXY_USEFUL: config.RED.scard(
                config.REDIS_KEY_PROXY_USEFUL
            ),
        }
        return {"respCode": 0, "respMsg": "成功", "result": status}
    except:
        app.logger.error(traceback.format_exc())
        return {"respCode": 1, "respMsg": "no status!", "result": {}}


# 随机获取一个USER_AGENT
@app.route("/user_agent", methods=["GET"], strict_slashes=False)
def user_agent():
    try:
        user_agent = random.choice(config.USER_AGENT_LIST)
        return {"respCode": 0, "respMsg": "成功", "result": user_agent}
    except:
        app.logger.error(traceback.format_exc())
        return {"respCode": 1, "respMsg": "no user_agent!", "result": {}}


# 启动服务
def run_proxy_api():
    app.run(debug=False, host=config.API_HOST, port=config.API_PORT)


if __name__ == "__main__":
    run_proxy_api()
