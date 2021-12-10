# 爬虫代理池Lite

> 测试网址(单机勿压)：http://43.133.195.71:31605/

## 一、下载安装

```shell
git clone https://github.com/guoxianru/proxy_pool_lite
```

## 二、项目配置

config.py 为配置文件，根据注释自行修改

## 三、启动项目

- 源码版

```shell
# 安装依赖
pip install -r requirements.txt
# 启动项目
nohup python proxy_pool_lite/proxy_engine.py >> proxy_pool_lite/proxy_pool_lite_`date +%Y-%m-%d_%H:%M:%S`.log 2>&1 &
```

- Docker版

```shell
docker-compose -f docker-compose.yml up -d --build
```

- 查看方法

IP:PORT

## 四、扩展代理

proxy_get.py 为获取新代理文件，新建函数将代理按指定格式添加到Redis中即可
