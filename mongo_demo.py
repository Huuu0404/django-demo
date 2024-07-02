import requests
from pymongo import MongoClient
import json
from datetime import datetime, timedelta
import pytz
import time

client = MongoClient('mongodb+srv://waynehu:2gy1k9jPasUqRqsz@cluster0.r9ljfbf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['mongo_demo']  
collection = db['events']  

def fetch_data_and_store():
    url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        if data:
            for item in data:
                collection.insert_one(item)
            print(f"Successfully inserted {len(data)} records into MongoDB.")
        else:
            print("No data retrieved.")

    except Exception as e:
        print(f"Error fetching or storing data: {str(e)}")

def schedule_job():
    tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz)
    next_run = now.replace(hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)

    delta = next_run - now
    delay_seconds = delta.total_seconds()

    time.sleep(delay_seconds)
    fetch_data_and_store()


if __name__ == "__main__":
    while True:
        schedule_job()
