# 爬虫代理池Lite

> 测试网址：http://proxypool.addcoder.com/

## 一、下载安装

获取源码

```shell
git clone https://github.com/guoxianru/proxy_pool_lite
```

安装依赖

```shell
pip install -r requirements.txt
```

## 二、项目配置

config.py 为配置文件，根据注释自行修改

## 三、启动项目

```shell
nohup /root/.envs/python36_spider/bin/python /srv/proxy_pool_lite/proxy_engine.py > /srv/proxy_pool_lite/proxy_pool_lite.log 2>&1 &
```

访问 127.0.0.1:5010 查看

## 四、扩展代理

proxy_get.py 为获取新代理文件，新建函数将代理按指定格式添加到Redis中即可
