import os
from random import choice
from shutil import copytree, rmtree
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

def Prefix(*args,**V):
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

def HelpCmd(cmds={},isMod=0,isAdmin=0,isOwner=0,**_):
    print(cmds)
    r =             '**User commands**:\n' +Join(cmds['userCommands']),
    if isMod:  r+='\n**Mod commands:**\n'  +Join(cmds['modCommands']),
    if isAdmin:r+='\n**Admin commands:**\n'+Join(cmds['adminCommands']),
    if isOwner:r+='\n**Owner commands:**\n'+Join(cmds['ownerCommands']),
    return r

def NewResponse(*_,Save=C,msg=C,data={},guildID=0,**V):
    d = {'replywith:': 'Responses', 'reactwith:': 'Reacts'}
    lenOfFirstArg=len(msg.content.split()[0])
    for key in d:
        fullMsg=msg.content.lower()
        if key in fullMsg:
            indexOf=fullMsg.index(key)
            KeyStr=fullMsg[lenOfFirstArg+1:indexOf-1]
            ValStr=fullMsg[indexOf+len(key)+1:]

            data[guildID][d[key]][KeyStr]=ValStr
            Save(data)
            return'Alas it is done'
    return'You need to include " replywith: " or " reactwith: " in the message. Not both btw.'

def ListResponses(responses={},reacts={},**_):
    return ('**Responses:**\n'+Join(responses.keys()),
        '\n**Reacts:**\n'+Join(reacts.keys()))

async def Update(say=C,isLinux=0,savestatePath='',codePath='',extraPath='',botPath='',**_):
    if isLinux:
        await say("updating...")

        rmtree(savestatePath)
        copytree(extraPath, savestatePath)
        await asySleep(0.5)
        os.system('cd '+botPath)
        os.system('git reset --hard')
        os.system('git clean -fd')
        os.system('git pull')
        os.system('cd '+codePath)
        os.system('python3 main.py')
        await asySleep(0.5)
        quit()

def Flip(*a,**_):
    return choice(('Heads','Tails'))

def RestoreBackup(extraPath='',savestatePath='',**_):
    rmtree(extraPath)
    copytree(savestatePath, extraPath)
    return'You restored the files: '+Join(os.listdir(savestatePath))

def RockPaperScissors(userChoice,**_):
    RPS = 'rock','paper','scissors'    
    if userChoice not in RPS:
        return'The command only accepts '+Join(RPS)

    botChoice = choice(RPS)

    r=''
    if userChoice == botChoice:
        r="Ah we drew the game m'lad, well played"
    elif userChoice == 'rock':
        if botChoice == 'scissors':
            r='Ha i see, my scissors seem to be no match for thy mighty rock <:hmm:881738404944023562>'
        elif botChoice == 'paper':
            r='Haha i got ya there! you see my paper is basically made of steel so you never had a chance with that sand-particle worth of a rock!'
    elif userChoice == 'scissors':
        if botChoice=='rock':
            r='Ha i won! My beutiful rock never fails against your unsharpened baby scissors <:KEKW:854415812534468627>'
        elif botChoice=='paper':
            r="Oh i lost! Y'know i got that paper from my grandma before she died... :(... Ha just kidding, totally got you there :)"
    elif userChoice == 'paper':
        if botChoice == 'rock':
            r="Did... did you just wrap your paper around my rock and assume i can't still throw it?.. wdym it's in the rules?.. God damnit"
        elif botChoice =='scissors':
            r="Ha my mighty metal scissors can cut throgh any paper! Y'know, your paper might aswell be taken right out of the toilet roll for how much of a fight it put up!"

    return f'You chose **{userChoice}**. I (the bot) chose **{botChoice}**.\n{r}'

def InfoCmd(isMod=0,isAdmin=0,isOwner=0,replyDelay=0,isReplyChannel=0,isBotChannel=0,isReactChannel=0,**_):
    return('```',
    'This command is mostly for debugging btw',
    f"You're mod: {isMod}",
    f"You're admin: {isAdmin}",
    f"You're bot owner: {isOwner}",
    f'Replies cooldown: {replyDelay}',
    f'{isBotChannel=}, {isReplyChannel=}, {isReactChannel=}',
    '```')

def DelDataSlot(slot:str,*args,data={},guildID=0,Save=C,**_):
    ValStr=' '.join(args)
    if ValStr in data[guildID][slot]:
        del data[guildID][slot][ValStr]
        Save(data)
        return'deleted'
    return"Reply doesn't exist"

cmdFns={
    'userCommands':{
        'Ping':Ping,
        'Pong':Pong,
        '8ball':Ball8,
        'ShowPrefix':ShowPrefix,
        'Rick':RickRoll,
        'Help':HelpCmd,
        'ListResponses':ListResponses,
        'Flip':Flip,
        'RPS':RockPaperScissors,
        'Info':InfoCmd,
    },
    'modCommands':{
        'DelResponse':Curry(DelDataSlot,'Responses'),
        'DelReact':Curry(DelDataSlot,'Reacts'),
        'NewResponse':NewResponse,
        'Prefix':Prefix,
        'ChangePrefix':ChangePrefix,
    },
    'adminCommands':{

    },
    'ownerCommands':{

    }
}