import json
import os
import django
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roar.settings')
django.setup()

from myapp.models import Event, EventUnit, Location, ShowInfo

# 讀取JSON檔案
with open('/home/user/Downloads/SearchShowAction.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 插入資料到資料庫
for item in data:
    event = Event(
        title=item.get('title'),
        uid = item.get('uid'),
        version = item.get('version'),
        category=item.get('category'),
        imageUrl=item.get('imageUrl'),
        webSales=item.get('webSales'),
        sourceWebPromote=item.get('sourceWebPromote'),
        comment=item.get('comment'),
        editModifyDate=datetime.strptime(item.get('editModifyDate'), "%Y/%m/%d %H:%M:%S") if item.get('editModifyDate') else None,
        sourceWebName=item.get('sourceWebName'),
        startDate=datetime.strptime(item.get('startDate'), "%Y/%m/%d") if item.get('startDate') else None,
        endDate=datetime.strptime(item.get('endDate'), "%Y/%m/%d") if item.get('endDate') else None,
        hitRate=item.get('hitRate')
    )
    event.save()

    for unit in item.get('masterUnit', []):
        EventUnit(event=event, unitType='master', unitName=unit).save()
    for unit in item.get('subUnit', []):
        EventUnit(event=event, unitType='sub', unitName=unit).save()
    for unit in item.get('supportUnit', []):
        EventUnit(event=event, unitType='support', unitName=unit).save()
    for unit in item.get('otherUnit', []):
        EventUnit(event=event, unitType='other', unitName=unit).save()

    for show_info in item.get('showInfo', []):
        location, created = Location.objects.get_or_create(
            locationName=show_info.get('locationName'),
            address=show_info.get('location'),
            latitude=show_info.get('latitude'),
            longitude=show_info.get('longitude')
        )
        ShowInfo(event=event, time=show_info.get('time'), location=location).save()

print("Data imported successfully!")
