# -*- coding: utf-8 -*-
# @Author: GXR
# @CreateTime: 2022-01-20
# @UpdateTime: 2022-01-20

import json
import random

import redis
from flask import Flask

import config

app = Flask(__name__)
red = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


# 功能列表
@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    return {
        "/get_one": "获取一个IP",
        "/get_all": "获取所有IP",
        "/get_status": "代理池状态",
        "/user_agent": "获取一个UA",
    }


# 随机获取一个可用代理
@app.route("/get_one", methods=["GET"], strict_slashes=False)
def get_one():
    try:
        proxy = json.loads(red.srandmember(config.REDIS_KEY_PROXY_USEFUL))
        return {"code": 0, "proxy": proxy}
    except:
        return {"code": 1, "msg": "no proxy!"}


# 获取所有可用代理
@app.route("/get_all", methods=["GET"], strict_slashes=False)
def get_all():
    try:
        proxy_list = []
        proxy_all = red.smembers(config.REDIS_KEY_PROXY_USEFUL)
        for proxy in proxy_all:
            proxy_list.append(json.loads(proxy))
        return {"code": 0, "proxy": proxy_list}
    except:
        return {"code": 1, "msg": "no proxy!"}


# 代理池代理数量统计
@app.route("/get_status", methods=["GET"], strict_slashes=False)
def get_status():
    try:
        status = {
            config.REDIS_KEY_PROXY_FREE: red.scard(config.REDIS_KEY_PROXY_FREE),
            config.REDIS_KEY_PROXY_USEFUL: red.scard(config.REDIS_KEY_PROXY_USEFUL),
        }
        return {"code": 0, "status": status}
    except:
        return {"code": 1, "msg": "no status!"}


# 随机获取一个USER_AGENT
@app.route("/user_agent", methods=["GET"], strict_slashes=False)
def user_agent():
    try:
        user_agent = random.choice(config.USER_AGENT_LIST)
        return {"code": 0, "user_agent": user_agent}
    except:
        return {"code": 1, "msg": "no user_agent!"}


# 启动服务
def run_proxy_api():
    app.run(debug=False, host=config.API_HOST, port=config.API_PORT)


if __name__ == "__main__":
    run_proxy_api()
