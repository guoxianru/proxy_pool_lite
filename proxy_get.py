# -*- coding: utf-8 -*-
# @Author: GXR
# @CreateTime: 2022-01-20
# @UpdateTime: 2022-09-29

import re
import threading
import time

import requests

import config
from proxy_api import app

"""
    代理格式：127.0.0.1:8888
"""


def freeproxy_89():
    """
    89代理
    https://www.89ip.cn/
    """
    try:
        response = requests.get(
            "http://api.89ip.cn/tqdl.html?api=1&num=3000&port=&address=&isp=",
            headers=config.HEADERS,
            timeout=5,
        )
        time.sleep(1)
        data = re.findall("(\d+).(\d+).(\d+).(\d+):(\d+)", response.text, re.S)
        with config.RED.pipeline(transaction=False) as p:
            for ip in data:
                proxy = ".".join(ip[:-1]) + ":" + str(ip[-1])
                p.sadd(config.REDIS_KEY_PROXY_FREE, proxy)
            p.execute()
        app.logger.info("[获取代理成功]-[89代理]-[%s]" % len(data))
    except:
        app.logger.error("[获取代理异常]-[89代理]")


def freeproxy_yun():
    """
    云代理
    http://www.ip3366.net/free/
    """
    try:
        url_list = [
            "http://www.ip3366.net/free/?stype=1&page=",
            "http://www.ip3366.net/free/?stype=2&page=",
        ]
        with config.RED.pipeline(transaction=False) as p:
            for url in url_list:
                for page in range(1, 11):
                    response = requests.get(
                        url + str(page),
                        headers=config.HEADERS,
                        timeout=5,
                    )
                    time.sleep(1)
                    data = re.findall(
                        "<td>(\d+).(\d+).(\d+).(\d+)</td>[\s\S]*?<td>(\d+)</td>",
                        response.text,
                        re.S,
                    )
                    for ip in data:
                        proxy = ".".join(ip[:-1]) + ":" + str(ip[-1])
                        p.sadd(config.REDIS_KEY_PROXY_FREE, proxy)
                    p.execute()
                    app.logger.info("[获取代理成功]-[云代理]-[%s]" % len(data))
    except:
        app.logger.error("[获取代理异常]-[云代理]")


def freeproxy_proxylistplus():
    """
    ProxyListplus
    https://list.proxylistplus.com/
    """
    try:
        with config.RED.pipeline(transaction=False) as p:
            for page in range(1, 11):
                response = requests.get(
                    "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-" + str(page),
                    headers=config.HEADERS,
                    timeout=5,
                )
                time.sleep(1)
                data = re.findall(
                    "<td>(\d+).(\d+).(\d+).(\d+)</td>[\s\S]*?<td>(\d+)</td>",
                    response.text,
                    re.S,
                )
                for ip in data:
                    proxy = ".".join(ip[:-1]) + ":" + str(ip[-1])
                    p.sadd(config.REDIS_KEY_PROXY_FREE, proxy)
                p.execute()
                app.logger.info("[获取代理成功]-[ProxyListplus]-[%s]" % len(data))
    except:
        app.logger.error("[获取代理异常]-[ProxyListplus]")


def run_proxy_get():
    threading.Thread(target=freeproxy_89).start()
    threading.Thread(target=freeproxy_yun).start()
    threading.Thread(target=freeproxy_proxylistplus).start()


if __name__ == "__main__":
    run_proxy_get()
