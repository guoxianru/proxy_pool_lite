# -*- coding: utf-8 -*-
# @Author: GXR
# @CreateTime: 2022-01-20
# @UpdateTime: 2022-09-29

import json
import threading
import time

import requests

import config
from proxy_api import app


# 检查所有新代理
def proxy_check():
    while 1:
        proxy = config.RED.spop(config.REDIS_KEY_PROXY_FREE)
        if not proxy:
            break
        proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
        try:
            response = requests.get(
                config.PROXY_CHECK_URL,
                headers=config.HEADERS,
                proxies=proxies,
                timeout=3,
            )
            if response.status_code == 200:
                config.RED.sadd(
                    config.REDIS_KEY_PROXY_USEFUL,
                    json.dumps(
                        {
                            "proxy": proxy,
                            "time": time.strftime(
                                "%Y-%m-%d %H:%M:%S", time.localtime(time.time())
                            ),
                        }
                    ),
                )
                app.logger.info("[可用代理]-[%s]" % proxy)
        except:
            pass


def run_proxy_check():
    for i in range(config.THREAD_COUNT_PROXY_CHECK):
        t = threading.Thread(target=proxy_check)
        t.start()


if __name__ == "__main__":
    run_proxy_check()
