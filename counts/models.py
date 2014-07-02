import random
import string
from django.db import models
from django.core import cache


__all__ = ['Messages']


prefix = 'messages'
users_key = '%s:%s' % (prefix, 'users')
cities_key = '%s:%s' % (prefix, 'cities')
multiple_requests = 'multiple requests to rebuild cache, returning rather than waiting'


class Messages(models.Model):
    state = models.CharField('State', max_length=64)
    city = models.CharField('City', max_length=64)
    username = models.CharField('User', max_length=64)
    message = models.TextField('Message')
    create_time = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        ordering = ['state', 'city', 'create_time']

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        rebuild_city_cache()
        rebuild_user_cache()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        models.Model.save(self,
                          force_insert=force_insert,
                          force_update=force_update,
                          using=using,
                          update_fields=update_fields)
        cache_contention = put_cache(self.state, self.city, self.username)
        if cache_contention:
            print "Cache missed an update since it was rebuilding"

    @staticmethod
    def get_city_count():
        if rebuild_city_cache():
            return cache.cache.raw_client.scard(cities_key)
        else:
            raise KeyError(multiple_requests)

    @staticmethod
    def get_user_count():
        if rebuild_user_cache():
            return cache.cache.raw_client.scard(users_key)
        else:
            raise KeyError(multiple_requests)

    @staticmethod
    def flush_cache():
        cache.cache.raw_client.delete(cities_key)
        cache.cache.raw_client.delete(users_key)


def put_cache(state, city, username):
    cache_contention = False
    if rebuild_city_cache():
        cache.cache.raw_client.sadd(cities_key, '%s:%s' % (state, city))
    else:
        cache_contention = True

    if rebuild_user_cache():
        cache.cache.raw_client.sadd(users_key, username)
    else:
        cache_contention = True
    return cache_contention


def rebuild_city_cache():
    if cache.cache.raw_client.exists(cities_key):
        return True
    lock = cities_key + '_lock'
    token = new_token()
    if cache.cache.raw_client.set(lock, token, 'px', 60000, 'nx'):
        q = Messages.objects.values('state', 'city').order_by('state', 'city').distinct('state', 'city')
        if q:
            cache.cache.raw_client.sadd(cities_key, *[state_city(dct) for dct in q])
        cache.cache.raw_client.delete(lock)
        return True
    else:
        return False


def rebuild_user_cache():
    if cache.cache.raw_client.exists(users_key):
        return True
    lock = users_key + '_lock'
    token = new_token()
    if cache.cache.raw_client.set(lock, token, 'px', 60000, 'nx'):
        q = Messages.objects.values('username').order_by('username').distinct()
        if q:
            cache.cache.raw_client.sadd(users_key, *[dct['username'] for dct in q])
        cache.cache.raw_client.delete(lock)
        return True
    else:
        return False


def state_city(dct):
    return '%s:%s' % (dct['state'], dct['city'])


def new_token():
    return ''.join(random.choice(string.ascii_letters) for _ in xrange(16))