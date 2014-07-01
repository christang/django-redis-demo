from django.db import models
from django.core import cache


__all__ = ['Messages']


prefix = 'messages'
users_key = '%s:%s' % (prefix, 'users')
cities_key = '%s:%s' % (prefix, 'cities')


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
        put_cache(self.state, self.city, self.username)

    @staticmethod
    def get_city_count():
        rebuild_city_cache()
        return cache.cache.raw_client.scard(cities_key)

    @staticmethod
    def get_user_count():
        rebuild_user_cache()
        return cache.cache.raw_client.scard(users_key)


def put_cache(state, city, username):
    rebuild_city_cache()
    cache.cache.raw_client.sadd(cities_key, '%s:%s' % (state, city))
    rebuild_user_cache()
    cache.cache.raw_client.sadd(users_key, username)


def rebuild_city_cache():
    if not cache.cache.raw_client.exists(cities_key):
        q = Messages.objects.values('state', 'city').order_by('state', 'city').distinct('state', 'city')
        cache.cache.raw_client.sadd(cities_key, *[state_city(dct) for dct in q])


def rebuild_user_cache():
    if not cache.cache.raw_client.exists(users_key):
        q = Messages.objects.values('username').order_by('username').distinct()
        cache.cache.raw_client.sadd(users_key, *[dct['username'] for dct in q])


def state_city(dct):
    return '%s:%s' % (dct['state'], dct['city'])
