# -*- coding: utf-8 -*-
# @Author: GXR
# @CreateTime: 2021-04-01
# @UpdateTime: 2021-08-10

import time

from apscheduler.schedulers.blocking import BlockingScheduler

import config
import proxy_api
import proxy_check
import proxy_get
import proxy_refresh

scheduler = BlockingScheduler()

# 定时获取新代理
scheduler.add_job(proxy_get.run_proxy_get, "interval", minutes=config.TIME_GET)

# 定时检查新代理
scheduler.add_job(proxy_check.run_proxy_check, "interval", minutes=config.TIME_CHECK)

# 定时刷新可用代理
scheduler.add_job(
    proxy_refresh.run_proxy_refresh, "interval", minutes=config.TIME_REFRESH
)

# 定时重启API
scheduler.add_job(
    proxy_api.run_proxy_api,
    "cron",
    hour=time.localtime().tm_hour,
    minute=time.localtime().tm_min + 1,
)

scheduler.start()
