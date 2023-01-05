# syntax for writing emotes is <:shroompause:976245280041205780> btw
from asyncio import sleep as asySleep
from asyncio import create_task
import os
import discord as dis
from random import random
from shutil import rmtree, copytree
from imports import vars, fns, maddyTimer
from imports.cmdFns import cmds
from time import sleep, time

os.chdir(__file__[:-len(os.path.basename(__file__))])
# region variable definitions

# region paths
isLinux=__file__[0]!='c'
mainPath      = '../../'
tokenPath     = mainPath+'Safe/Fire-Owl-bot.yaml'
savestatePath = mainPath+'data/Fire-Owl-data'
extraPath     = mainPath+'Fire-Owl-bot/code/extra/'
botPath       = mainPath+'Fire-Owl-bot/'
codePath      = botPath+'code/'
datatxtPath   = extraPath+'data.txt'
# endregion

# load backup
if os.path.exists(extraPath):
    rmtree(extraPath)
    sleep(0.1)
copytree(savestatePath, extraPath)

client = dis.Client(intents = dis.Intents.all())

cmdsL={j:{i.lower():cmds[j][i] for i in cmds[j]} for j in cmds}

# Music settings
max_volume=250 # Max audio volume. Set to -1 for unlimited.


# Data setup
def Save(d):fns.openW(datatxtPath,d)

data:dict[int,dict[str]] = fns.openR(datatxtPath)

# Fill in new settings that could have been added
for guild in data:
    for setting in vars.defaultGuildSettings:
        if setting not in data[guild]:
            data[guild][setting]=vars.defaultGuildSettings[setting]
Save(data)

# General globals
replyDelayList=set()
muteRoleName='MUTED(by Fire-Bot)'

# endregion

async def on_ready():
    if isLinux:
        create_task(maddyTimer.maddyTimerMain(client))
    await client.change_presence(activity=dis.Game(f'subscribe to FIRE OWL'))
    print('Logged in as',
        client.user.name,
        client.user.id,
        f'In {len(client.guilds)} servers',
        '------', sep='\n')
    try:
        while 1:
            # Code for unmuting muted people when their time is up
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
                    data[guildID]['Self Muted']=[j for i,j in zip(x,data[guildID]['Self Muted']) if not i]
                    Save(data)
            await asySleep(10)
    except:
        print("on_ready() stopped")
        (await client.fetch_channel(980859412564553738)).send('The on_ready() startup function crashed. Routines stopped.')

async def on_message(msg:dis.Message):
    if msg.author.bot:
        return
    if not(isLinux or msg.content.lower().startswith("test")):
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

    if not msg.guild: return await say("I don't work in DMs sadly.",DM=1)

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
    authorID       :int                = msg.author.id
    isOwner        :bool               = authorID == 671689100331319316
    isAdmin        :bool               = msg.author.top_role.permissions.administrator or isOwner
    isMod          :bool               = isAdmin or any(i.id in modRoles for i in msg.author.roles)
    isBotChannel   :bool               = channel.id in botChannels    or not botChannels
    isReplyChannel :bool               = channel.id in replyChannels  or not replyChannels
    isReactChannel :bool               = channel.id in reactsChannels or not reactsChannels

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
        
        if not (isBotChannel or
            channel.id not in replyDelayList
            and isReplyChannel
            and random()<=chanceForReply):
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
                    replyDelayList.add(channel.id)
                    await asySleep(replyDelay)
                    replyDelayList.remove(channel.id)
                    break
        return

    if (0,0)==(isBotChannel,isMod):
        return

    allowedCmdsL=cmdsL['userCommands']\
               |(cmdsL['modCommands']if isMod else{})\
               |(cmdsL['adminCommands']if isAdmin else{})\
               |(cmdsL['ownerCommands']if isOwner else{})
    
    if cmd == prefix:
        cmd='help'
    else:
        posValues=*filter(lambda i:i.startswith(cmd[len(prefix):].lower()),allowedCmdsL.keys()),
        if len(posValues)==1:
            cmd=posValues[0]
        else:
            cmd=''
            r=0 if posValues else posValues

    if cmd in allowedCmdsL:
        argCount=fns.ArgCount(allowedCmdsL[cmd])
        hasInfArgs=fns.HasInfArgs(allowedCmdsL[cmd])
        hasInfKWArgs=fns.HasInfKWArgs(allowedCmdsL[cmd])
        KWARGS={
            'msg':msg,
            'cmd':cmd,
            'say':say,
            'data':data,
            'Save':Save,
            'cmds':cmds,
            'isMod':isMod,
            'myData':myData,
            'reacts':reacts,
            'prefix':prefix,
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
            'responses':responses,
            'extraPath':extraPath,
            'hasInfArgs':hasInfArgs,
            'replyDelay':replyDelay,
            'botChannels':botChannels,
            'isBotChannel':isBotChannel,
            'hasInfKWArgs':hasInfKWArgs,
            'replyChannels':replyChannels,
            'savestatePath':savestatePath,
            'reactsChannels':reactsChannels,
            'chanceForReply':chanceForReply,
            'isReplyChannel':isReplyChannel,
            'isReactChannel':isReactChannel,
            'isReactChannel':isReactChannel,
            'isReactChannel':isReactChannel,
            'isReactChannel':isReactChannel,
        }
        errored,reTypedArgs=await fns.FitIntoFunc(allowedCmdsL[cmd],client,args,KWARGS)
        if errored:
            r=reTypedArgs
        elif isLinux:
            try:
                if hasInfKWArgs:
                    r=await fns.intoAsync(allowedCmdsL[cmd])(*reTypedArgs,**KWARGS)
                else:
                    r=await fns.intoAsync(allowedCmdsL[cmd])(*reTypedArgs)

            except Exception as e:
                r='Error',e,f'```{e.__class__}```'
        else:
            if hasInfKWArgs:
                r=await fns.intoAsync(allowedCmdsL[cmd])(*reTypedArgs,**KWARGS)
            else:
                r=await fns.intoAsync(allowedCmdsL[cmd])(*reTypedArgs)
            # I split by isLinux so i can get clear errors on my windows machine
            # but get errors from discord through my linux machine

    if not r:
        return
    if not hasattr(r,'__iter__') or type(r)==str:
        r=r,
    await say(*r)

async def on_reaction_add(reaction, author):
    ...

*map(client.event,(
    on_ready,
    on_message,
    on_reaction_add
)),
from yaml import safe_load
with open(tokenPath, encoding='utf-8') as f:
    client.run(safe_load(f)['Token'])