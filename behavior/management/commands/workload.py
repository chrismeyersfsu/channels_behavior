import asyncio
import time
import json
import multiprocessing

from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def run_sync(func):
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(func)
    event_loop.close()


def run_sync(ignore=None):
    channel_layer = get_channel_layer()
    i = 0
    while True:
        async_to_sync(channel_layer.group_send)(
            'default',
            {'type': 'internal.message', 'text': json.dumps({'1': 'a' * 1, 'ts_sent': int(time.time()*1000)})}
        )
        if i % 1000 == 0:
            print(f"{i} messages sent")
        i += 1


async def run_async():
    channel_layer = get_channel_layer()
    i = 0
    while True:
        await channel_layer.group_send(
            'default',
            {'type': 'internal.message', 'text': json.dumps({'1': 'a' * 1024, 'ts_sent': int(time.time()*1000)})}
        )
        if i % 1000 == 0:
            print(f"{i} messages sent")
        i += 1


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sync', action='store_true', help='Use sync_to_async() to send events.')
        parser.add_argument('-c', '--concurrency', type=int, help='Use sync_to_async() to send events.', default=1)

    def handle(self, *args, **options):
        concurrency = options['concurrency'] or 1
        if options['sync']:
            if concurrency > 1:
                p = multiprocessing.Pool(concurrency)
                p.map(run_sync, range(0, concurrency))
            else:
                run_sync()
        else:
            event_loop = asyncio.get_event_loop()
            try:
                event_loop.run_until_complete(run_async())
            except KeyboardInterrupt:
                print("Closing")
            event_loop.close()

