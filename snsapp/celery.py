from celery import celery

app = Celery('Django_Web_Application', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'fetch_news_every_24_hours': {
        'task': 'snsapp.tasks.fetch_and_save_news',
        'schedule':  crontab(minute=0, hour=0), 
    }
}
