import os
from random import choice, randint
import re
from shutil import copytree, rmtree
from time import time
if __name__!="__main__":
    from imports.fns import *
    from imports.vars import *
    from imports import TicTacToe, AI
else:
    import TicTacToe
    from vars import *
    from fns import *
from asyncio import sleep as asySleep
import discord as dis
from discord.abc import PrivateChannel
import json

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
    return'Not available for the test version'

def Backup(savestatePath='',extraPath='',**_):
    rmtree(savestatePath)
    copytree(extraPath, savestatePath)
    return'You backuped the files: '+Join(os.listdir(extraPath))
    

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

def DelDataSlot(slot,*arguments,data={},guildID=0,Save=C,**_):
    ValStr=' '.join(arguments)
    if ValStr in data[guildID][slot]:
        del data[guildID][slot][ValStr]
        Save(data)
        return'deleted'
    return"Reply doesn't exist"

def Zote(*a,**_):
    return choice(zoteQuotes)

async def Metheus(*_a,say=C,msg=C,client=C,**_):
    await say('Keep in mind this is a command for a spesific game called the Metheus Puzzle (<https://dontstarve-archive.fandom.com/wiki/Metheus_Puzzles>)')
    return await metheus(client,msg,say)

async def EmergencyQuit(say=C,**_):
    await say("I'm sorry for what i did :(\nBye lovely folks!")
    asySleep(0.5)
    quit()

def Error(**_):
    return Any+Any

async def MoveCmd(inpChannel:ChannelID,numOfMsgs:int,*args:int,msg=C,say=C,client=C,prefix='',**_):
    await msg.delete()
    if len(args)>1:return await say(
        'This command requires 2 or 3 arguments.',
        prefix+'move <#Channel> <number of messages> <optional, range of messages>',
        'Example of moving 31 messages to the channel #bot-spam:',
        prefix+'move #bot-spam 31',
        'or moving the messages between and including 10th and 20th messages to the channel #bot-spam:',
        prefix+'move #bot-spam 10 20',
        DM=1
    )
    try:
        webhook = await (await client.fetch_channel(inpChannel)).create_webhook(name=msg.author.display_name)
    except dis.errors.HTTPException:
        for i in await msg.guild.webhooks():
            await (await client.fetch_webhook(i)).delete()
        webhook:dis.Webhook = await (await client.fetch_channel(inpChannel)).create_webhook(name=msg.author.display_name)

    if args:
        history = (await msg.channel.history(limit=args[0]).flatten())[numOfMsgs-1:]
        for i in history[::-1]:
            await i.delete()
    else:
        history = await msg.channel.purge(limit=numOfMsgs)

    await say(f"Please move to <#{inpChannel}>, Where it's way more cozy for this convo :>")

    for i in history[::-1]:
        Sendingtxt=(i.clean_content+'\n'+' '.join(f'||[{z.filename}]({z.url})||' if z.filename.startswith('SPOILER') else f"[{z.filename}]({z.url})"  for z in i.attachments))[:2000]
        async def SenderFunction(x=0):
            if x%100==99:
                asySleep(3)
                return SenderFunction(x)
            if x>500:return"Internet connection is not good enough for moving messages"
            try:
                return await webhook.send(
                    Sendingtxt if Sendingtxt else '** **',
                    wait=1,
                    username=i.author.name,
                    avatar_url=i.author.avatar_url
                )
            except dis.errors.HTTPException as err:
                print(str(err.response))
                await asySleep((lambda t:int(t[0])/1000 if t else 0)(re.findall("'Retry-After': '([0123456789]*)'",str(err.response))))
                return await SenderFunction(x+1)
            except dis.errors.NoMoreItems:
                return"I'm unable to read that far in history, Stopping here."

        msgSent=await SenderFunction()
        if type(msgSent)==str:
            await webhook.delete()
            return msgSent
        
        for j in i.reactions:
            try:
                await msgSent.add_reaction(j)
            except:
                ""
    await webhook.delete()

def ReplyDelay(delay:int,data={},guildID=0,Save=C,**_):
        if not delay.isnumeric():
            return'Time has to be an intiger number'
        data[guildID]['Reply delay']=delay
        Save(data)
        return'done, set reply delay to '+repr(delay)


muteRoleName='MUTED(by Fire-Bot)'
async def MuteMyself(*args:TimeType,prefix='',data={},guildID=0,msg=C,authorID=0,Save=C,**_):
    muteDuration=sum(args)
    if muteDuration<=0:
        return'The time values you provided totalled 0'

    roleobject = dis.utils.get(msg.guild.roles,name=muteRoleName)

    if roleobject is None:
        roleobject = await msg.guild.create_role(
            name=muteRoleName, 
            colour=dis.colour.Color.dark_gray(),
            permissions=dis.Permissions(permissions=0)
        )
        for channel in msg.guild.channels:
            await channel.set_permissions(
                roleobject,
                speak=False,
                send_messages=False,
                read_message_history=True,
                read_messages=False
            )
    await msg.author.add_roles(roleobject)
    data[guildID]['Self Muted']+=(authorID, muteDuration, time()),
    Save(data)
    return f"Done. Muted {msg.author.name} for {' '.join(map(str,args))} ({muteDuration} seconds)"

async def UnmuteCmd(name,msg={},**_):
    mutedPerson=await msg.guild.fetch_member(name)
    mutedRole = dis.utils.get(msg.guild.roles,name=muteRoleName)
    if mutedRole != None:
        await mutedPerson.remove_roles(mutedRole)
        return f"✅ {mutedPerson.name} was unmuted"

def ChannelIDs(msg=C,**_):
    channelsList=[(str(1+i.position),i.name,str(i.id))for i in msg.guild.text_channels]
    lengthEach = [*map(len,map(' '.join,channelsList))]
    formatedCmdsList='\n'.join(' '.join(x[:-1])+y*' '+' '+x[-1] for x,y in zip(channelsList,(max(lengthEach)-i for i in lengthEach)))
    return f'```pos, name, {" "*(max([29]+lengthEach)-29)}ID:\n{formatedCmdsList}```'

def Add8ball(*args,data={},Save=C,guildID=0,**_):
    data[guildID]['8ball']|={' '.join(args)}
    Save(data)
    return'Added'

def SetBotChannels(*args,data={},guildID=0,Save=C,**_):
    if any([1-i.isnumeric()for i in args]):
        return'Not valid channel IDs'
    data[guildID]['Bot channels']={*map(int,args)}
    Save(data)
    return'done'

def AddBotChannels(*args,data={},Save=C,guildID=0,**_):
    data[guildID]['Bot channels']|={*map(int,args)}
    Save(data)
    return'Added'

def DelBotChannels(*args,data={},Save=C,guildID=0,**_):
    data[guildID]['Bot channels']-={*map(int,args)}
    Save(data)
    return'Added'


def List8ball(myData={},**_):
    return'8ball list: '+Join(myData['8ball'])


async def Recommend(arg,*args,client=C,**_):
    await client.get_channel(980859412564553738).send(' '.join((arg,)+args))
    return'Thanks for the recommendation :D'
    
def SetReplyChannels(*args,data={},guildID,Save=C,**_):
    if sum((1-i.isnumeric() for i in args)):
        return'Not valid channel IDs'
    
    data[guildID]['Replies channels']={*map(int,args)}
    Save(data)
    return'done'

def SetReactChannels(args,data={},guildID=0,Save=C,**_):
    if any((1-i.isnumeric() for i in args)):
        return'Not valid channel IDs'
    data[guildID]['Reacts channels']={*map(int,args)}
    Save(data)
    return'done'

async def HighLow(upTo:int,channel=0,authorID=0,client=C,say=C,**_):
    if not upTo.isnumeric():
        return'Arg needs to be intiger'
    await say(f'Game started. Guess a number between 1-{int(upTo)}')
    correct=randint(1,int(upTo))

    guess=-1
    while guess!=correct:
        try:
            guess = int(await client.wait_for(
                "message", 
                check=lambda m:(m.channel.id,m.author.id,m.content.isnumeric()) ==(channel.id,authorID,1),
                timeout=10*60).content)
        except TimeoutError:
            return f'I got impatient waiting so i ended the game'
        if guess<correct:
            await say('Higher!')
        elif guess>correct:
            await say('Lower!')
    return'You won!'

    # make an import react/response x from other discords command
    #TODO make Import command complete
def Import(discordID:ChannelID,*dataSlots,data={},guildID=0,prefix='',Save=C,client=C,**_):
    dataSlot=' '.join(dataSlots)
    options='Responses','Reacts','8ball'
    if dataSlot not in options:
        return('You probably wrote improper syntax. Correct syntax is:',
            f"{prefix}import <which discord> <{'/'.join(options)}>")

    if discordID not in data:
        return"I don't recognize the discord you tried to import from"
        
    data[guildID][dataSlot]|=data[discordID][dataSlot]
    Save(data)
    return f"Imported {dataSlot} from {dis.utils.get(client.guilds,id=discordID).name}"

def ModRoles(*args,data={},guildID=0,Save=C,prefix='',**_):
    # args[0][3:-1] is how to get role ID from role: '<@&975765928333701130>'
    if not args:
        return 'Role IDs: '+Join(data[guildID]["ModRoles"])
    if not args[0].isnumeric():
        return f'Second argument must be an intiger.\n{prefix}AddModRole <roleID>'
    data[guildID]['ModRoles']|={*map(int,args)}
    Save(data)
    return'done'

def RemoveModRoles(arg,*args,data={},guildID=0,Save=C,prefix='',**_):
    if all((i.isnumeric()for i in (arg,*args))):
        data[guildID]['ModRoles']-={*map(int,args[0])}
        Save(data)
        return'done'
    return f'This command all arguments to be role IDs.\n{prefix}RemoveModRoles <RoleID>'

def ListModRoles(myData={},**_):
    return'**Mod roles:**',Join(myData['ModRoles'])

def ListServers(client=C,**_):
    return'list of servers:\n',Join(i.name for i in client.guilds)


async def LeaveVC(msg=C,data={},guildID=0,Save=C,**_):
    if msg.guild.voice_client and msg.guild.voice_client.channel:
        await msg.guild.voice_client.disconnect()
        data[guildID]['MusicPlaylist'] = []
        Save()
        return'Done'
    return'Not in a voice channel.'


async def Play(*args,msg=C,myData={},client=C,data={},guildID=0,**_):
    if not msg.author.voice:
        return"You're not in a voice channel."
    if not args:
        if not myData['MusicPlaylist']:
            return"There is no song playing, so you can't pause/resume."
        vcClient=msg.guild.voice_client
        if vcClient.is_paused():
            await vcClient.resume()
            return'Resumed'
        await vcClient.pause()
        return'Paused'
    video=get_Video(' '.join(args))
    
    data[guildID]['MusicPlaylist']+=[video]
    if not data[guildID]['MusicPlaylist']:
        await msg.author.voice.channel.connect()
        play_song(msg,data,client)
    return'Song added to queue'

async def SkipSong(*args,data={},myData={},client=C,authorID=0,msg=C,guildID=0,**_):
    if not myData['MusicPlaylist']:
        return"There's nothing to skip"
    data[guildID]['MusicSkipVotes'].add(authorID)
    users_in_channel=len([i for i in msg.author.voice.channel.members if not i.bot])
    if users_in_channel:
        voteRatio=len(data[guildID]['MusicSkipVotes'])/users_in_channel
    else:voteRatio=1
    neededVoteRatio=data[guildID]['MusicNeededVoteRatio']
    if voteRatio >= neededVoteRatio:
        data[guildID]['MusicPlaylist'].pop(0)
        msg.channel.guild.voice_client.stop()
        if len(data[guildID]['MusicPlaylist']):
            await msg.author.voice.channel.connect()
            play_song(msg,data,client)
        return"Enough votes, skipped"
    else:
        return f'Not enough votes. Only {int(100*voteRatio)}% want to skip, when {int(100*neededVoteRatio)}% are needed'

async def ForceSkipSong(*args,data={},client=C,msg,guildID=0,**_):
    if not data[guildID]['MusicPlaylist']:
        return"There's nothing to skip"
    data[guildID]['MusicPlaylist'].pop(0)
    msg.channel.guild.voice_client.stop()
    if len(data[guildID]['MusicPlaylist']):
        await msg.author.voice.channel.connect()
        play_song(msg,data,client)
    return"Skiped"


def NowPlaying(myData={},**_):
    if len(myData['MusicPlaylist']) > 0:
        return [f"{len(myData['MusicPlaylist'])} songs in queue:"]+[
            f"  {index+1}. **{song.title}** (requested by **{song.requested_by.name}**)"
            for index, song in enumerate(myData['MusicPlaylist'])
        ]
    return"The play queue is empty."


async def APLCmd(*args,client=C,msg={},prefix='',cmd='',**_):
    if not args:
        return"Nothing to evaluate"
    await client.get_channel(1042892476526100480).send("⋄"+msg.content[1+len(prefix)+len(cmd):])
    try:
        return(await client.wait_for(
            "message",
            check=(lambda m:(m.channel.id,m.author.id)==(1042892476526100480,975728573312802847)),
            timeout=10
        )).content
    except TimeoutError:
        return"Took too long"


async def TicTacToeCmd(say=C,client=C,**_):
    await say('Game started! (Credits to EdelfQ for the game code)')
    await TicTacToe.TurtleGame(client,say)

async def BoardGame(msg=C,say=C,**_):
        embed = dis.Embed(
            title = 'Pick your game! :D',
            description = '\n'.join((
                "Use the buttons below to select what game you'd like me to start for you.",
                "1️⃣ Checkers",
                "2️⃣ TicTacToe"
                #"3️⃣ Connect4",
                #"4️⃣ Chess",
                #"5️⃣ 4player chess",
                #"6️⃣ random",
            )), 
            color=0xE659ff
        )
        embed.set_thumbnail(url=msg.guild.icon_url)
        sentMsg=await say(embed=embed)
        for i in ('1️⃣'): #,'2️⃣','3️⃣','4️⃣','5️⃣','6️⃣'
            await sentMsg.add_reaction(i)


async def Testing(*args,say=C,client=C,**_):
    embed = dis.Embed(
        title = 'Pick your prounoun(s)! :D',
        description = '\n'.join((
            "Use the buttons below to select what pronouns you'd like us to display for you.",
            "Pick however many you'd like, and if none of them suit you, you may message a mod/admin for a custom pronoun role :>",
            "1️⃣ They/Them",
            "2️⃣ She/Her",
            "3️⃣ He/Him",
            "4️⃣ Any",
            "5️⃣ Ask me",
            "6️⃣ custom (bot dms you)"
        )), 
        color=0xE659ff)

    embed.set_thumbnail(url=msg.guild.icon_url)
    sentMsg=await say(embed=embed)
    for i in ('1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣'):
        await sentMsg.add_reaction(i) 
    
    msg = await client.wait_for(
        'reaction_add',
        check=(lambda r,u:(u,str(r.emoji))==(msg.author,'↕')),
        timeout=30
    )

    try:
        reaction, user = await client.wait_for('reaction_add', 
            check=lambda r,u:u==msg.author,
            timeout=60.0
        )
    except:
        return'-'

async def SpoilerMsg(msg:dis.Message=C,say=C,client=C,**_):
    deleted = 0 # for testing if deletion was successful
    while not deleted:
        try:
            await msg.delete()
        except dis.NotFound:
            deleted = 1
        except:
            await asySleep(1)
    try:
        repliedToMsg = await msg.channel.fetch_message(msg.reference.message_id)
    except:
        await say('This command needs you to reply to a message',DM=1)
        return

    if repliedToMsg==None:
        await say('This command needs you to reply to a message',DM=1)
        return
    

    webhook = await msg.channel.create_webhook(name=repliedToMsg.author.display_name)
    
    Sendingtxt='||'+(repliedToMsg.clean_content+'\n'+' '.join(f"[{z.filename}]({z.url})"for z in repliedToMsg.attachments))[:1996]+'||'
    msgSent=await webhook.send(
        Sendingtxt,
        wait=1,
        username=repliedToMsg.author.name,
        avatar_url=repliedToMsg.author.avatar_url
    )
    if msgSent:
        for j in repliedToMsg.reactions:
            await msgSent.add_reaction(j)
    await repliedToMsg.delete()
    await webhook.delete()

async def UnSpoilerMsg(msg:dis.Message=C,say=C,client=C,**_):
    deleted = 0 # for testing if deletion was successful
    while not deleted:
        try:
            await msg.delete()
        except dis.NotFound:
            deleted = 1
        except:
            await asySleep(1)
    try:
        repliedToMsg = await msg.channel.fetch_message(msg.reference.message_id)
    except:
        await say('This command needs you to reply to a message',DM=1)
        return

    if repliedToMsg==None:
        await say('This command needs you to reply to a message',DM=1)
        return

    webhook = await msg.channel.create_webhook(name=repliedToMsg.author.display_name)
    
    Sendingtxt:str = repliedToMsg.clean_content

    if not (Sendingtxt[:2]=='||' and Sendingtxt[-2:]=='||') or repliedToMsg.attachments:
        await say('Make sure the message was spoilered by me (the bot), since in this case the message was not formatted as expected.',DM=1)
        return

    msgSent = await webhook.send(
        Sendingtxt[2:-2],
        wait=1,
        username=repliedToMsg.author.name,
        avatar_url=repliedToMsg.author.avatar_url
    )
    if msgSent:
        for j in repliedToMsg.reactions:
            await msgSent.add_reaction(j)
    await repliedToMsg.delete()
    await webhook.delete()

def ResetDataSlot(*slotName,data={},Save=C,guildID=0,**_):
    slot=' '.join(slotName)
    for i in data[guildID]:
        if slot==i.lower():
            data[guildID][i]=type(data[guildID][i])()
            Save(data)
            return 'Done'
    return "Data slot doesn't exist"

def ListDataSlot(*slotName,data={},guildID=0,**_):
    slot=' '.join(slotName)
    for i in data[guildID]:
        if slot==i.lower():
            return str(data[guildID][i])
    return "Data slot doesn't exist"

async def AskAI(*_,msg:dis.Message=C,**a):
    msg.content:str=msg.content
    await AI.send_message(msg, msg.content[msg.content.index(" ")+1:])

async def AskSmartass(*_,msg:dis.Message=C,**a):
    msg.content:str=msg.content
    await AI.send_message(msg, msg.content[msg.content.index(" ")+1:], smart=True)

def PipInstall(*package,**_):
    os.system(f'pip install {" ".join(package)} --disable-pip-version-check')
    return"done"

def ToggleAI(*a,**_):
    AI.OFF = not AI.OFF
    return f"Done. Set it to {AI.OFF}"

async def JsonOfMyData(*args:list[str], msg=C, author=C, say=C, **_):
    limit = int(args[0]) if args and args[0].isnumeric() else None

    def onEachMsg(x:dis.Message):
        return *map(ascii, (x.content, ' '.join(map(str, x.reactions)), str(x.created_at))),

    async def getChannelData(channel:dis.TextChannel):
        return *map(onEachMsg, await channel.history(limit=limit
            ).filter(lambda m:m.author.id==author.id
            ).flatten()
        ),
    
    await say("Starting, this might take a while.")
    l:list[list] = filter(None,[await getChannelData(i)for i in msg.guild.channels if hasattr(i, "history")])
    text = json.dumps(dict(zip(["content", "reactions", "timestampUTC"],zip(*l))))
    with open("extra/tempjson.json",mode='w')as f:
        f.write(text)
    await say(file=dis.File("extra/tempjson.json"))
#    os.remove("extra/tempjson.json")

cmds={
    'userCommands':{
        'AskAI'            :AskAI,
        'AskSmartass'      :AskSmartass,
        '8ball'            :Ball8,
        'Flip'             :Flip,
        'Help'             :HelpCmd,
        'HighLowGame'      :HighLow,
        'Info'             :InfoCmd,
        'LeaveVC'          :LeaveVC,
        'List8ball'        :List8ball,
        'ListModRoles'     :ListModRoles,
        'ListResponses'    :ListResponses,
        'Metheus'          :Metheus,
        'MuteMyself'       :MuteMyself,
        'Ping'             :C("hiii"),
        'Recommend'        :Recommend,
        'Rick'             :RickRoll,
        'RockPaperScissors':RockPaperScissors,
        'ShowPrefix'       :ShowPrefix,
        'TicTacToe'        :TicTacToeCmd,
        'Zote'             :Zote,
#       'APL'              :APLCmd,
#       'NowPlaying'       :NowPlaying,
#       'Play'             :Play,
#       'Skip'             :SkipSong,
    },
    'modCommands':{
        'Add8ball'        :Add8ball,
        'ChannelIDs'      :ChannelIDs,
        'Move'            :MoveCmd,
        'Remove8ball'     :Curry(DelDataSlot,'8ball'),
        'Unmute'          :UnmuteCmd,
        'SpoilerMessage'  :SpoilerMsg,
        'UnSpoilerMessage':UnSpoilerMsg,
#       'ForceSkip'       :ForceSkipSong,
    },
    'adminCommands':{
        'JsonOfMyData'    :JsonOfMyData,
        'AddBotChannel'   :AddBotChannels,
        'AddModRoles'     :ModRoles,
        'ChangePrefix'    :ChangePrefix,
        'DelBotChannels'  :DelBotChannels,
        'DelReact'        :Curry(DelDataSlot,'Reacts'),
        'DelResponse'     :Curry(DelDataSlot,'Responses'),
        'ModRoles'        :ModRoles,
        'NewResponse'     :NewResponse,
        'Prefix'          :Prefix,
        'RemoveModRoles'  :RemoveModRoles,
        'ReplyDelay'      :ReplyDelay,
        'SetBotChannels'  :SetBotChannels,
        'SetReactChannels':SetReactChannels,
        'SetReplyChannels':SetReplyChannels,

    },
    'ownerCommands':{
        'Error'        :Error,
        'Import'       :Import,
        'PipInstall'   :PipInstall,
        'Backup'       :Backup,
        'BoardGame'    :BoardGame,
        'EmergencyQuit':EmergencyQuit,
        'ListServers'  :ListServers,
        'RestoreBackup':RestoreBackup,
        'Testing'      :Testing,
        'Update'       :Update,
        'ResetDataSlot':ResetDataSlot,
        'ListDataSlot' :ListDataSlot,
        'ToggleAI'     :ToggleAI,
    }
}

# Testing section:
if __name__=="__main__":

    # Make sure there are no invalid KWARGS for the commands
    kwargKeys='msg','cmd','say','data','Save','cmds','isMod','myData','reacts','prefix','client','allArgs','guildID','channel','isOwner','isAdmin','isLinux','botPath','modRoles','argCount','authorID','codePath','channelID','responses','extraPath','hasInfArgs','replyDelay','botChannels','isBotChannel','replyChannels','savestatePath','reactsChannels','chanceForReply','isReplyChannel','isReactChannel','isReactChannel','isReactChannel','isReactChannel','author'
    for i in cmds:
        for j in cmds[i]:
            ValidKWARGForFunc(cmds[i][j],{i:0 for i in kwargKeys})