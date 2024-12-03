from django.http import StreamingHttpResponse
from .models import FeedModel
import feedparser
import httpx
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django.core.cache import cache
import os
from asgiref.sync import sync_to_async
from urllib.parse import quote
from django.core.serializers import serialize
import json
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def fetch_feed():
    async with httpx.AsyncClient() as client:
        # RSS Feed URL
        url = os.getenv("RSS_FEED_URL")
        try:
            response = await client.get(url)
            return response.text
        except httpx.HTTPStatusError as e:
            # Raise an error with the same status code
            raise Exception(f"HTTP Error {e.response.status_code}: {e.response.reason_phrase}") from e
        except Exception as e:
            # Handle other exceptions 
            raise Exception(f"An error occurred: {str(e)}") from e
             

@sync_to_async
def get_last_updated_time():
    # Fetch Last updated time value to save only the latest entries to db (and link shortening)
    last_updated = cache.get("last_updated")
    print("Trying to retreive last updated time from cache ", last_updated)

    if not last_updated:
        # Fall Back for last updated is issues with cache
        latest_entry = FeedModel.objects.order_by("-published").first()
        if(latest_entry):
            print("Reteived from latest entry")
            last_updated = latest_entry.published
        else:
            print("Retreived from last fall back")
            last_updated = datetime.now(ZoneInfo("Asia/Kolkata")) - timedelta(seconds=61) # subtracting 1 minutes 1 second from current IST

    return last_updated

async def shorten_url(url):
    async with httpx.AsyncClient() as client:
        print("Shortening URL for", url)
        # RSS Feed URL
        tiny_url_api = os.getenv("TINY_URL")
        encoded_url = quote(url)

        # Try to shorten the URL and fall back to original if any error occurs
        try:
            response = await client.get(tiny_url_api + "=" + encoded_url)
            return response.text
        except:
            print("Error occured while shortening url")
            return url

async def compute_feed():
    last_updated = await get_last_updated_time()
    print("Last updated retreived as ", last_updated)

    # Fetching feed 
    feed_content = await fetch_feed()
    print("Fetched latest feed")
    feed = feedparser.parse(feed_content)

    for entry in feed.entries:
        published = entry.published
        published_datetime = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")    

        # Update only if published after the last update
        if(published_datetime <= last_updated):
            continue

        print(f"The following article was published on {published_datetime} which is after the feed was last updated{last_updated}: {entry.title}")

        title = entry.title
        summary = entry.summary
        image_url = entry.media_content[0]["url"] if entry.media_content and entry.media_content[0]["medium"] == "image" else ""
        link = entry.link
        shortened_link = await shorten_url(link)

        await sync_to_async(FeedModel.objects.create)(
            title=title,
            summary=summary,
            published=published_datetime,
            image=image_url,
            link=link,
            shortened_link=shortened_link
        )


    latest_feed = await sync_to_async(list)(FeedModel.objects.order_by("-published")[:16])

    serialized_feed = [ 
        {
            "title" : entry.title,
            "summary" : entry.summary,
            "published" : entry.published.astimezone(ZoneInfo("Asia/Kolkata")).strftime("%b %d, %Y, %I:%M %p"),
            "image" : entry.image,
            "link" : entry.link,
            "shortened_link" : entry.shortened_link,
        }

        for entry in latest_feed
    ] 

    cache.set("last_updated", datetime.now(ZoneInfo("Asia/Kolkata")), timeout=61)
    
    return serialized_feed

async def refresh_feed(request):
    async def event_stream():
        while True:
            try:
                print(f"Updating at {datetime.now()}")
                data = await compute_feed()
                yield f"data: {json.dumps(data)}\n\n"
            except Exception as e:
                print("Error occured, ", str(e))
                yield f"data: {json.dumps({'error': 'An error occurred', 'message': str(e)})}\n\n"

            await asyncio.sleep(601)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    return response