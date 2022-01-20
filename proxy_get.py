# -*- coding: utf-8 -*-
# @Author: GXR
# @CreateTime: 2022-01-20
# @UpdateTime: 2022-01-20

import re
import threading
import time

import redis
import requests
from loguru import logger
from lxml import etree

import config

"""
    代理格式：127.0.0.1:8888
"""

red = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def freeproxy_89():
    """
        89代理
        https://www.89ip.cn/
    """
    try:
        response = requests.get(
            "http://api.89ip.cn/tqdl.html?api=1&num=3000&port=&address=&isp=",
            headers=config.HEADERS,
            timeout=20,
        )
        time.sleep(1)
        data = re.findall("(\d+).(\d+).(\d+).(\d+):(\d+)", response.text, re.S)
        with red.pipeline(transaction=False) as p:
            for ip in data:
                proxy = ".".join(ip[:-1]) + ":" + str(ip[-1])
                p.sadd(config.REDIS_KEY_PROXY_FREE, proxy)
            p.execute()
        logger.debug("获取代理[%s]" % len(data))
    except:
        logger.error("获取代理异常")


def freeproxy_xiaoshu():
    """
        小舒代理
        http://www.xsdaili.com/
    """
    try:
        response = requests.get(
            url="http://www.xsdaili.com/", headers=config.HEADERS, timeout=20
        )
        time.sleep(1)
        response.encoding = response.status_code
        html = etree.HTML(response.text)
        hrefs = html.xpath("//div[@class='title']/a/@href")[:2]
        for href in hrefs:
            url = "http://www.xsdaili.cn" + href
            response_ip = requests.get(url, headers=config.HEADERS, timeout=20)
            time.sleep(1)
            response_ip.encoding = response_ip.status_code
            data = re.findall("(\d+).(\d+).(\d+).(\d+):(\d+)", response_ip.text, re.S,)
            with red.pipeline(transaction=False) as p:
                for ip in data:
                    proxy = ".".join(ip[:-1]) + ":" + str(ip[-1])
                    p.sadd(config.REDIS_KEY_PROXY_FREE, proxy)
            p.execute()
            logger.debug("获取代理[%s]" % len(data))
    except:
        logger.error("获取代理异常")


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
        with red.pipeline(transaction=False) as p:
            for url in url_list:
                for page in range(1, 6):
                    response = requests.get(
                        url + str(page), headers=config.HEADERS, timeout=20
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
                    logger.debug("获取代理[%s]" % len(data))
    except:
        logger.error("获取代理异常")


def freeproxy_proxylistplus():
    """
        ProxyListplus
        https://list.proxylistplus.com/
    """
    try:
        with red.pipeline(transaction=False) as p:
            for page in range(1, 6):
                response = requests.get(
                    "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-" + str(page),
                    headers=config.HEADERS,
                    timeout=20,
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
                logger.debug("获取代理[%s]" % len(data))
    except:
        logger.error("获取代理异常")


def run_proxy_get():
    threading.Thread(target=freeproxy_89).start()
    threading.Thread(target=freeproxy_xiaoshu).start()
    threading.Thread(target=freeproxy_yun).start()
    threading.Thread(target=freeproxy_proxylistplus).start()


if __name__ == "__main__":
    run_proxy_get()
