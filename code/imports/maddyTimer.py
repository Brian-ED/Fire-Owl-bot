import random 
from asyncio import sleep as asySleep
from datetime import datetime
import discord as dis
import pytz

client=dis.Client()
maddyTimezone=pytz.timezone("EET")

async def WaitTill(send,time):
    dt = datetime.now(maddyTimezone)
    while (dt.hour,dt.minute)!=time:
        print("Time info: ",dt.hour,dt.minute,time)
        dt = datetime.now(maddyTimezone)
        await asySleep(40)
    print("Notif sent")
    await send("Clean your teeth and have fun tying yourself up")

@client.event
async def on_ready():
    print("Auto sender started")
    maddy=await client.fetch_user(633637569975943169)
    while 1:
        await WaitTill(maddy.send,(*map(random.randrange,(18,0),(22,59)),))
        await WaitTill(maddy.send,(7,45))


## Instead of yaml stuff, you can use:
# token = YOUR_TOKEN
# client.run(token)

from yaml import safe_load
with open('../../Safe/Fire-Owl-bot.yaml', encoding='utf-8') as f:
    client.run(safe_load(f)['Token'])