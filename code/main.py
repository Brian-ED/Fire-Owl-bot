from asyncio import sleep as asySleep
from asyncio import run_coroutine_threadsafe
import os
import discord as dis
from random import randint,random
from shutil import rmtree, copytree
# import youtube_dl as ytdl
import imports.functions as fns
import imports.vars as Vars

client = dis.Client()

isLinux=__file__[0]!='c'
loc             = 'C:/Users/brian/Persinal/discBots/'
if isLinux: loc = '../../'
tokenPath       = loc+'Safe/Fire-Owl-bot.yaml'
savestateDir    = loc+'data/Fire-Owl-data'
extraDir        = loc+'Fire-Owl-bot/code/extra/'
botDir          = loc+'Fire-Owl-bot/'
codeDir         = botDir+'code/'
BQNpath         = codeDir+'imports/BQNEval/BQNEval.bqn'
datatxtPath     = extraDir+'data.txt'

# load backup
rmtree(extraDir)
copytree(savestateDir, extraDir)



cmds = {
    'userCommands':{
        '8ball', 'Help', 'Roll', 'Flip', 'rps','yt','Google',
        'Youtube','ListResponses','Info','hkWiki','Recommend',
        'Rick','Zote','muteMyself','SpamMe','List8Ball','metheus'

        # music commands to add:::
        # playlists, play, p, 
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
        }
}

defaultGuildSettings={
    'Prefix'              :'fo!',
    'Bot channels'        :set(),
    'Replies channels'    :set(),
    'Reacts channels'     :set(),
    'Reply delay'         :0,
    'Replies per min'     :10,
    'Chance for reply'    :1,
    'Reacts'              :Vars.defaultReactsList,
    'Responses'           :Vars.defaultResponsesList,
    'React spam'          :0,
    '8ball'               :Vars.ball8,
    'ModRoles'            :set(),
    'MusicPlaylist'       :[],
    'MusicSkipVotes'      :set(),
    'MusicNeededVoteRatio':.5
}

data:dict[int:dict[str:]] = fns.openR(datatxtPath)

def save(data):
    fns.openW(datatxtPath,data)

for i in defaultGuildSettings:
    if i not in list(data.values())[0]:
        for y in data:
            data[y][i]=defaultGuildSettings[i]
        save(data)

replyDelayList=set()
spamPing=set()


def randItem(i:list):
    return list(i)[randint(0,len(i)-1)]

if not isLinux:
    from subprocess import Popen, PIPE, STDOUT

    def BQNeval(i:str,BQNpath:str=BQNpath)->str:
        fns.openW(BQNpath,i)
        return Popen(['BQN',BQNpath], stdout=PIPE, stderr=STDOUT).stdout.read().decode('utf8')

def Join(i): return ', '.join(sorted(i))


recommendsChannel:object = client.get_channel(980859412564553738)

@client.event
async def on_ready():
    await client.change_presence(activity=dis.Game(f'subscribe to FIRE OWL'))
    print('Logged in as',
    client.user.name,
    client.user.id,
    f'In {len(client.guilds)} servers',
    '------', sep='\n')

# syntax for writing emotes is <:shroompause:976245280041205780> btw
@client.event
async def on_message(msg):
    if msg.author.bot:return

    async def say(*values,sep='\n',**KWARGS):
        await msg.channel.send(sep.join(str(i)for i in values),**KWARGS)
    async def sayDM(*values,sep='\n',**KWARGS):
        await msg.author.send(sep.join(str(i)for i in values),**KWARGS)
    
    if not msg.guild: return say(msg.channel.send("I don't work in DMs sadly."))


    guildID:int = msg.guild.id
    data:dict[int:dict[str:]] = fns.openR(datatxtPath)
    if guildID not in data:
        data[guildID] = defaultGuildSettings
        save(data)
    botChannels    :set[int]           = data[guildID]['Bot channels']
    reactsChannels :set[int]           = data[guildID]['Reacts channels']
    replyChannels  :set[int]           = data[guildID]['Replies channels']
    modRoles       :set[int]           = data[guildID]['ModRoles']
    responses      :set[dict[str:str]] = data[guildID]['Responses']
    reacts         :set[dict[str:str]] = data[guildID]['Reacts']
    prefix         :str                = data[guildID]['Prefix']
    replyDelay     :int                = data[guildID]['Reply delay']
    chanceForReply :float              = data[guildID]['Chance for reply']
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
    vcClient                           = msg.guild.voice_client
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
        if channelID not in replyDelayList and isReplyChannel and random()<=chanceForReply or isBotChannel:   
            for x in responses:
                if all(i in lArgs for i in x.split(' ')):
                    #TODO Fix this, it doesn't seem to work
                    if 1000<len(responses[x]):
                        embedVar = dis.Embed(color=0x336EFF).add_field(
                            name='', value=responses[x][    :1000], inline=False,).add_field(
                            name='', value=responses[x][1000:2000], inline=False,)
                        if len(responses[x])>2000:embedVar.add_field(name='', value=responses[x][2000:3000], inline=False,)
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
        errormsg=(
            error,
            ' '.join('__'+j+'__' if i in whichArgs else j for i,j in enumerate(args))
        )
        if cmd in (cmds['adminCommands'],cmds['modCommands'],cmds['ownerCommands'],cmds['VIPCommands']):
            await msg.delete()
            await sayDM(*errormsg)
        r=errormsg 

    if cmd == 'help':
        r =             'User commands:\n'+ Join(cmds['userCommands']),
        if isMod:  r+='\nMod commands:\n'+  Join(cmds['modCommands']),
        if isAdmin:r+='\nAdmin commands:\n'+Join(cmds['adminCommands']),
        if isOwner:r+='\nOwner commands:\n'+Join(cmds['ownerCommands']),
        if isVIP:  r+='\nVIP commands (Available to you):\n'+Join(cmds['VIPCommands'][authorID]),

    elif cmd == 'prefix':
        if len(args)<2:
            r=f'Current prefix: "{prefix}".'
        else:
            data[guildID]['Prefix']=args[1]
            save(data)
            r=f'Prefix changed to: "{args[1]}"'

    elif cmd == 'rick':
        await sayDM('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        await asySleep(15)
        await sayDM(
            'Ok i am so sorry... please forgive me. here are some cats :D',
            'https://www.youtube.com/watch?v=VZrDxD0Za9I')
        await asySleep(200)
        await sayDM('cope')
        await asySleep(5)
        await sayDM('this can help :)\nhttps://www.youtube.com/watch?v=Lc6db8qfZEw')

    elif cmd == '8ball':
        r=randItem(data[guildID]['8ball'])

    elif cmd == 'roll':
        if len(args) == 1:
            return await say(randint(1,6))
        elif not all(i.isnumeric() for i in args[1:]):
            return await throw('This command only accepts intigers',(1,2))
        i=[int(i) for i in args[1:]]
        i.sort()
        if len(i)==1:
            if i[0]==0: r=random()
            else: r=randint(1,i[0])
        elif len(i)==2:
            r=randint(*i)
        else:
            return await throw('This command only accepts max 2 inputs',range(3,len(args)))

    elif cmd == 'newresponse':
        d = {'replywith:': 'Responses', 'reactwith:': 'Reacts'}
        for k in d:
            if k in args:
                indexOf=args.index(k)
                KeyStr=' '.join(args[1:indexOf]).lower()
                ValStr=' '.join(args[indexOf+1:])
                data:dict = fns.openR(datatxtPath)
                data[guildID][d[k]][KeyStr]=ValStr
                save(data)
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
        save(data)
        r=f'Set to {bool(data[guildID]["React spam"])}'

    elif cmd == 'rps':
        RPS = ['rock','paper','scissors']    
        if len(args)==1 or args[1].lower() not in RPS:
            return await throw(f'The command only accepts '+Join(RPS),(1,))

        userChoice = args[1].lower()
        botChoice = randItem(RPS)
        reply=fns.rps(userChoice,botChoice)
        r=f'You chose **{userChoice}**. I (the bot) chose **{botChoice}**.\n{reply}'

    elif cmd == 'recommend':
        if len(args)==1:
            return await throw(f'Remember to recommend something\n{prefix}recommend <recommendation>')
        await recommendsChannel.send(' '.join(args[1:]))
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
            save(data)
            r='deleted'
        else:
            r="Reply doesn't exist"
    
    elif cmd == 'delreact':
        ValStr=' '.join(args[1:])
        if ValStr in reacts:
            del data[guildID]['Reacts'][' '.join(args[1:])]
            save(data)
            r='deleted'
        else:
            r="reply doesn't exist"

    elif cmd == 'update' and isLinux:
        await say("updating...")

        rmtree(savestateDir)
        copytree(extraDir, savestateDir)
        await asySleep(.5)
        os.system('cd '+botDir)
        os.system('git reset --hard')
        os.system('git clean -fd')
        os.system('git pull')
        os.system('cd '+codeDir)
        os.system('python3 main.py')
        await asySleep(0.5)
        quit()

    elif cmd == 'restorebackup':
        rmtree(extraDir)
        copytree(savestateDir, extraDir)
        r='You restored the files: '+Join(os.listdir(savestateDir))
    
    elif cmd == 'backup':
        rmtree(savestateDir)
        copytree(extraDir, savestateDir)
        r='You backuped the files: '+Join(os.listdir(extraDir))
    
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
            save(data)

    elif cmd == 'makefile':
        if len(args)<3:
            r=f'Not correct syntax\n{prefix}makefile <fileName> <contents>'
        else:
            fns.openW(extraDir+args[1],args[2])
            r=f'You wrote file {args[1]} with the contents {args[2]}'
    
    elif cmd == 'listfiles':
        r=Join(os.listdir(extraDir))
    
    
    elif cmd == 'move':
        await msg.delete()
        if len(args)!=3:
            return await msg.author.send(f'This command requires 2 arguments minimum.\n{prefix}move <#Channel> <number of messages(10 if none given)>')
        
        if not args[1][2:-1].isnumeric():
            return await msg.author.send(f'Channel ID was invalid. remember to do #ChannelName')

        if not args[2].isnumeric():
            return await msg.author.send(f'Number of messages to move was invalid. remember to do have it as a intiger')
        
        destinationChannel=await client.fetch_channel(int(args[1][2:-1]))
        webhook = await destinationChannel.create_webhook(name=msg.author.name)
        history = await msg.channel.history(limit=int(args[2])).flatten()

        for i in history[::-1]:
            await i.delete()
            if len(i.content)!=0:
                msgSent=await webhook.send(
                    i.content+'\n'+' '.join(f"[{z.filename}]({z.url})" for z in i.attachments),
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
            save(data)
            r ='done'
        else:r='Not valid channel IDs'

    elif cmd=='setreplychannels':
        if 0==sum([not i.isnumeric() for i in args[1:]]):
            data[guildID]['Replies channels']=[int(i) for i in args[1:]]
            save(data)
            r ='done'
        else:r='Not valid channel IDs'

    elif cmd=='setreactchannels':
        if 0==sum([not i.isnumeric() for i in args[1:]]):
            data[guildID]['Reacts channels']=[int(i) for i in args[1:]]
            save(data)
            r='done'
        else:r='Not valid channel IDs'
    
    elif cmd=='highlow':
        x = int(args[1]) if len(args)>1 and args[1].isnumeric() else 100
        await say(f'Game started. Guess a number between 1-{x}')
        print(1)
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
            save(data)
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
            save(data)
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
                save(data)
            except:
                r='There was no reply found'
    
    elif cmd == 'addmodrole': # args[1][3:-1] is how to get role ID from role: '<@&975765928333701130>'
        if len(args)==1:
            return await say(f'Role IDs:\n{data[guildID]["ModRoles"]}')
        if not args[1].isnumeric():
            r=f'Second argument must be an intiger.\n{prefix}AddModRole <roleID>'
        if args[1].isnumeric():
            data[guildID]['ModRoles']|={int(args[1])}
        save(data)
        r='done'

    elif cmd == 'removemodrole':
        if len(args)==1 or not args[1].isnumeric():
            r=f'This command requires one extra argument.\n{prefix}RemoveModRole <RoleID>'
        if args[1].isnumeric():
            data[guildID]['ModRoles'].remove(int(args[1]))
        save(data)
        r='done'
    
    elif cmd == 'listmodroles':
        r='Mod roles:\n'+Join(data[guildID]['ModRoles'])
        
    elif cmd == 'listservers':
        r='list of servers:\n',Join(i.name for i in client.guilds)

    elif cmd == 'testing':
        # x=await msg.author.voice.channel.connect()
        await msg.channel.send("[hello](https://google.com)")

    elif cmd == 'leavevc':
        if vcClient and vcClient.channel:
            await vcClient.disconnect()
            data[guildID]['Playlist']=[]
            save()
        else:
            await throw("Not in a voice channel.")
    
    elif cmd in ('p','play'):
        if 0<len(data[guildID]['MusicPlaylist']):
            if len(args)==1:
                if vcClient.is_paused():
                    vcClient.resume()
                else:vcClient.pause()
            else:
                data[guildID]['MusicPlaylist'].append(' '.join(args[1:]))
                save(data)
        else:
            song=' '.join(args[1:])
            data[guildID]['MusicSkipVotes'] = set()
            save(data)
            source=dis.PCMVolumeTransformer(dis.FFmpegPCMAudio(song.stream_url, before_options=Vars.FFMPEG_BEFORE_OPTS), volume=200)
            run_coroutine_threadsafe(vcClient.disconnect(),vcClient.loop)

        """Plays audio hosted at <url> (or performs a search for <url> and plays the first result)."""
        if vcClient and vcClient.channel:
            data[msg.guild.id]['Music'].append(video)
            await msg.channel.send("Added to queue.", embed=video.get_embed())
        else:
            if not (msg.author.voice is not None and msg.author.voice.channel is not None):
                return await throw("You need to be in a voice channel to do that.")

            vcChannelJoined = await msg.author.voice.channel.connect()

            #get info:::
            def _get_info(video_url):
                with ytdl.YoutubeDL(Vars.YTDL_OPTS) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    video = None
                    if "_type" in info and info["_type"] == "playlist":
                        return _get_info(
                            info["entries"][0]["url"])  # get info for first video
                    else:
                        video = info
                    return video

            video=_get_info('https://www.youtube.com/watch?v=v_B3qkp4nO4&list=RDMMXGUS7VnLvZU&index=8')

            ###Defining vars:::
            # video_format = video["formats"][0]
            # stream_url =   video["formats"][0]["url"]
            # video_url = video["webpage_url"]
            # video["title"]
            uploader =  video["uploader"] if "uploader" in video else ""
            thumbnail = video["thumbnail"] if "thumbnail" in video else None

            ###make video embed:::
            embed = dis.Embed(title=video["title"], description=uploader, url=video["webpage_url"])
            embed.set_footer(
                text=f"Requested by {msg.author.name}",
                icon_url=msg.author.name.avatar_url)
            if thumbnail:embed.set_thumbnail(url=thumbnail)

            ###
            await msg.channel.send("", embed=video.get_embed())
            r=f"Now playing '{video.title}'"

        vcClient.play(source, after=after_playing)
        save(data)
    
    elif cmd in {'skip','s'}:
        if not data[guildID]['MusicPlayList']:
            return throw("There's nothing to skip")
        data[guildID]['MusicSkipVotes'].add(authorID)
        users_in_channel = len(i for i in msg.channel.members if not i.bot)
        currentVoters = data[guildID]['MusicSkipVotes']
        voteRatio=len(currentVoters)/users_in_channel
        neededVoteRatio=data[guildID]['MusicNeededVoteRatio']
        if voteRatio >= neededVoteRatio:
            r="Enough votes, skipping..."
            channel.guild.voice_client.stop()
        else:
            r=f'Not enough votes. Only {int(100*voteRatio)}% want to skip, when {int(100*neededVoteRatio)}% are needed'
    
    elif cmd in {'np','nowplaying'}:
        if len(data[guildID]['MusicPlaylist']) > 0:
            r = [f"{len(data[guildID]['MusicPlaylist'])} songs in queue:"]+[
                f"  {index+1}. **{song.title}** (requested by **{song.requested_by.name}**)"
                for index, song in enumerate(data[guildID]['MusicPlaylist'])
            ]
        else:
            r="The play queue is empty."
    else:r='That is not a valid command'

    if r:
        if str(type(r))[8:-2] in {'tuple','list','range','generator','set'}:
            await say(*r)
        else:
            await say(r)


from yaml import safe_load
with open(tokenPath, encoding='utf-8') as f:
    client.run(safe_load(f)['Token'])