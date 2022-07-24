from asyncio import sleep as asySleep
import os
from typing import Iterable
import discord as dis
from random import randint,random
from shutil import rmtree, copytree
import imports.functions as fns
import imports.vars as vars

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
        'Rick','Zote','muteMyself','SpamMe','List8Ball'
    },

    'modCommands':{
        'Move'
    },

    'adminCommands':{
        'NewResponse','DelResponse','DelReact','SetReplyChannels',
        'SetReactChannels','SetBotChannels','ChannelIDs','Prefix','addModRole',
        'ReplyDelay','ReplyChance','ToggleReactSpam','Add8ball','remove8ball',
        'removemodrole'
    },


    'VIPCommands':{
        486619954745966594:{'EmergencyQuit'} # Fire Owl
    },

    'ownerCommands':{
        'Update','EmergencyQuit','MakeFile','ListFiles','Backup',
        'RestoreBackup','Testing','Highlow','SettingAdded',
        'BQNEval','ListServers',

        'importreplies','Add','Remove' # work in  progress
        }
}

defaultGuildSettings={
    'Prefix'          :'fo!',
    'Bot channels'    :set(),
    'Replies channels':set(),
    'Reacts channels' :set(),
    'Reply delay'     :0,
    'Replies per min' :10,
    'Chance for reply':1,
    'Reacts'          :vars.defaultReactsList,
    'Responses'       :vars.defaultResponsesList,
    'React spam'      :0,
    '8ball'           :vars.ball8,
    'ModRoles'        :set()
}

replyDelayList=set()
spamPing=set()

def save(data):
    fns.openW(datatxtPath,data)

def randItem(i:list):
    return list(i)[randint(0,len(i)-1)]

if not isLinux:
    from subprocess import Popen, PIPE, STDOUT

    def BQNeval(i:str,BQNpath:str=BQNpath)->str:
        fns.openW(BQNpath,i)
        return Popen(['BQN',BQNpath], stdout=PIPE, stderr=STDOUT).stdout.read().decode('utf8')

def Join(i): return ', '.join(sorted(i))

@client.event
async def on_ready():
    await client.change_presence(activity=dis.Game(f'subscribe to FIRE OWL'))
    print('Logged in as',
    client.user.name,
    client.user.id,
    f'In {len(client.guilds)} servers:',
    '------',
    *(i.name for i in client.guilds),
    '------', sep='\n')

# syntax for writing emotes is <:shroompause:976245280041205780> btw
@client.event
async def on_message(msg):
    if msg.author.bot:return
    if not msg.guild :return await msg.channel.send("I don't work in DMs sadly.")

    async def say(*values,sep='\n'):
        await msg.channel.send(sep.join(values))

    args :list[str] = msg.content.split(' ')
    lArgs:list[str] = msg.content.lower().split(' ')
    guildID  :int   = msg.guild.id
    channelID:int   = msg.channel.id
    msgAuthor:int   = msg.author.id
    isOwner  :bool  = msgAuthor == 671689100331319316
    isAdmin  :bool  = msg.author.top_role.permissions.administrator or isOwner
    isVIP    :bool  = msgAuthor in cmds['VIPCommands']
    isMod    :bool  = isAdmin #or msgAuthor in modRoles 

    data = fns.openR(datatxtPath)
    if guildID not in data:
        data[guildID] = defaultGuildSettings
        save(data)

    botChannels    = data[guildID]['Bot channels']
    reactsChannels = data[guildID]['Reacts channels']
    replyChannels  = data[guildID]['Replies channels']
    responses      = data[guildID]['Responses']
    reacts         = data[guildID]['Reacts']
    prefix         = data[guildID]['Prefix']
    replyDelay     = data[guildID]['Reply delay']
    chanceForReply = data[guildID]['Chance for reply']
    isBotChannel   = channelID in botChannels    or not botChannels
    isReplyChannel = channelID in replyChannels  or not replyChannels
    isReactChannel = channelID in reactsChannels or not reactsChannels

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
                        embedVar = dis.Embed(color=0x336EFF)
                        embedVar.add_field(name='', value=responses[x][    :1000], inline=False,)
                        embedVar.add_field(name='', value=responses[x][1000:2000], inline=False,)
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
    if isVIP:commands|=cmds['VIPCommands'][msgAuthor]

    commands={i.lower() for i in commands}
    
    cmd = fns.commandHandler(prefix,args[0],commands,ifEmpty='help')

    if cmd == 'help':
        r =             'User commands:\n'+ Join(cmds['userCommands']),
        if isMod:  r+='\nMod commands:\n'+  Join(cmds['modCommands']),
        if isAdmin:r+='\nAdmin commands:\n'+Join(cmds['adminCommands']),
        if isOwner:r+='\nOwner commands:\n'+Join(cmds['ownerCommands']),
        if isVIP:  r+='\nVIP commands (Available to you):\n'+Join(cmds['VIPCommands'][msgAuthor]),

    elif cmd == 'prefix':
        if len(args)<2:
            r=f'Current prefix: "{prefix}".'
        else:
            data[guildID]['Prefix']=args[1]
            save(data)
            r=f'Prefix changed to: "{args[1]}"'

    elif cmd == 'rick':
        await msg.author.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        await asySleep(15)
        await msg.author.send(
            'Ok i am so sorry... please forgive me. here are some cats :D',
            'https://www.youtube.com/watch?v=VZrDxD0Za9I')
        await asySleep(200)
        await msg.author.send('cope')
        await asySleep(5)
        await msg.author.send('this can help :)\nhttps://www.youtube.com/watch?v=Lc6db8qfZEw')

    elif cmd == '8ball':
        r=randItem(data[guildID]['8ball'])

    elif cmd == 'roll':
        if len(args)<2:
            r=randint(1,6)
        else:
            sum([i.isnumeric() for i in args[1:]])
            if len(args) == 2:
                if '0'==args[1]:
                    r=random()
                else:r=randint(1,int(args[1]))
            else:
                r=randint(int(args[1]),int(args[2]))

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
        r='Responses: '+', '.join(list(responses.keys())),
        '\nReacts: '+', '.join(list(reacts.keys()))

    elif cmd == 'flip':
        r=msg.author.mention+(' heads',' tails')[randint(0,1)]

    elif cmd == 'togglereactspam':
        data[guildID]['React spam'] = not data[guildID]['React spam']
        save(data)
        r=f'Set to {bool(data[guildID]["React spam"])}'

    elif cmd == 'rps':
        if len(args)<2: return await say('Please enter rock, paper, or scissors as second argument')
        RPS = ['rock','paper','scissors']    
        userChoice = args[1].lower()
        botChoice = randItem(RPS)
        if userChoice not in RPS:
            r=f'Please enter one of the following items: {", ".join(RPS)}'
        else:
            (userChoice,botChoice,reply)=fns.rps(userChoice,botChoice)
            r=f'You chose **{userChoice}**. I (the bot) chose **{botChoice}**.\n{reply}'
    
    elif cmd == 'recommend':
        if len(args)!=1:
            await client.get_channel(980859412564553738).send(' '.join(args[1:]))
            r='Thanks for the recommendation :D'
        else:
            r=f'Remember to recommend something\n{prefix}recommend <recommendation>'

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
        )[len(args)==2]

    elif cmd == 'info':
        r='```',
        'This command is mostly for debugging btw',
        f"You're admin: {isAdmin}",
        f"You're bot owner: {isOwner}",
        f'Replies cooldown: {replyDelay}',
        f'{isBotChannel=}, {isReplyChannel=}, {isReactChannel=}',
        '```'

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
        r='You restored the files: '+', '.join(os.listdir(savestateDir))
    
    elif cmd == 'backup':
        rmtree(savestateDir)
        copytree(extraDir, savestateDir)
        r='You backuped the files: '+', '.join(os.listdir(extraDir))
    
    elif cmd == 'zote':
        r=randItem(vars.zoteQuotes)

    elif cmd == 'emergencyquit':
        await say("I'm sorry for what i did :(\nBye lovely folks!")
        asySleep(0.5)
        quit()
    
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
        r=', '.join(os.listdir(extraDir))
    
    
    elif cmd == 'move':
        await msg.delete()
        if len(args)!=3:
            return await msg.author.send(f'This command requires 2 arguments minimum.\n{prefix}move <#Channel> <number of messages(10 if none given)>')
        
        if not args[1][2:-1].isnumeric():
            return await msg.author.send(f'Channel ID was invalid. remember to do #ChannelName')

        if not args[2].isnumeric():
            return await msg.author.send(f'Number of messages to move was invalid. remember to do have it as a intiger')
        
        webhook = await (await client.fetch_channel(int(args[1][2:-1]))).create_webhook(name=msg.author.name)
        history = await msg.channel.history(limit=int(args[2])).flatten()

        for i in history[::-1]:
            await i.delete()
            if len(i.content)!=0:
                await webhook.send(i.content, username=i.author.name, avatar_url=i.author.avatar_url)
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
            msg.author.id == msgAuthor and\
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

    elif cmd=='settingadded':
        for i in defaultGuildSettings:
            for j in data.values():
                if i not in j:
                    for y in data:
                        data[y][i]=defaultGuildSettings[i]
                    save(data)
                break
        r='Done. Updated settings'

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
            f"Available options are: {', '.join(options)}"
        else:
            data[guildID][args[2]]|=data[int(args[1])][args[2]]
            save(data)
            r=f"Imported {args[2]} from {dis.utils.get(client.guilds,id=int(args[1])).name}"

    elif cmd=='spamme':
        global spamPing
        if msgAuthor in spamPing:
            spamPing.remove(msgAuthor)
            r='Ok i stopped spamming :D'
        else:
            await say('I will now spam you :D')
            spamPing.add(msgAuthor)
            while msgAuthor in spamPing:
                asySleep(5)
                await msg.author.send('This is spam ping')

    elif cmd=='list8ball':
        r='8ball list: '+', '.join(data[guildID]['8ball'])

    elif cmd == 'bqneval':
        for i in ' '.join(args[1:]).split('•')[1:]:
            if not any(i.startswith(j) for j in ['Show ','Out ']):
                return await say('Invalid use of •')
        r=BQNeval(' '.join(args[1:]))


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
            return await say(Join(data[guildID]['ModRoles']))
        if len(args)==1 or not args[1][3:-1].isnumeric() or not args[1].isnumeric():
            r=f'This command requires one extra argument.\n{prefix}AddModRole <@Rolename or roleID>'
        if args[1].isnumeric():
            data[guildID]['ModRoles']|={int(args[1])}
        else:
            data[guildID]['ModRoles']|={int(args[1][3:-1])}
        save(data)
        r='done'

    elif cmd == 'removemodrole':
        if len(args)==1 or not args[1][3:-1].isnumeric() or not args[1].isnumeric():
            r=f'This command requires one extra argument.\n{prefix}AddModRole @Rolename'
        if args[1].isnumeric():
            data[guildID]['ModRoles'].remove(int(args[1]))
        else:
            data[guildID]['ModRoles'].remove(int(args[1][3:-1]))
        save(data)
        r='done'

    #TODO
    elif cmd == 'Add':
        addables = 'Bot channels','Replies channels','Reacts channels','8ball'
        if len(args)<3:
            return await say('This command requires atleast 3 arguments, with the following syntax: ',
            )
        
    elif cmd == 'listservers':
        r='list of servers:',Join(i.name for i in client.guilds)

    elif cmd == 'testing':
        1+1

    if r:
        if str(type(r))[8:-2] in ('tuple','list','range','generator','set'):
            await say(*r)
        else:
            await say(r)


from yaml import safe_load
with open(tokenPath, encoding='utf-8') as f:
    client.run(safe_load(f)['Token'])