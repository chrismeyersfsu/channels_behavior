FROM python
ENV PYTHONUNBURRERED 1

RUN mkdir -p /opt/channels_redis_debug
WORKDIR /opt/channels_redis_debug
ADD requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt
#RUN python manage.py migrate
