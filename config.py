# -*- coding: utf-8 -*-
# @Author: GXR
# @CreateTime: 2021-04-22

# 代理池Redis设置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_PASSWORD = "password"
REDIS_DB = "0"

# 代理池Redis-key
REDIS_KEY_PROXY_FREE = "proxy_free"
REDIS_KEY_PROXY_USEFUL = "proxy_useful"

# 代理池检查线程数
THREAD_COUNT_PROXY_CHECK = 10

# 代理池刷新线程数
THREAD_COUNT_PROXY_REFRESH = 5

# 获取新代理时间周期
TIME_GET = 1

# 检查新代理时间周期
TIME_CHECK = 2

# 刷新可用代理时间周期
TIME_REFRESH = 3

# 代理池API设置
API_HOST = "0.0.0.0"
API_PORT = "5010"

# 测试代理网站
PROXY_CHECK_URL = "https://www.baidu.com/"

# 通用请求头
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}

# USER_AGENT池
USER_AGENT_LIST = [
    # Mac的Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
    # Windows10的Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    # Windows10的Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/89.0.774.77",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
    # Windows7的火狐浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0"
    # Windows7的360极速浏览器
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
]
