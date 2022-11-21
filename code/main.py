from asyncio import sleep as asySleep
import os
import discord as dis
from random import randint,random,choice
from shutil import rmtree, copytree
# redifine the default vars function to be uppercase.
# no idea why it's colored green by syntax highlighting. It's a function
Vars=vars
from imports import vars, fns
from imports.cmdFns import cmdFns
from imports.fns import Join
from time import sleep, time
from imports import TicTacToe
os.chdir(__file__[:-len(os.path.basename(__file__))])
muteRoleName='MUTED(by Fire-Bot)'
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
# spamPing=set()

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

    def If(cond:bool,i:set)->set:
        return (set(),i)[cond]
    
    commands=cmds['userCommands']\
        |If(isOwner,cmds['ownerCommands'])\
        |If(isAdmin,cmds['adminCommands'])\
        |If(isMod,cmds['modCommands'])
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
            'allArgs':allArgs,
            'guildID':guildID,
            'channel':channel,
            'isOwner':isOwner,
            'isAdmin':isAdmin,
            'modRoles':modRoles,
            'argCount':argCount,
            'authorID':authorID,
            'channelID':channelID,
            'responses':responses,
            'hasInfArgs':hasInfArgs,
            'replyDelay':replyDelay,
            'botChannels':botChannels,
            'isBotChannel':isBotChannel,
            'replyChannels':replyChannels,
            'reactsChannels':reactsChannels,
            'chanceForReply':chanceForReply,
            'isReplyChannel':isReplyChannel,
            'isReactChannel':isReactChannel,
            'extraPath':extraPath,
            'savestatePath':savestatePath,
            'isLinux':isLinux,
            'codePath':codePath,
            'botPath':botPath,
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

    elif cmd == 'backup':
        rmtree(savestatePath)
        copytree(extraPath, savestatePath)
        r='You backuped the files: '+Join(os.listdir(extraPath))
    
    elif cmd == 'zote':
        r=choice(vars.zoteQuotes)

    elif cmd == 'emergencyquit':
        await say("I'm sorry for what i did :(\nBye lovely folks!")
        asySleep(0.5)
        quit()

    elif cmd == 'metheus':
        await say('Keep in mind this is a command for a spesific game called the Metheus Puzzle (<https://dontstarve-archive.fandom.com/wiki/Metheus_Puzzles>)')
        await fns.metheus(client,msg,say,throw)
    
    elif cmd == 'replydelay':
        if not args: r='Remember to add a delay time in seconds'
        elif not args[0].isnumeric(): r='Time has to be an intiger number'
        else:
            r=f'done, set reply delay to {args[0]}'
            data[guildID]['Reply delay'] = int(args[0])
            Save(data)

    elif cmd == 'makefile':
        if len(args)<2:
            r=f'Not correct syntax\n{prefix}makefile <fileName> <contents>'
        else:
            fns.openW(extraPath+args[0],args[1])
            r=f'You wrote file {args[0]} with the contents {args[1]}'
    
    elif cmd == 'listfiles':
        r=Join(os.listdir(extraPath))
    
    elif cmd == 'move':
        await msg.delete()
        if len(args)not in(2,3):
            return await say(f'This command requires 2 arguments.\n{prefix}move <#Channel> <number of messages>',DM=1)

        if not args[0][2:-1].isnumeric():
            return await say(
                'Channel ID was invalid. remember to do #ChannelName',
                DM=1
            )

        if not args[1].isnumeric() or args[2:] and not args[2].isnumeric():
            return await say(
                'Number of messages to move was invalid. remember to do have it as a intiger',
                DM=1
            )
        webhook = await (await client.fetch_channel(int(args[0][2:-1]))).create_webhook(name=msg.author.display_name)
        
        if args[2:]:
            history = (await msg.channel.history(limit=int(args[2])).flatten())[int(args[1])-1:]
            for i in history[::-1]:
                await i.delete()
        else:
            history = await msg.channel.history(limit=int(args[1])).flatten()
            await msg.channel.purge(
                limit=int(args[1])
            )

        await say(f"Please move to {args[0]}, Where it's way more cozy for this convo :>")

        for i in history[::-1]:
            Sendingtxt=(i.clean_content+'\n'+' '.join(f"[{z.filename}]({z.url})" for z in i.attachments))[:2000]

            msgSent=await webhook.send(
                Sendingtxt if Sendingtxt else '** **',
                wait=1,
                username=i.author.name,
                avatar_url=i.author.avatar_url)
            for j in i.reactions:
                await msgSent.add_reaction(j)
        await webhook.delete()


    elif cmd == 'unmute':
        if not args:
            return await say("Please specify the name of the member in the command")
        mutedPerson=await msg.guild.fetch_member(args[0])
        mutedRole = dis.utils.get(msg.guild.roles,name=muteRoleName)
        if mutedRole != None:
            await mutedPerson.remove_roles(mutedRole)
            await msg.channel.send(f"✅ {mutedPerson.name} was unmuted")

    elif cmd == 'mutemyself':
        # changed
        IsValidTime = lambda i:i[-1] in "smhd" and i[:-1].isnumeric()
        if not (args and all(map(IsValidTime,args))):
            return await say(
                'Wrong syntax. Please rephrase the command like so:',
                f'{prefix}muteMyself <num+s> <num+m> <num+h> <num+d>',
                "They can be in any order you'd like :D, example:",
                f'{prefix}MuteMyself 3d 4h 5m 2s'
            )

        muteDuration=fns.getTime(args)
        if muteDuration<=0:
            return await say('The time values you provided totalled 0')

        roleobject = dis.utils.get(msg.guild.roles,name=muteRoleName)

        if roleobject is None:
            roleobject = await msg.guild.create_role(
                name=muteRoleName, 
                colour=dis.colour.Color.dark_gray(),
                permissions=dis.Permissions(permissions=0)
            )
            for channel in msg.guild.channels:
                await channel.set_permissions(roleobject, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await say(f"Done. Muted {msg.author.name} for {' '.join(args)} ({muteDuration} seconds)")
        await msg.author.add_roles(roleobject)

        data[guildID]['Self Muted']=data[guildID]['Self Muted']+(authorID, muteDuration, time()),
        Save(data)

    elif cmd == 'channelids':
        channelsList=[(str(1+i.position),i.name,str(i.id)) for i in msg.guild.text_channels]
        lengthEach = [*map(len,map(' '.join,channelsList))]
        formatedCmdsList='\n'.join(' '.join(x[:-1])+y*' '+' '+x[-1] for x,y in zip(channelsList,(max(lengthEach)-i for i in lengthEach)))
        r=f'```pos, name, {" "*(max([29]+lengthEach)-29)}ID:\n{formatedCmdsList}```'
        if len(r)>2000: r=r[:1990]+'```'

    elif cmd=='setbotchannels':
        if any([not i.isnumeric() for i in args]):
            r='Not valid channel IDs'
        else:
            data[guildID]['Bot channels']=set(map(int,args))
            Save(data)
            r ='done'

    elif cmd=='setreplychannels':
        if sum((not i.isnumeric() for i in args)):
            r='Not valid channel IDs'
        else:
            data[guildID]['Replies channels']=set(map(int,args))
            Save(data)
            r ='done'

    elif cmd=='setreactchannels':
        if sum((not i.isnumeric() for i in args)):
            r='Not valid channel IDs'
        else:
            r='done'
            data[guildID]['Reacts channels']=set(map(int,args))
            Save(data)
    
    elif cmd == 'recommend':
        if []==args:
            return await throw(f'Remember to recommend something:\n{prefix}recommend Make the bot better!')
        await client.get_channel(980859412564553738).send(' '.join(args))
        r='Thanks for the recommendation :D'
    
    elif cmd=='highlow':
        x = int(args[0]) if args and args[0].isnumeric() else 100
        await say(f'Game started. Guess a number between 1-{x}')
        correct=randint(1,x)

        def check(msg):
            return\
            msg.channel.id == channelID and\
            msg.author.id == authorID and\
            msg.content.isnumeric()

        guess=-1
        while guess!=correct:
            try:
                guess = int(await client.wait_for("message", check=check, timeout=10*60).content)
            except:
                return await say(f'I got impatient waiting for {msg.author.name}')
            if guess<correct:
                await say('Higher!')
            elif guess>correct:
                await say('Lower!')
        r='You won!'

    elif cmd=='add8ball':
        if args:
            data[guildID]['8ball']|={' '.join(args)}
            Save(data)
            r='Added'
        else:
            r='8ball list: '+Join(data[guildID]['8ball'])

    # make an import react/response x from other discords command
    #TODO make Import command complete
    elif cmd=='import':
        options='Responses','Reacts','8ball'
        if len(args)!=2 or (not args[0].isnumeric()):
            r='You probably wrote improper syntax. Correct syntax is:',
            f"fo!import <which discord:id> <{'/'.join(options)}>"

        elif int(args[0]) not in data:
            r="I don't recognize the discord you tried to import from"
        
        elif args[1] not in options:
            r="I don't recognize the thing you tried to import. (argument 2).",
            f"Available options are: {Join(options)}"
        else:
            data[guildID][args[1]]|=data[int(args[0])][args[1]]
            Save(data)
            r=f"Imported {args[1]} from {dis.utils.get(client.guilds,id=int(args[0])).name}"

    # elif cmd=='spamme':
    #     global spamPing
    #     if authorID in spamPing:
    #         spamPing.remove(authorID)
    #         r='Ok i stopped spamming :D'
    #     else:
    #         await say('I will now spam you :D')
    #         spamPing.add(authorID)
    #         while authorID in spamPing:
    #             asySleep(5)
    #             await msg.author.send('This is spam ping')

    elif cmd=='list8ball':
        r='8ball list: '+Join(data[guildID]['8ball'])

    elif cmd == 'remove8ball':
        if args:
            if ' '.join(args) in data[guildID]['8ball']:
                data[guildID]['8ball'].remove(' '.join(args))
                r='Removed'
                Save(data)
            else:
                r='There was no reply found'
        else: 
            r='8ball list: '+Join(data[guildID]['8ball'])

    elif cmd == 'addmodrole': # args[0][3:-1] is how to get role ID from role: '<@&975765928333701130>'
        if not args:
            r=f'Role IDs:\n{data[guildID]["ModRoles"]}'
        elif args[0].isnumeric():
            data[guildID]['ModRoles']|={int(args[0])}
            Save(data)
            r='done'
        else:
            r=f'Second argument must be an intiger.\n{prefix}AddModRole <roleID>'

    elif cmd == 'removemodrole':
        if args and args[0].isnumeric():
            data[guildID]['ModRoles'].remove(int(args[0]))
            Save(data)
            r='done'
        else:
            r=f'This command requires one extra argument.\n{prefix}RemoveModRole <RoleID>'
    
    elif cmd == 'listmodroles':
        r='Mod roles:\n',Join(myData['ModRoles'])
        
    elif cmd == 'listservers':
        r='list of servers:\n',Join(i.name for i in client.guilds)

    elif cmd == 'leavevc':
        if msg.guild.voice_client and msg.guild.voice_client.channel:
            await msg.guild.voice_client.disconnect()
            data[guildID]['MusicPlaylist'] = []
        else:
            r="Not in a voice channel."
    
    elif cmd == 'play':
        if not msg.author.voice:
            return await throw("You're not in a voice channel.")
        if not args:
            if data[guildID]['MusicPlaylist']:
                (lambda x:x.resume() if x.is_paused() else x.pause())(
                    msg.guild.voice_client
                )
            else:
                await throw("There is no song playing, so you can't pause/resume.")
            return
        video=fns.get_Video(' '.join(args))
        await say(video.keys())

        data[guildID]['MusicPlaylist']+=[video]
        await say('Song added to queue')
        if not data[guildID]['MusicPlaylist']:
            await msg.author.voice.channel.connect()
            fns._play_song(msg,data,client)
    
    elif cmd == 'skip':
        if not data[guildID]['MusicPlaylist']:
            return await throw("There's nothing to skip")
        data[guildID]['MusicSkipVotes'].add(authorID)
        users_in_channel = len([i for i in msg.author.voice.channel.members if not i.bot])
        if users_in_channel:
            voteRatio=len(data[guildID]['MusicSkipVotes'])/users_in_channel
        else:voteRatio=1
        neededVoteRatio=data[guildID]['MusicNeededVoteRatio']
        if voteRatio >= neededVoteRatio:
            r="Enough votes, skipping..."
            data[guildID]['MusicPlaylist'].pop(0)
            channel.guild.voice_client.stop()
            if len(data[guildID]['MusicPlaylist']):
                await msg.author.voice.channel.connect()
                fns._play_song(msg,data,client)
        else:
            r=f'Not enough votes. Only {int(100*voteRatio)}% want to skip, when {int(100*neededVoteRatio)}% are needed'
    elif cmd in {'fs','forceskip'}:
        if not data[guildID]['MusicPlaylist']:
            return await throw("There's nothing to skip")
        r="Skipping..."
        data[guildID]['MusicPlaylist'].pop(0)
        channel.guild.voice_client.stop()
        if len(data[guildID]['MusicPlaylist']):
            await msg.author.voice.channel.connect()
            fns._play_song(msg,data,client)

    elif cmd == 'nowplaying':
        if len(data[guildID]['MusicPlaylist']) > 0:
            r = [f"{len(data[guildID]['MusicPlaylist'])} songs in queue:"]+[
                f"  {index+1}. **{song.title}** (requested by **{song.requested_by.name}**)"
                for index, song in enumerate(data[guildID]['MusicPlaylist'])
            ]
        else:
            r="The play queue is empty."
    
    elif cmd == 'apl':
        if []==args: return await say("Nothing to evaluate")
        await client.get_channel(1042892476526100480).send("⋄"+msg.content[1+len(prefix)+len(cmd):])
        try:
            r = (await client.wait_for(
                "message",
                check=(lambda m:(m.channel.id,m.author.id)==(1042892476526100480,975728573312802847)),
                timeout=10
            )).content
        except:
            r = "Took too long"
    
    elif cmd=='tictactoe':
        await say('Game started! (Credits to EdelfQ for the game code)')
        await TicTacToe.TurtleGame(client,say)

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