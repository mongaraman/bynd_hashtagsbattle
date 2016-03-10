from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

DEFAULT_BATTLE_END_DAYS = 1

CRAWL_STATUSES = (
    ('R', 'Running'),
    ('D', 'Done'),
)

class Battle(models.Model): 
    ''' Class containing battle model fields.'''

    default_endtime = datetime.now() + timedelta(days=DEFAULT_BATTLE_END_DAYS)
    battle_id = models.AutoField(primary_key=True)
    battle_name = models.CharField(max_length=120)
    hashtag1 = models.CharField(max_length=250)
    hashtag2 = models.CharField(max_length=250)
    battle_start = models.DateTimeField(auto_now_add=True)
    battle_end = models.DateTimeField(default=default_endtime)
    tag1_num_tweets = models.IntegerField(default=0)
    tag2_num_tweets = models.IntegerField(default=0)
    tag1_num_spell_errors = models.IntegerField(default=0)
    tag2_num_spell_errors = models.IntegerField(default=0)
    num_tweet_winner = models.CharField(max_length=250, default='')
    num_spell_winner = models.CharField(max_length=250, default='')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    crawl_status = models.CharField(max_length=1, choices=CRAWL_STATUSES,
                                    default='R')

    def __unicode__(self): # __unicode__ on Python 2
        return self.battle_name

    def __str__(self):
        return self.battle_name

    def get_absolute_url(self):
        return reverse("battles:detail", kwargs={"id": self.battle_id})

    class Meta:
        ordering = ["-timestamp", "-updated"]


