from random import randrange
from asyncio import sleep as asySleep
from datetime import datetime
import pytz

maddyTimezone=pytz.timezone("EET")

async def WaitTill(send,*time):
    dt = datetime.now(maddyTimezone)
    while (dt.hour,dt.minute)!=time:
        print("Time info: ",dt.hour,dt.minute,time)
        dt = datetime.now(maddyTimezone)
        await asySleep(40)
    print("Notif sent")
    await send("Clean your teeth and have fun tying yourself up")

async def maddyTimerMain(client):
    print("Auto sender started")
    maddy=await client.fetch_user(633637569975943169)
    while 1:
        await WaitTill(maddy.send,7,45)
        await WaitTill(maddy.send,*map(randrange,(18,0),(22,59)))