# channels_behavior
Django channels performance characteristics and redis_channels behavior

`docker-compose up` or `make docker-compose`

http://localhost:8049/static/index.html <--- click the "connect" button

```
docker exec -it channels_redis_debug_daphne_1 /bin/bash
cd /opt/channels_redis_debug
./manage.py workload
```

You will notice the "Time to get" immediately begins to rise. This is because events are being produced faster than they can be consumed. The "Rate over the last 5 seconds" rises and then dives to a new low water mark when the channel group capacity is reached.
