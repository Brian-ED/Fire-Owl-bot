from random import choice
from imports.fns import *
from asyncio import sleep as asySleep

Ping=C("hiii")
Pong=C("hello")

def Ball8(*_,myData={},**a):
    return choice([*myData['8ball']])

def ChangePrefix(arg,data={},Save=C,guildID=0,**_):
    data[guildID]['Prefix']=arg
    Save(data)
    return f'Prefix changed to: "{arg}"'

def ShowPrefix(prefix='',**_):
    return f'Current prefix: "{prefix}".'

def prefix(*args,**V):
    return ChangePrefix(args[0],**V) if args else ShowPrefix(**V)

async def RickRoll(say=C,**_):
    ytUrl='https://youtu.be/'
    await say(ytUrl+'dQw4w9WgXcQ',DM=1)
    await asySleep(15)
    await say(
        'Ok i am so sorry... please forgive me. here are some cats :D',
        ytUrl+'VZrDxD0Za9I',DM=1)
    await asySleep(200)
    await say('cope',DM=1)
    await asySleep(5)
    await say(f'this can help :)\n{ytUrl}Lc6db8qfZEw',DM=1)


cmdFns={
    "Ping":Ping,
    "Pong":Pong,
    "8ball":Ball8,
    "ChangePrefix":ChangePrefix,
    "ShowPrefix":ShowPrefix,
    "Prefix":prefix,
    "Rick":RickRoll,
}