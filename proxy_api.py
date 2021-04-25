# -*- coding: utf-8 -*-
# @Author: GXR
# @CreateTime: 2021-04-22

import json
import random

import redis
from flask import Flask, jsonify
from flask import Response

import config


# 返回格式统一为JSON
class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)


app = Flask(__name__)
app.response_class = JsonResponse
red = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
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
        return proxy
    except:
        return "no proxy!"


# 获取所有可用代理
@app.route("/get_all", methods=["GET"], strict_slashes=False)
def get_all():
    try:
        proxy = {"proxy_all": []}
        proxy_all = red.smembers(config.REDIS_KEY_PROXY_USEFUL)
        for i in proxy_all:
            proxy["proxy_all"].append(json.loads(i))
        return proxy
    except:
        return "no proxy!"


# 代理池代理数量统计
@app.route("/get_status", methods=["GET"], strict_slashes=False)
def get_status():
    status = {
        config.REDIS_KEY_PROXY_FREE: red.scard(config.REDIS_KEY_PROXY_FREE),
        config.REDIS_KEY_PROXY_USEFUL: red.scard(config.REDIS_KEY_PROXY_USEFUL),
    }
    return status if status else "no status!"


# 随机获取一个USER_AGENT
@app.route("/user_agent", methods=["GET"], strict_slashes=False)
def user_agent():
    user_agent = random.choice(config.USER_AGENT_LIST)
    return user_agent if user_agent else "no user_agent!"


# 启动服务
def run_proxy_api():
    app.run(debug=False, host=config.API_HOST, port=config.API_PORT)


if __name__ == "__main__":
    run_proxy_api()
