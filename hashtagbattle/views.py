from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Battle
from .forms import BattleForm
from crawler import crawler
import apscheduler
import random
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
SCHEDULER = BackgroundScheduler()

def battle_create(request):
    ''' Method for creating new battles.
    Params:
        request <django request object>
    '''

    #only authorized users can run this method
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = BattleForm(request.POST or None)
    if form.is_valid():
        instance =  form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created.")    
        return redirect('battles:list')
    context = {
        "form": form
    }
    return render(request, "battle_form.html", context)

def battle_detail(request, id=None):
    ''' Method for showing battle details.
    Params:
        request <django request object>
        id <integer> battle id
    '''

    battle = get_object_or_404(Battle, battle_id=id)
    context = {
        "battle": battle
    }
    return render(request, "battle_details.html", context)

def battle_list(request):
    ''' Method for showing battles list.
    Params:
        request <django request object>
        id <integer> battle id
    '''

    battles_lst = Battle.objects.all()
    paginator = Paginator(battles_lst, 10) # Show 10 battles per page

    page = request.GET.get('page')
    try:
        battles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        battles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        battles = paginator.page(paginator.num_pages)
    context = {
        "title": "list",
        "battles": battles
    }
    return render(request, "battle_list.html", context)

def battle_update(request, id=None):
    ''' Method for updating battle details.
    Params:
        request <django request object>
        id <integer> battle id
    '''

    #only authorized users can run this method
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Battle, battle_id=id)
    form = BattleForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated.")
        #return HttpResponseRedirect(instance.get_absolute_url())
        return redirect('battles:list')
    context = {
        "form": form,
        "instance": instance
    }
    return render(request, "battle_form.html", context)

def battle_status_update(request, id=None, status=None):
    ''' Method for updating battle status to either R=Running or D=Done.
    Params:
        request <django request object>
        id <integer> battle id
        status <string> current status
    '''

    #only authorized users can run this method
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Battle, battle_id=id)
    status = 'D' if status=='R' else 'R'
    Battle.objects.filter(
        battle_id=instance.battle_id).update(crawl_status=status)
    messages.success(request, "Staus Updated Successfully.")
    return redirect('battles:list')

def battle_delete(request, id=None):
    ''' Method for deleting selected battle.
    Params:
        request <django request object>
        id <integer> battle id
    '''

    #only authorized users can run this method
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Battle, battle_id=id)
    instance.delete()
    messages.success(request, "Successfully Deleted.")
    return redirect('battles:list')

def battle_result(request, id=None):
    ''' Method for showing battle result for selected battle id.
    Params:
        request <django request object>
        id <integer> battle id
    '''

    instance = get_object_or_404(Battle, battle_id=id)
    res = crawler(instance.hashtag1, instance.hashtag2)
    messages.success(request, res, extra_tags='html_safe')
    return redirect('battles:list')

def start_crawling(request):
    ''' Method used to start crawler
    Params:
        request <django request object>
    '''

    jobid = random.randint(1000,10000)

    try:
        SCHEDULER.start() # start scheduler
        messages.success(request, "Twitter Crawler started successfully.")
    except apscheduler.schedulers.SchedulerAlreadyRunningError:
        messages.success(request, "Crawler is already running.")
    return redirect('battles:list')

def stop_crawling(request):
    ''' Method to stop crawler.
    Params:
        request <django request object>
    '''

    try:
        SCHEDULER.shutdown()
        messages.success(request, "Crawling stopped successfully.")
    except apscheduler.schedulers.SchedulerNotRunningError:
        messages.success(request, "Crawler is not running, start it first.")
    return redirect('battles:list')

def get_candidate_battles():
    ''' Method used to return battles which are to be crawled.'''

    battles = Battle.objects.filter(crawl_status='R')
    return battles

def update_crawl_data(battle):
    ''' Method used to update battle record with crawl stats and winner.
    Params:
        battle row object
    '''

    # do actual crawling and returns dict of data
    res = crawler(battle.hashtag1, battle.hashtag2)
    # sample res= {'num_tweet_winner': 'PURPOSETOUR',
                   #'tag2_num_tweets': '21', 'tag2_num_spell_errors': '68',
                   #'tag1_num_spell_errors': '82', 'tag1_num_tweets': '19',
                   #'num_spell_winner': 'PURPOSETOUR'}

    # update battle status to done if its end date has past
    crawl_status = 'R'
    tz_info = battle.battle_end.tzinfo
    if battle.battle_end <= datetime.now(tz_info):
        crawl_status = 'D'
    
    # updated battle record with crawled data
    Battle.objects.filter(battle_id=battle.battle_id).update(
            crawl_status=crawl_status,
            tag1_num_tweets=res['tag1_num_tweets'],
            tag2_num_tweets=res['tag2_num_tweets'],
            tag1_num_spell_errors=res['tag1_num_spell_errors'],
            tag2_num_spell_errors=res['tag2_num_spell_errors'],
            num_tweet_winner=res['num_tweet_winner'],
            num_spell_winner=res['num_spell_winner'],
    )
    return True

# other options are weeks=0, days=0, hours=0, minutes=0, seconds=0 etc
@SCHEDULER.scheduled_job('interval', seconds=5)
def crawl_twitter():
    ''' Crawl Twitter for hash tags.'''

    battles = get_candidate_battles()
    for battle in battles:
        # update battle crawl data table
        st = update_crawl_data(battle)
    return st
    
       




