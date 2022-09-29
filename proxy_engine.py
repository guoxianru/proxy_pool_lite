# -*- coding: utf-8 -*-
# @Author: GXR
# @CreateTime: 2022-01-20
# @UpdateTime: 2022-09-29

import time

from apscheduler.schedulers.blocking import BlockingScheduler

import config
import proxy_api
import proxy_check
import proxy_get
import proxy_refresh

scheduler_options = {
    "job_defaults": {
        # 积攒的任务只跑一次
        "coalesce": True,
        # 最大并发实例数
        "max_instances": 1,
        # 任务超时容错
        "misfire_grace_time": 30,
    },
    "timezone": "Asia/Shanghai",
}
scheduler = BlockingScheduler(**scheduler_options)

# 定时获取新代理
scheduler.add_job(
    proxy_get.run_proxy_get,
    "interval",
    minutes=config.TIME_GET,
    id="proxy_get",
)

# 定时检查新代理
scheduler.add_job(
    proxy_check.run_proxy_check,
    "interval",
    minutes=config.TIME_CHECK,
    id="proxy_check",
)

# 定时刷新可用代理
scheduler.add_job(
    proxy_refresh.run_proxy_refresh,
    "interval",
    minutes=config.TIME_REFRESH,
    id="proxy_refresh",
)

# 定时重启API
scheduler.add_job(
    proxy_api.run_proxy_api,
    "cron",
    hour=time.localtime().tm_hour,
    minute=time.localtime().tm_min + 1,
    id="proxy_api",
)

scheduler.start()
