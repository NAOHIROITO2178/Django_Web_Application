from celery import shared_task
import requests
from .models import News
from datetime import datetime

@shared_task
def fetch_and_save_news():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    top_stories = response.json()[:100]
  
    for story_id top_stories:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_reponse = requests.get(story_url)
        story_data = story_response.json()

        if any(ord(c) >= 128 for c in story_data.get('title', '')):
            news, created = News.object.get_or_create(
                id=story_id, 
                defaults={
                    'title':story_data.get('title'),
                    'link': story_data.get('url'),
                    'time': datatime.fromtimestamp(story_data.get('time')),
                }
            )
            if created:
                print(f"新しいニュースの追加: {news.title}")

    News.objects.filter(time__lt=datetime.now() - timedelta(days=1)).delete()

