from random import randrange
from asyncio import sleep as asySleep
from datetime import datetime
import pytz

async def maddyTimerMain(client):
    maddyTimezone=pytz.timezone("EET")
    print("Auto sender started")
    maddy=await client.fetch_user(633637569975943169)
    while 1:
        times=(7,45),tuple(map(randrange,(18,0),(22,59)))
        print(times)

        while(lambda t:(t.hour,t.minute))(datetime.now(maddyTimezone))not in times:
            await asySleep(40)
        
        print("Notif sent")
        await maddy.send("Clean your teeth and have fun tying yourself up")
        await asySleep(200)