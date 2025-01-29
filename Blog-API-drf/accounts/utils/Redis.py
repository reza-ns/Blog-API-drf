import redis
from django.conf import settings

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    charset="utf-8",
    decode_responses=True
)


def redis_save(name, dic, expire_time):
    r.hset(name=name, mapping=dic)
    r.expire(name=name, time=expire_time, nx=True)

def redis_get(name):
    if r.exists(name) == 1:
        result = r.hgetall(name)
        return True, result
    else:
        return False, None