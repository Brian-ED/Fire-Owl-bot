from asyncio import sleep as asySleep
import os
import discord as dis
from random import randint,random
from shutil import rmtree, copytree
import imports.functions as fns
import imports.vars as Vars
DEBUG=0
from time import sleep
os.chdir(__file__[:-len(os.path.basename(__file__))])
client = dis.Client()

isLinux=__file__[0]!='c'
mainPath      = '../../' if isLinux else 'C:/Users/brian/Persinal/discBots/'
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
        '8ball', 'Help', 'Roll', 'Flip', 'rps','yt','Google',
        'Youtube','ListResponses','Info','hkWiki','Recommend',
        'Rick','Zote','muteMyself','SpamMe','List8Ball','metheus',
        'play','skip','nowplaying','leavevc'
        # music commands to add:::
        # playlists, 
    },

    'modCommands':{
        'Move','listmodroles'
    },

    'adminCommands':{
        'NewResponse','DelResponse','DelReact','SetReplyChannels',
        'SetReactChannels','SetBotChannels','ChannelIDs','Prefix','addModRole',
        'ReplyDelay','ReplyChance','ToggleReactSpam','Add8ball','remove8ball',
        'removemodrole'

        # daily polls
    },


    'VIPCommands':{
        486619954745966594:{'EmergencyQuit'} # Fire Owl
    },

    'ownerCommands':{
        'Update','EmergencyQuit','MakeFile','ListFiles','Backup',
        'RestoreBackup','Testing','Highlow','ListServers',

        'importreplies' # work in  progress

        'boardgame'
    }
}

# Music settings:
max_volume=250 # Max audio volume. Set to -1 for unlimited.

data:dict[int,dict[str]] = fns.openR(datatxtPath)

def Save(d):
    fns.openW(datatxtPath,d)

for guild in data:
    for setting in Vars.defaultGuildSettings:
        if setting not in data[guild]:
            data[guild][setting]=Vars.defaultGuildSettings[setting]
Save(data)

replyDelayList=set()
spamPing=set()

def randItem(i):
    return list(i)[randint(0,len(i)-1)]

def Join(i):
    return ', '.join(sorted(i))

@client.event
async def on_ready():
    await client.change_presence(activity=dis.Game(f'subscribe to FIRE OWL'))
    print('Logged in as',
    client.user.name,
    client.user.id,
    f'In {len(client.guilds)} servers',
    '------', sep='\n')

genderChatCopyPasta="""Alright I’m just gonna throw this out there so we can drop it. Gender chat was a terrible idea to begin with and it won’t be coming back. It took something that is meant to be acknowledged, accepted, and moved on and put it on a pedestal for discussion an argument like it was some sort of science experiment to be observed. It’s a complex subject matter which many people have complex and naturally different views on, with what it is, where it comes from, if it’s inherent, to some if it even exists. Blaming people for having a view that doesn’t conform to yours isn’t great, and neither is blaming people for the channel being a bad idea to begin with, its not much short of just belief based discrimination. It’s was never a good idea, and it wouldn’t be a good idea to reinstate. Period. Now let’s all drop it"""

# syntax for writing emotes is <:shroompause:976245280041205780> btw
@client.event
async def on_message(msg:dis.Message):
    if msg.author.bot:return
    if DEBUG and msg.guild.id!=998681444253704353:return #831963301289132052

    async def say(*values,sep='\n',DM=False,**KWARGS):
        return await (msg.channel,msg.author)[DM].send(sep.join(map(str,values)),**KWARGS)

    if not msg.guild: return say("I don't work in DMs sadly.",DM=1)

    guildID:int = msg.guild.id
    global data
    if guildID not in data:
        data[guildID] = Vars.defaultGuildSettings
        Save(data)
    myData=data[guildID]
    botChannels    :set[int]           = myData['Bot channels']
    reactsChannels :set[int]           = myData['Reacts channels']
    replyChannels  :set[int]           = myData['Replies channels']
    modRoles       :set[int]           = myData['ModRoles']
    responses      :set[dict[str:str]] = myData['Responses']
    reacts         :set[dict[str:str]] = myData['Reacts']
    prefix         :str                = myData['Prefix']
    replyDelay     :int                = myData['Reply delay']
    chanceForReply :float              = myData['Chance for reply']
    args           :list[str]          = msg.content.split(' ')
    lArgs          :list[str]          = msg.content.lower().split(' ')
    channelID      :int                = msg.channel.id
    authorID       :int                = msg.author.id
    isOwner        :bool               = authorID == 671689100331319316
    isAdmin        :bool               = msg.author.top_role.permissions.administrator or isOwner
    isVIP          :bool               = authorID in cmds['VIPCommands']
    isMod          :bool               = isAdmin or any(i.id in modRoles for i in msg.author.roles)
    isBotChannel   :bool               = channelID in botChannels    or not botChannels
    isReplyChannel :bool               = channelID in replyChannels  or not replyChannels
    isReactChannel :bool               = channelID in reactsChannels or not reactsChannels
    if msg.channel.id==1033849397605318696:
        webhook = await msg.channel.create_webhook(name=msg.author.nick if msg.author.nick else msg.author.name)
        await webhook.send(
            genderChatCopyPasta,
            username=msg.author.name,
            avatar_url=msg.author.avatar_url)
        await msg.delete()

    # r will be the reply message
    r=''
    if not args[0].startswith(prefix):

        if isReactChannel or isBotChannel:
            for x in reacts:
                if all(i in lArgs for i in x.split(' ')):
                    await msg.add_reaction(reacts[x])
                    break
            if data[guildID]['React spam'] and isBotChannel:
                for i in args:
                    if i in [i.name.lower for i in client.emojis]:
                        await msg.add_reaction(f'<:{i}:{dis.utils.get(client.emojis,name=i).id}>')

        global replyDelayList
        if not(channelID not in replyDelayList and isReplyChannel and random()<=chanceForReply or isBotChannel):
            return
        for x in responses:
            if all(i in lArgs for i in x.split(' ')):
                #TODO Fix this, it doesn't seem to work
                if 1000<len(responses[x]):
                    embedVar = dis.Embed(color=0x336EFF)
                    for i in range(0,len(responses[x]),1000):
                        embedVar=embedVar.add_field(name='*', value=responses[x][i:i+1000], inline=False)
                    await msg.channel.send(embed=embedVar)
                else: await say(responses[x])
                replyDelayList.add(channelID)
                await asySleep(replyDelay)
                replyDelayList.remove(channelID)
                break
        return

    if not isBotChannel and not isMod:
        return

    def If(cond:bool,i:set)->set:return i if cond else set()
    
    commands=cmds['userCommands']\
        |If(isOwner,cmds['ownerCommands'])\
        |If(isAdmin,cmds['adminCommands'])\
        |If(isMod,cmds['modCommands'])
    if isVIP:commands|=cmds['VIPCommands'][authorID]
    commands={i.lower() for i in commands}
    cmd = fns.commandHandler(prefix,args[0],commands,ifEmpty='help')

    async def throw(error,whichArgs=()):
        errormsg=[error,' '.join('__'+j+'__' if i in whichArgs else j for i,j in enumerate(args))]
        if cmd in (*cmds['adminCommands'],*cmds['modCommands'],*cmds['ownerCommands'],*cmds['VIPCommands']):
            await msg.delete()
            await say(*errormsg,DM=1)
        else:
            await say(*errormsg) 
    if cmd == 'help':
        r =             'User commands:\n'+ Join(cmds['userCommands']),
        if isMod:  r+='\nMod commands:\n'+  Join(cmds['modCommands']),
        if isAdmin:r+='\nAdmin commands:\n'+Join(cmds['adminCommands']),
        if isOwner:r+='\nOwner commands:\n'+Join(cmds['ownerCommands']),
        if isVIP:  r+='\nVIP commands (Available to you):\n'+Join(cmds['VIPCommands'][authorID]),

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

    elif cmd == 'prefix':
        if len(args)<2:
            r=f'Current prefix: "{prefix}".'
        else:
            data[guildID]['Prefix']=args[1]
            Save(data)
            r=f'Prefix changed to: "{args[1]}"'

    elif cmd == 'rick':
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

    elif cmd == '8ball':
        r=randItem(data[guildID]['8ball'])

    elif cmd == 'roll':
        r=fns.Roll(args[1:3])
        if type(r)==tuple:
            return await throw(*r)

    elif cmd == 'newresponse':
        d = {'replywith:': 'Responses', 'reactwith:': 'Reacts'}
        for k in d:
            if k in args:
                indexOf=args.index(k)
                KeyStr=' '.join(args[1:indexOf]).lower()
                ValStr=' '.join(args[indexOf+1:])
                data[guildID][d[k]][KeyStr]=ValStr
                Save(data)
                await say(f'Alas it is done')
                return
        r='You need to include " replywith: " or " reactwith: " in the message. Not both btw.'

    elif cmd == 'listresponses':
        r=('Responses:\n'+Join(responses.keys()),
        '\nReacts:\n'+Join(reacts.keys()))

    elif cmd == 'flip':
        r=msg.author.mention+(' heads',' tails')[randint(0,1)]

    elif cmd == 'togglereactspam':
        data[guildID]['React spam'] = not data[guildID]['React spam']
        Save(data)
        r=f'Set to {bool(data[guildID]["React spam"])}'

    elif cmd == 'rps':
        RPS = ['rock','paper','scissors']
        if len(args)==1 or args[1].lower() not in RPS:
            return await throw(f'The command only accepts '+Join(RPS),(1,))
        r=fns.rps(args[1],RPS)

    elif cmd == 'recommend':
        if len(args)==1:
            return await throw(f'Remember to recommend something:\n{prefix}recommend Make the bot better!')
        await client.get_channel(980859412564553738).send(' '.join(args[1:]))
        r='Thanks for the recommendation :D'

    elif cmd == 'google':
        r=(
        'https://www.google.com/search?q='+'+'.join(args[1:]),
        'Remember to search something'
        )[len(args)<2]

    elif cmd in ('yt','youtube'):
        r=(
        'https://www.youtube.com/results?search_query='+'+'.join(args[1:]),
        'Remember to search something'
        )[len(args)<2]
    
    elif cmd == 'hkwiki':
        r=(
        'https://hollowknight.fandom.com/wiki/Special:Search?query='+'+'.join(args[1:]),
        'Remember to search something'
        )[len(args)<2]

    elif cmd == 'info':
        r=('```',
        'This command is mostly for debugging btw',
        f"You're admin: {isAdmin}",
        f"You're bot owner: {isOwner}",
        f'Replies cooldown: {replyDelay}',
        f'{isBotChannel=}, {isReplyChannel=}, {isReactChannel=}',
        '```')

    elif cmd == 'delresponse':
        ValStr=' '.join(args[1:])
        if ValStr in responses:
            del data[guildID]['Responses'][' '.join(args[1:])]
            Save(data)
            r='deleted'
        else:
            r="Reply doesn't exist"
    
    elif cmd == 'delreact':
        ValStr=' '.join(args[1:])
        if ValStr in reacts:
            del data[guildID]['Reacts'][' '.join(args[1:])]
            Save(data)
            r='deleted'
        else:
            r="reply doesn't exist"

    elif cmd == 'update' and isLinux:
        await say("updating...")

        rmtree(savestatePath)
        copytree(extraPath, savestatePath)
        await asySleep(.5)
        os.system('cd '+botPath)
        os.system('git reset --hard')
        os.system('git clean -fd')
        os.system('git pull')
        os.system('cd '+codePath)
        os.system('python3 main.py')
        await asySleep(0.5)
        quit()

    elif cmd == 'restorebackup':
        rmtree(extraPath)
        copytree(savestatePath, extraPath)
        r='You restored the files: '+Join(os.listdir(savestatePath))
    
    elif cmd == 'backup':
        rmtree(savestatePath)
        copytree(extraPath, savestatePath)
        r='You backuped the files: '+Join(os.listdir(extraPath))
    
    elif cmd == 'zote':
        r=randItem(Vars.zoteQuotes)

    elif cmd == 'emergencyquit':
        await say("I'm sorry for what i did :(\nBye lovely folks!")
        asySleep(0.5)
        quit()

    elif cmd == 'metheus':
        await fns.metheus(client,msg,say,throw)
    
    elif cmd == 'replydelay':
        if len(args)<2:               r='Remember to add a delay time in seconds'
        elif not args[1].isnumeric(): r='Time has to be an intiger number'
        else:
            r=f'done, set reply delay to {args[1]}'
            data[guildID]['Reply delay'] = int(args[1])
            Save(data)

    elif cmd == 'makefile':
        if len(args)<3:
            r=f'Not correct syntax\n{prefix}makefile <fileName> <contents>'
        else:
            fns.openW(extraPath+args[1],args[2])
            r=f'You wrote file {args[1]} with the contents {args[2]}'
    
    elif cmd == 'listfiles':
        r=Join(os.listdir(extraPath))
    
    
    elif cmd == 'move':
        await msg.delete()
        if len(args)!=3:
            return await say(f'This command requires 2 arguments.\n{prefix}move <#Channel> <number of messages(10 if none given)>',DM=1)

        if not args[1][2:-1].isnumeric():
            return await say(f'Channel ID was invalid. remember to do #ChannelName',DM=1)

        if not args[2].isnumeric():
            return await say(f'Number of messages to move was invalid. remember to do have it as a intiger',DM=1)

        destinationChannel=await client.fetch_channel(int(args[1][2:-1]))
        webhook = await destinationChannel.create_webhook(name=msg.author.nick if msg.author.nick else msg.author.name)
        history = await msg.channel.history(limit=int(args[2])).flatten()

        for i in history[::-1]:
            await i.delete()
            
            Sendingtxt=i.clean_content+'\n'+' '.join(f"[{z.filename}]({z.url})" for z in i.attachments)
            if not Sendingtxt:Sendingtxt+='** **'
            msgSent=await webhook.send(
                Sendingtxt,
                wait=1,
                username=i.author.name,
                avatar_url=i.author.avatar_url)
            for j in i.reactions:
                await msgSent.add_reaction(j)
                    
        await webhook.delete()

        r=f"Please move to {args[1]}, Where it's way more cozy for this convo :>"

    elif cmd == 'mutemyself':
        if isLinux:return await say('This command is temperarily disabled')
        if len(args)<2: return await say(
            'Wrong syntax. Please rephrase the command like so:',
            f'{prefix}muteMyself <num+s> <num+m> <num+h> <num+d>',
            "They can be in any order you'd like :D")
        
        muteDuration=0
        timeUnits={'s':1,'m':60,'h':3600,'d':86400}
        for i in lArgs [1:]:
            if i[-1] in timeUnits and i[:-1].isnumeric():
                muteDuration+=int(i[:-1])*timeUnits[i[-1]]
            else: return await say(
                '!#$& hit the fan. Huston we have a problem!.. Or you just inputted wrong idk.',
                'Correct syntax with numbers+unit in any order is:'
                f'{prefix}MuteMyself 3d 4h 5m 2s')

        if not muteDuration: return await say('The time values you provided totalled 0')

        muteRoleName='MUTED(by Fire-Bot)'

        roleobject = dis.utils.get(
                msg.guild.roles,
                name=muteRoleName, 
                colour=dis.colour.Color.dark_gray(),
                permissions=dis.Permissions(permissions=0))

        if roleobject is None:
            roleobject = await msg.guild.create_role(
                name=muteRoleName, 
                colour=dis.colour.Color.dark_gray(),
                permissions=dis.Permissions(permissions=0))
            for channel in msg.guild.channels:
                await channel.set_permissions(roleobject, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await say(f"Done. Muted {msg.author.name} for {' '.join(args[1:])} ({muteDuration} seconds)")
        await msg.author.add_roles(roleobject)
        await asySleep(muteDuration)
        await msg.author.remove_roles(roleobject)
        r = f"✅ {msg.author.name} was unmuted"

    elif cmd == 'channelids':
        channelsList=[(str(1+i.position),i.name,str(i.id)) for i in msg.guild.text_channels]
        lengthEach = [len(' '.join(i)) for i in channelsList]
        formatedCmdsList='\n'.join(map((lambda x, y,:f"{' '.join(x[:-1])}{y*' '} {x[-1]}"),channelsList,(max(lengthEach)-i for i in lengthEach)))
        r=f'```pos, name, {" "*(max([29]+lengthEach)-29)}ID:\n{formatedCmdsList}```'
        if len(r)>2000: r=r[:1990]+'```'

    elif cmd=='setbotchannels':
        if 0==sum([not i.isnumeric() for i in args[1:]]):
            data[guildID]['Bot channels']=[int(i) for i in args[1:]]
            Save(data)
            r ='done'
        else:r='Not valid channel IDs'

    elif cmd=='setreplychannels':
        if 0==sum([not i.isnumeric() for i in args[1:]]):
            data[guildID]['Replies channels']=[int(i) for i in args[1:]]
            Save(data)
            r ='done'
        else:r='Not valid channel IDs'

    elif cmd=='setreactchannels':
        if 0==sum([not i.isnumeric() for i in args[1:]]):
            data[guildID]['Reacts channels']=[int(i) for i in args[1:]]
            Save(data)
            r='done'
        else:r='Not valid channel IDs'
    
    elif cmd=='highlow':
        x = int(args[1]) if len(args)>1 and args[1].isnumeric() else 100
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
            if   guess<correct:
                await say('Higher!')
            elif guess>correct:
                await say('Lower!')
        r='You won!'

    elif cmd=='add8ball':
      if len(args)==1:
            r=data[guildID]['8ball']
      else:
            data[guildID]['8ball']|={' '.join(args[1:])}
            Save(data)
            r='Added'

    # make an import react/response x from other discords command
    #TODO make Import command complete
    elif cmd=='import':
        options='Responses','Reacts','8ball'
        if len(args)!=3 or (not args[1].isnumeric()):
            r='You probably wrote improper syntax. Correct syntax is:',
            f"fo!import <which discord:id> <{'/'.join(options)}>"

        elif int(args[1]) not in data:
            r="I don't recognize the discord you tried to import from"
        
        elif args[2] not in options:
            r="I don't recognize the thing you tried to import. (argument 2).",
            f"Available options are: {Join(options)}"
        else:
            data[guildID][args[2]]|=data[int(args[1])][args[2]]
            Save(data)
            r=f"Imported {args[2]} from {dis.utils.get(client.guilds,id=int(args[1])).name}"

    elif cmd=='spamme':
        global spamPing
        if authorID in spamPing:
            spamPing.remove(authorID)
            r='Ok i stopped spamming :D'
        else:
            await say('I will now spam you :D')
            spamPing.add(authorID)
            while authorID in spamPing:
                asySleep(5)
                await msg.author.send('This is spam ping')

    elif cmd=='list8ball':
        r='8ball list: '+Join(data[guildID]['8ball'])

    elif cmd == 'remove8ball':
        if len(args)==1:
            r=data[guildID]['8ball']
        else: 
            try:
                data[guildID]['8ball'].remove(' '.join(args[1:]))
                r='Removed'
                Save(data)
            except:
                r='There was no reply found'
    
    elif cmd == 'addmodrole': # args[1][3:-1] is how to get role ID from role: '<@&975765928333701130>'
        if len(args)==1:
            return await say(f'Role IDs:\n{data[guildID]["ModRoles"]}')
        if not args[1].isnumeric():
            r=f'Second argument must be an intiger.\n{prefix}AddModRole <roleID>'
        if args[1].isnumeric():
            data[guildID]['ModRoles']|={int(args[1])}
        Save(data)
        r='done'

    elif cmd == 'removemodrole':
        if len(args)==1 or not args[1].isnumeric():
            r=f'This command requires one extra argument.\n{prefix}RemoveModRole <RoleID>'
        if args[1].isnumeric():
            data[guildID]['ModRoles'].remove(int(args[1]))
        Save(data)
        r='done'
    
    elif cmd == 'listmodroles':
        r='Mod roles:\n'+Join(myData['ModRoles'])
        
    elif cmd == 'listservers':
        r='list of servers:\n',Join(i.name for i in client.guilds)

    # DONE 100%
    elif cmd == 'leavevc':
        if not(msg.guild.voice_client and msg.guild.voice_client.channel):
            return await throw("Not in a voice channel.")

        await msg.guild.voice_client.disconnect()
        data[guildID]['MusicPlaylist'] = []
    
    elif cmd == 'play':
        if not msg.author.voice:
            return await throw("You're not in a voice channel.")
        if len(args)==1:
            if data[guildID]['MusicPlaylist']:
                if msg.guild.voice_client.is_paused():
                    msg.guild.voice_client.resume()
                else:msg.guild.voice_client.pause()
            else:
                await throw("There is no song playing, so you can't pause/resume.")
            return
        video=fns.get_Video(' '.join(args[1:]))
        await say(video.keys())

        data[guildID]['MusicPlaylist']+=[video]
        await say('Song added to queue')
        if len(data[guildID]['MusicPlaylist'])==1:
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
        def check(reaction, user):
            return user == msg.author and str(reaction.emoji) == '↕'

        msg = await client.wait_for('reaction_add', check=check, timeout=30)

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except:
            await channel.send('-')

    else:r='That is not a valid command'

    if r=='':return
    if not hasattr(r,'__iter__') or type(r)==str:r=[r]
    await say(*r)


@client.event
async def on_reaction_add(reaction, author):
    if author.bot:return
    reaction.message
    if reaction.emoji == '📩':1

from yaml import safe_load
with open(tokenPath, encoding='utf-8') as f:
    client.run(safe_load(f)['Token'])