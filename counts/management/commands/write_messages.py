import collections
import optparse
import os
import random
import string
import sys
import time
from django.core.management import base
from counts import models as count_models

import _io

CWD = os.path.dirname(__file__)
CITIES_FN = 'data/Top5000Population.csv'
CITIES_PATH = os.path.join(CWD, CITIES_FN)
USERS = 100

class Command(base.BaseCommand):
    
    help = 'Loads messages into the db'
    option_list = base.BaseCommand.option_list + (
        optparse.make_option('-c', '--clear',
            action='store_true',
            default=False,
            help='Clear the messages table'),
        optparse.make_option('-n', '--number',
            type='int',
            default=1,
            help='Number of messages to fill table with'),
        optparse.make_option('-d', '--delay',
            type='int',
            default=0,
            help='Delay in milliseconds between each message'),
    )

    def __init__(self, *args, **options):
        """Initialize a set of cities and usernames
        """
        base.BaseCommand.__init__(self, *args, **options)
        self._usernames = [ random_username() for i in xrange(USERS) ]
        with open(CITIES_PATH) as cities_file:
            self._locations = _io.read_city_state_pop(cities_file)

    def handle(self, *args, **options):
        """Adds n_msgs=n to the Message table, waiting t_delay=d 
        milliseconds in between
        """
        if options['clear']:
            count_models.Messages.objects.all().delete()
            print 'Messages cleared'
            options['number'] = options['number'] if options['number'] != 1 else 0
        print 'Writing %d messages' % options['number']
        for i in xrange(options['number']):
            username = random.choice(self._usernames)
            location = random.choice(self._locations.keys())
            message = count_models.Messages(
                    state=location.state, 
                    city=location.city,
                    username=username,
                    message=str(i))
            message.save()
            time.sleep(options['delay']/1000.0)

def random_username():
    return ''.join(random.choice(string.lowercase) for _ in xrange(10))

