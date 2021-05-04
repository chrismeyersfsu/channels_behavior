import json
import logging

from django.conf.urls import url
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter


__all__ = ['application']


logger = logging.getLogger('cmeyers')


class EventConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send_json({'accept': True})
        await self.channel_layer.group_add('default', self.channel_name)
        logger.debug(f"client '{self.channel_name}' joined the default group.")
        for key, q in self.channel_layer.receive_buffer.items():
            logger.debug(f"channel{key}: size {q.qsize()}")

    async def disconnect(self, code):
        logger.debug(f"client '{self.channel_name}' left the default group.")
        await self.channel_layer.group_discard('default', self.channel_name)

    async def internal_message(self, event):
        await self.send(event['text'])


urls = [
    url(r'ws/$', EventConsumer)
]
application = ProtocolTypeRouter({
    'websocket': URLRouter(urls)
})

