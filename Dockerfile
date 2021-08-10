FROM python:3.6
ENV DEBIAN_FRONTEND noninteractive
ENV TZ Asia/Shanghai
ADD . /srv/proxy_pool_lite
WORKDIR /srv/proxy_pool_lite
EXPOSE 5555

RUN mkdir /root/.pip
COPY ./pip.conf /root/.pip/pip.conf
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "proxy_engine.py" ]
