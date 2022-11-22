from asyncio import sleep as asySleep
import os
import discord as dis
from random import random
from shutil import rmtree, copytree
# redifine the default vars function to be uppercase.
# no idea why it's colored green by syntax highlighting. It's a function
Vars=vars
from imports import vars, fns
from imports.cmdFns import cmdFns
from time import sleep, time
from imports import TicTacToe
os.chdir(__file__[:-len(os.path.basename(__file__))])

client = dis.Client()

    #RPS = ['rock','paper','scissors']
    #if not args or args[0] not in RPS:
    #    return await throw(f'The command only accepts '+Join(RPS),(1,))

    #userChoice = args[0].lower()
    #botChoice = choice(RPS)
    #reply=fns.rps(userChoice,botChoice)
    #r=f'You chose **{userChoice}**. I (the bot) chose **{botChoice}**.\n{reply}'

isLinux=__file__[0]!='c'
mainPath      = '../../'
tokenPath     = mainPath+'Safe/Fire-Owl-bot.yaml'
savestatePath = mainPath+'data/Fire-Owl-data'
extraPath     = mainPath+'Fire-Owl-bot/code/extra/'
botPath       = mainPath+'Fire-Owl-bot/'
codePath      = botPath+'code/'
datatxtPath   = extraPath+'data.txt'

# load backup
if os.path.exists(extraPath):
    rmtree(extraPath)
    sleep(0.1)
copytree(savestatePath, extraPath)


cmds = {
    'userCommands':{
        'Help', 'Flip', 'rps','ListResponses','Info','hkWiki','Recommend',
        'Rick','Zote','MuteMyself','List8Ball','Metheus',
        'Play','Skip','NowPlaying','Leavevc','APL',
        'TicTacToe' 
        # music commands to add:::
        # playlists, 
    },

    'modCommands':{
        'Move','ListModRoles', 'Unmute'
    },

    'adminCommands':{
        'NewResponse','DelResponse','DelReact','SetReplyChannels',
        'SetReactChannels','SetBotChannels','ChannelIDs','Prefix','addModRole',
        'ReplyDelay','ReplyChance','Add8ball','remove8ball',
        'removemodrole'

        # daily polls
    },

    'ownerCommands':{
        'Update','EmergencyQuit','MakeFile','ListFiles','Backup',
        'RestoreBackup','Testing','Highlow','ListServers','Eval'

        'importreplies','boardgame' # work in  progress
    }
}
JoinDict=lambda x,y:{i:x[i]|y[j]for i,j in zip(x,y)}
cmds=JoinDict(cmds,{i:cmdFns[i].keys() for i in cmdFns})

cmdFnsL={j:{i.lower():cmdFns[j][i] for i in cmdFns[j]} for j in cmdFns}
allCmdFnsL=fns.SToF('|')(*[cmdFnsL[i]for i in cmdFnsL])

# Music settings:
max_volume=250 # Max audio volume. Set to -1 for unlimited.

data:dict[int,dict[str]] = fns.openR(datatxtPath)

def Save(d):
    fns.openW(datatxtPath,d)

for guild in data:
    for setting in vars.defaultGuildSettings:
        if setting not in data[guild]:
            data[guild][setting]=vars.defaultGuildSettings[setting]
Save(data)

replyDelayList=set()

muteRoleName='MUTED(by Fire-Bot)'

async def on_ready():
    await client.change_presence(activity=dis.Game(f'subscribe to FIRE OWL'))
    print('Logged in as',
    client.user.name,
    client.user.id,
    f'In {len(client.guilds)} servers',
    '------', sep='\n')
    while 1:
        for guildID in data:
            x=[]
            for MutedUserID,muteDuration,timeWhenStarted in data[guildID]['Self Muted']: # msg, muteDuration, time()
                x+=[0]
                if muteDuration<time()-timeWhenStarted:
                    x[-1]=1
                    MutedUserGuild=await client.fetch_guild(guildID)
                    mutedRole = dis.utils.get(MutedUserGuild.roles,name=muteRoleName)
                    if mutedRole != None:
                        MutedUser:dis.Member = await MutedUserGuild.fetch_member(MutedUserID)
                        await MutedUser.remove_roles(mutedRole)
                        await MutedUser.send(f"✅ You are unmuted from "+MutedUserGuild.name)
            if any(x):
                data[guildID]['Self Muted']=*(j for i,j in zip(x,data[guildID]['Self Muted']) if not i),
                Save(data)
        await asySleep(10)
# syntax for writing emotes is <:shroompause:976245280041205780> btw

async def on_message(msg:dis.Message):
    if msg.author.bot:
        return
    if not(isLinux or msg.content.startswith("test")):
        return
    if len(msg.content.split())==0:
        return
    async def say(*values,sep='\n',DM=False,**KWARGS):
        textToBeSent=sep.join(map(str,values))
        if textToBeSent.endswith('```') and len(textToBeSent)>2000:
            textToBeSent=textToBeSent[:1997]+'```'
        elif len(textToBeSent)>2000:
            textToBeSent=textToBeSent[:2000]
        return await (msg.channel,msg.author)[DM].send(textToBeSent,**KWARGS)

    if not msg.guild: return say("I don't work in DMs sadly.",DM=1)

    guildID:int = msg.guild.id
    global data
    if guildID not in data:
        data[guildID] = vars.defaultGuildSettings
        Save(data)
    myData=data[guildID]
    botChannels    :set[int]           = myData['Bot channels']
    reactsChannels :set[int]           = myData['Reacts channels']
    replyChannels  :set[int]           = myData['Replies channels']
    modRoles       :set[int]           = myData['ModRoles']
    responses      :set[dict[str:str]] = myData['Responses']
    reacts         :set[dict[str:str]] = myData['Reacts']
    prefix         :str                = ("test!",myData['Prefix'])[isLinux]
    replyDelay     :int                = myData['Reply delay']
    chanceForReply :float              = myData['Chance for reply']
    allArgs=cmd,*args                  = msg.content.lower().split()
    channel        :dis.ChannelType    = msg.channel
    channelID      :int                = channel.id
    author         :dis.User           = msg.author
    authorID       :int                = author.id
    isOwner        :bool               = authorID == 671689100331319316
    isAdmin        :bool               = msg.author.top_role.permissions.administrator or isOwner
    isMod          :bool               = isAdmin or any(i.id in modRoles for i in msg.author.roles)
    isBotChannel   :bool               = channelID in botChannels    or not botChannels
    isReplyChannel :bool               = channelID in replyChannels  or not replyChannels
    isReactChannel :bool               = channelID in reactsChannels or not reactsChannels

    # r will be the reply message  
    r=''
    if not cmd.startswith(prefix):

        if isReactChannel or isBotChannel:
            for react in reacts:
                if fns.InV2(react,allArgs):
                    await msg.add_reaction(reacts[react])
            # if data[guildID]['React spam'] and isBotChannel:
            #     emotes=[i.name for i in client.emojis]
            #     for i in allArgs:
            #         if i in emotes:
            #             await msg.add_reaction(f'<:{i}:{dis.utils.get(client.emojis,name=i).id}>')

        global replyDelayList
        
        if not(channelID not in replyDelayList and isReplyChannel and random()<=chanceForReply or isBotChannel):
            return

        for x in responses:
            if fns.InV2(x,allArgs):
                if 1000<len(responses[x]):
                    embedVar = dis.Embed(color=0x336EFF)
                    for i in range(0,len(responses[x]),1000):
                        embedVar=embedVar.add_field(name='*', value=responses[x][i:i+1000], inline=False)
                    await msg.channel.send(embed=embedVar)
                else: await say(responses[x])
                if not isBotChannel:
                    replyDelayList.add(channelID)
                    await asySleep(replyDelay)
                    replyDelayList.remove(channelID)
                    break
        return

    if (0,0)==(isBotChannel,isMod):
        return

    commands=cmds['userCommands']\
        |fns.If(isOwner,cmds['ownerCommands'])\
        |fns.If(isAdmin,cmds['adminCommands'])\
        |fns.If(isMod,cmds['modCommands'])
    commands={i.lower() for i in commands}
    cmd = fns.commandHandler(prefix,cmd,commands,ifEmpty='help')

    async def throw(error,whichArgs=()):
        errormsg=[error,' '.join('__'+j+'__' if i in whichArgs else j for i,j in enumerate(allArgs))]
        if any((cmd in cmds[i]for i in('adminCommands','modCommands','ownerCommands'))):
            await msg.delete()
            await say(*errormsg,DM=1)
        else:
            await say(*errormsg) 

    if cmd in allCmdFnsL:
        argCount=fns.ArgCount(allCmdFnsL[cmd])
        hasInfArgs=fns.HasInfArgs(allCmdFnsL[cmd])
        KWARGS={
            'msg':msg,
            'cmd':cmd,
            'say':say,
            'cmds':cmds,
            'data':data,
            'Save':Save,
            'isMod':isMod,
            'throw':throw,
            'myData':myData,
            'reacts':reacts,
            'prefix':prefix,
            'author':author,
            'client':client,
            'allArgs':allArgs,
            'guildID':guildID,
            'channel':channel,
            'isOwner':isOwner,
            'isAdmin':isAdmin,
            'isLinux':isLinux,
            'botPath':botPath,
            'modRoles':modRoles,
            'argCount':argCount,
            'authorID':authorID,
            'codePath':codePath,
            'channelID':channelID,
            'responses':responses,
            'extraPath':extraPath,
            'hasInfArgs':hasInfArgs,
            'replyDelay':replyDelay,
            'botChannels':botChannels,
            'isBotChannel':isBotChannel,
            'replyChannels':replyChannels,
            'savestatePath':savestatePath,
            'reactsChannels':reactsChannels,
            'chanceForReply':chanceForReply,
            'isReplyChannel':isReplyChannel,
            'isReactChannel':isReactChannel,
        }
        if argCount>len(args):
            r=(f'You input too few arguments for the command "{cmd}".',
               f'The command needs minimum {argCount} arguments, not {len(args)}')
        elif not hasInfArgs and argCount<len(args):
            r=(f'Too many arguments for the command "{cmd}".',
               f'The command needs {argCount} arguments, not {len(args)}')
        elif isLinux:
            try:
                r=await fns.Call(allCmdFnsL[cmd],*args,**KWARGS)    
            except Exception as e:
                r='Error',e,f'```{e.__class__}```'
        else:
            r=await fns.Call(allCmdFnsL[cmd],*args,**KWARGS)  
            # I split by isLinux so i can get clear errors on my windows machine
            # but get errors from discord through my linux machine

    elif cmd == 'testing':
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
    

    elif cmd == 'boardgame':
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

        msg = await client.wait_for(
            'reaction_add',
            check=(lambda r,u:(u,str(r.emoji))==(msg.author,'↕')),
            timeout=30
        )

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except:
            await channel.send('-')

    elif cmd == 'eval':
        r=eval(msg.content[len(prefix)+4:])

    else:r='That is not a valid command'

    if r=='':return
    if not hasattr(r,'__iter__') or type(r)==str:r=[r]
    await say(*r)


async def on_reaction_add(reaction, author):
    if author.bot:return
    reaction.message
    if reaction.emoji == '📩':1


*map(client.event,(
    on_ready,
    on_message,
    on_reaction_add
)),
from yaml import safe_load
with open(tokenPath, encoding='utf-8') as f:
    client.run(safe_load(f)['Token'])