#!/bin/bash

# 加载环境变量
source ~/.bashrc

# 停止所有容器
docker stop $(docker ps -a -q)

# 删除所有容器（container）：
docker rm $(docker ps -a -q)

# 删除全部镜像（images）的话
docker rmi $(docker images -a)

# 清除历史文件
cd /srv && rm -rf proxy_pool_lite

# 拉取最新代码
/usr/bin/expect <<-EOF
  set timeout 10
  spawn git clone git@github.com:guoxianru/proxy_pool_lite.git
  expect "Enter passphrase for key '/root/.ssh/id_rsa':"
  send "root\r"
  expect eof
EOF

# 切换项目目录
cd proxy_pool_lite

# 切换虚拟环境
workon flask_py38

# 启动服务进程
docker-compose -f docker-compose.yml up -d --build

# 重启Nginx
systemctl restart nginx
