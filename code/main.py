from asyncio import sleep as asySleep
import os
import discord as dis
import yaml
from random import randint,random
from platform import platform
from shutil import rmtree, copytree
from imports import functions as fns
from imports.vars import zoteQuotes,defaultReactsList,defaultResponsesList
isLinux = platform(True,True) != 'Windows-10'

prefix = 'fo!' 
client = dis.Client()

loc             = 'C:/Users/brian/Persinal/discBots/'
if isLinux: loc = '../../'
tokenPath       = loc+'Safe/Fire-Owl-bot.yaml'
savestateDir    = loc+'data/Fire-Owl-data'
extraDir        = loc+'Fire-Owl-bot/code/extra/'
botDir          = loc+'Fire-Owl-bot/'
codeDir         = botDir+'code/'
datatxtPath     = extraDir+'data.txt'
respondstxtPath = extraDir+'responds.txt'
reactstxtPath   = extraDir+'reacts.txt'


# load backup
rmtree(extraDir)
copytree(savestateDir, extraDir)

userCommands  = ['8ball', 'Help', 'Roll', 'Flip', 'rps','yt','Google','Youtube','ListResponses','Info','hkWiki','Recommend','Rick','Zote','muteMyself']
adminCommands = ['NewResponse','DelResponse','DelReact','SetReplyChannels','SetReactChannels','SetBotChannels','ChannelIDs','Prefix','ReplyDelay','ReplyChance','ToggleReactSpam']
selectPeople  = {486619954745966594:['EmergencyQuit']}
ownerCommands = ['Update','EmergencyQuit','MakeFile','ListFiles','Backup','RestoreBackup','NewSettings','eval','Testing','Highlow','SettingAdded','importreplies']
adminCommands.sort()
userCommands.sort()
ownerCommands.sort() 

defaultGuildSettings={'Prefix'          :'fo!',
                      'Bot channels'    :[],
                      'Replies channels':[],
                      'Reacts channels' :[],
                      'Reply delay'     :0,
                      'Replies per min' :10,
                      'Chance for reply':1,
                      'Reacts'          :defaultReactsList,
                      'Responses'       :defaultResponsesList,
                      'React spam'      :0}

global replyDelayList
replyDelayList=[]

def save(data):
    fns.openW(datatxtPath,data)

def randItem(i):
    return i[randint(0,len(i)-1)]

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
    if not msg.guild:
        await msg.channel.send("I don't work in DMs sadly.")
        return

    async def say(*values,sep='\n'):
        await msg.channel.send(sep.join(values))
    args:list[str]  = msg.content.split(' ')
    lArgs:list[str] = msg.content.lower().split(' ')
    isOwner:bool    = msg.author.id == 671689100331319316
    isAdmin:bool    = msg.author.top_role.permissions.administrator or isOwner
    guildID:int     = msg.guild.id
    channelID:int   = msg.channel.id
    msgAuthor:int   = msg.author.id

    commands = [i.lower() for i in\
        userCommands+\
        ([],adminCommands)[isAdmin]+\
        ([],ownerCommands+sum(selectPeople.values(),[]))[isOwner]]
    if msgAuthor in selectPeople:
        commands += selectPeople[msgAuthor]
    commands = list(set(commands))

    data = fns.openR(datatxtPath)
    if guildID not in data:
        data[guildID]=defaultGuildSettings
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
                    if 1000<len(responses[x]):
                        embedVar = dis.Embed(color=0x336EFF)
                        embedVar.add_field(name='', value=responses[x][    :1000], inline=False,)
                        embedVar.add_field(name='', value=responses[x][1000:2000], inline=False,)
                        if len(responses[x])>2000:embedVar.add_field(name='', value=responses[x][2000:3000], inline=False,)
                        await msg.channel.send(embed=embedVar)
                    else: await say(responses[x])
                    replyDelayList += [channelID]
                    await asySleep(replyDelay)
                    replyDelayList.remove(channelID)
                    break
        return

    if not isBotChannel:
        return
    args[0] = fns.commandHandler(prefix,args[0],commands)

    if args[0] == 'help':
        r ='List of commands: '+', '.join(userCommands)
        if isAdmin: r+='\n\nList of admin commands: '+', '.join(adminCommands)
        if isOwner: r+='\n\nList of owner commands: '+', '.join(ownerCommands)

    elif args[0] == 'prefix':
        if len(args)<2:
            r=f'Current prefix: "{prefix}".'
        else:
            data[guildID]['Prefix']=args[1]
            save(data)
            r=f'Prefix changed to: "{args[1]}"'

    elif args[0] == 'rick':
        await msg.author.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        await asySleep(15)
        await msg.author.send('Ok i am so sorry... please forgive me. here are some cats :D\nhttps://www.youtube.com/watch?v=VZrDxD0Za9I')
        await asySleep(200)
        await msg.author.send('cope')
        await asySleep(5)
        await msg.author.send('this can help :)\nhttps://www.youtube.com/watch?v=Lc6db8qfZEw')

    elif args[0] == '8ball':
        ball8=['Yes','No','Not sure','You know it','Absolutely not',
               'Absolutely yes','Cannot tell','Sure','Mmm, I have no idea',
               'Haha ye boi','What? No!','Yep','Nope','Maybe',"I'm too afraid to tell",
               "Sorry that's too hard to answer",'Most likely']
        r=randItem(ball8)

    elif args[0] == 'roll':
        if len(args)<2:
            r=randint(1,6)
        else:
            sum([i.isnumeric() for i in args[1:]])
            if len(args) == 2:
                if '0'==args[1]:
                    r=random()
                else:r=randint(1,int(args[1]))
            else:    r=randint(int(args[1]),int(args[2]))

    elif args[0] == 'newresponse':
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

    elif args[0] == 'listresponses':
        r='Responses: '+', '.join(list(responses.keys())),
        'Reacts: '+', '.join(list(reacts.keys()))

    elif args[0] == 'flip':
        r=msg.author.mention+(' heads',' tails')[randint(0,1)]
    
    elif args[0] == 'togglereactspam':
        data[guildID]['React spam'] = not data[guildID]['React spam']
        save(data)
        r=f'Set to {bool(data[guildID]["React spam"])}'

    elif args[0] == 'rps':
        if len(args)<2: return await say('Please enter rock, paper, or scissors as second argument')
        RPS = ['rock','paper','scissors']    
        userChoice = args[1].lower()
        botChoice = randItem(RPS)
        if userChoice not in RPS:
            r=f'Please enter one of the following items: {", ".join(RPS)}'
        else:
            (userChoice,botChoice,reply)=fns.rps(userChoice,botChoice)
            r=f'You chose **{userChoice}**. I (the bot) chose **{botChoice}**.\n{reply}'
    
    elif args[0] == 'recommend':
        if len(args)!=1:
            await client.get_channel(980859412564553738).send(' '.join(args[1:]))
            r='Thanks for the recommendation :D'
        else:
            r=f'Remember to recommend something\n{prefix}recommend <recommendation>'

    elif args[0] == 'google':
        r=(
        'https://www.google.com/search?q='+'+'.join(args[1:]),
        'Remember to search something'
        )[len(args)<2]

    elif args[0] in ['yt','youtube']:
        r=(
        'https://www.youtube.com/results?search_query='+'+'.join(args[1:]),
        'Remember to search something'
        )[len(args)<2]
    
    elif args[0] == 'hkwiki':
        r=(
        'https://hollowknight.fandom.com/wiki/Special:Search?query='+'+'.join(args[1:]),
        'Remember to search something'
        )[len(args)<2]

    elif args[0] == 'info':
        r='```',
        'This command is mostly for debugging btw',
        f"You're admin: {isAdmin}",
        f"You're bot owner: {isOwner}",
        f'Replies cooldown: {replyDelay}',
        f'{isBotChannel=}, {isReplyChannel=}, {isReactChannel=}',
        '```'

    elif args[0] == 'delresponse':
        ValStr=' '.join(args[1:])
        if ValStr in responses:
            del data[guildID]['Responses'][' '.join(args[1:])]
            save(data)
            r='deleted'
        else:
            r="Reply doesn't exist"
    
    elif args[0] == 'delreact':
        ValStr=' '.join(args[1:])
        if ValStr in reacts:
            del data[guildID]['Reacts'][' '.join(args[1:])]
            save(data)
            r='deleted'
        else:
            r="reply doesn't exist"

    elif args[0] == 'update' and isLinux:
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

    elif args[0] == 'restorebackup':
        rmtree(extraDir)
        copytree(savestateDir, extraDir)
        r='You restored the files: '+', '.join(os.listdir(savestateDir))
    
    elif args[0] == 'backup':
        rmtree(savestateDir)
        copytree(extraDir, savestateDir)
        r='You backuped the files: '+', '.join(os.listdir(extraDir))
    
    elif args[0] == 'zote':
        r=randItem(zoteQuotes)

    elif args[0] == 'emergencyquit':
        await say("I'm sorry for what i did :(\nBye lovely folks!")
        asySleep(0.5)
        quit()
    
    elif args[0] == 'replydelay':
        if len(args)<2:               r='Remember to add a delay time in seconds'
        elif not args[1].isnumeric(): r='Time has to be an intiger number'
        else:
            r=f'done, set reply delay to {args[1]}'
            data[guildID]['Reply delay'] = int(args[1])
            save(data)

    elif args[0] == 'makefile':
        if len(args)<3:
            r=f'Not correct syntax\n{prefix}makefile <fileName> <contents>'
        else:
            fns.openW(extraDir+args[1],args[2])
            r=f'You wrote file {args[1]} with the contents {args[2]}'
    
    elif args[0] == 'listfiles':
        r=', '.join(os.listdir(extraDir))

    elif args[0] == 'mutemyself':
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

    elif args[0] == 'channelids':
        channelsList=[(str(1+i.position),i.name,str(i.id)) for i in msg.guild.text_channels]
        lengthEach = [len(' '.join(i)) for i in channelsList]
        formatedCmdsList='\n'.join(map((lambda x, y,:f"{' '.join(x[:-1])}{y*' '} {x[-1]}"),channelsList,(max(lengthEach)-i for i in lengthEach)))
        r=f'```pos, name, {" "*(max([29]+lengthEach)-29)}ID:\n{formatedCmdsList}```'
        if len(r)>2000: r=r[:1990]+'```'

    elif args[0]=='setbotchannels':
        if 0==sum([not i.isnumeric() for i in args[1:]]):
            data[guildID]['Bot channels']=[int(i) for i in args[1:]]
            save(data)
            r ='done'
        else:r='Not valid channel IDs'

    elif args[0]=='setreplychannels':
        if 0==sum([not i.isnumeric() for i in args[1:]]):
            data[guildID]['Replies channels']=[int(i) for i in args[1:]]
            save(data)
            r ='done'
        else:r='Not valid channel IDs'
    
    elif args[0]=='setreactchannels':
        if 0==sum([not i.isnumeric() for i in args[1:]]):
            data[guildID]['Reacts channels']=[int(i) for i in args[1:]]
            save(data)
            r='done'
        else:r='Not valid channel IDs'
    
    elif args[0]=='newsettings':
        (data[guildID]['Responses'],data[guildID]['Reacts'])=[fns.openR(i) for i in [respondstxtPath,reactstxtPath]]
        save(data)
        r='done'
    
    elif args[0]=='highlow':
        x=100
        if len(args)>1 and args[1].isnumeric():
            x=int(args[1])
        await say(f'Game started. Guess a number between 1-{x}')
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
    
    elif args[0]=='settingadded':
        for i in defaultGuildSettings:
            for j in data.values():
                if i not in j:
                    for y in data:
                        data[y][i]=defaultGuildSettings[i]
                    save(data)
                break
        r='Done. Updated settings'

    elif args[0]=='eval':
        if len(args)<2:
            r='This requires two arguments minimum'
        else:
            r=eval(' '.join(args[1:]))
    
    # make an import react/response x from other discords command
    elif args[0]=='import':
        options='Responses','Reacts'
        if len(args)<2:
            r='You probably wrote improper syntax:',
            f"fo!import <which discord:id> <optional:{'/'.join(options)}> <optional:spesific reply or react>"
        elif args[1].isnumeric():
            if int(args[1]) not in data:
                r="I don't recognize the discord you tried to import from"
            else:
                if 1:1
                for option in options:
                    data[guildID][option]+=data[int(args[1])][option]
                save(data)
                r=f"Imported {', '.join(options[:-1])+' and '+options[-1]} from {dis.utils.get(client.guilds,int(args[1])).name}"

    if str(type(r)) in (f"<class '{i}'>"for i in ('tuple','list','range','generator')):
        await say(*r)
    else: await say(r)


with open(tokenPath, encoding='utf-8') as f:
    client.run(yaml.safe_load(f)['Token'])
