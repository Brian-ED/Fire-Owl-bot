from asyncio import sleep as asySleep
from dataclasses import dataclass
import os
import discord as dis
import yaml
from random import randint,random
import functions as fns
from platform import platform
from shutil import rmtree, copytree
from dataclasses import dataclass
from imports.vars import zoteQuotes,defaultReactsList,defaultResponsesList
isLinux = platform(True,True) != 'Windows-10'

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
adminCommands = ['NewResponse','DelResponse','DelReact','SetReplyChannels','SetReactChannels','SetBotChannels','ChannelIDs','Prefix','ReplyDelay','ReplyChance']
vip           = {486619954745966594:['EmergencyQuit']}
adminCommands.sort()
userCommands.sort()

defaultGuildSettings={'Prefix'          :'fo!',
                      'Bot channels'    :[],
                      'Replies channels':[],
                      'Reacts channels' :[],
                      'Reply delay'     :0,
                      'Replies per min' :10,
                      'Chance for reply':1,
                      'Reacts'          :defaultReactsList,
                      'Responses'       :defaultResponsesList}

global replyDelayList
replyDelayList=[]

def save(data):
    fns.openW(datatxtPath,data)

def randItem(i):
    return i[randint(0,len(i)-1)]

async def say():
    raise "say wasn't defined properly"

class c: 

    def say(x:str):''
    args            :list[str]
    lArgs           :list[str]
    isOwner         :bool
    isAdmin         :bool
    guildID         :int
    channelID       :int
    msgAuthor       :int
    data            :dict
    gData           :dict
    commands        :list[str]
    botChannels     :list[int]
    reactsChannels  :list[int]
    replyChannels   :list[int]
    responses       :list[str]
    reacts          :list[str]
    prefix          :str
    replyDelay      :int
    chanceForReply  :float
    isBotChannel    :bool
    isReplyChannel  :bool
    isReactChannel  :bool


@client.event
async def on_ready():
    await client.change_presence(activity=dis.Game(f'subscribe to FIRE OWL'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(f'In {len(client.guilds)} servers')
    print('------')

# syntax for writing emotes is <:shroompause:976245280041205780> btw
@client.event
async def on_message(msg):
    if msg.author.bot:return
    if not msg.guild: return await msg.channel.send("I don't work in DMs sadly.")

    @dataclass
    class c: 
    
        say            = msg.channel.send
        args           = msg.content.split(' ')
        lArgs          = msg.content.lower().split(' ')
        isOwner        = msg.author.id == 671689100331319316
        isAdmin        = msg.author.top_role.permissions.administrator or isOwner
        guildID        = msg.guild.id
        channelID      = msg.channel.id
        msgAuthor      = msg.author.id

        data = fns.openR(datatxtPath)
        if channelID not in data:
            data[channelID]=defaultGuildSettings
            save(data)
        gData           = data[guildID]
        
        commands = userCommands[:]
        if isOwner          :commands += ownerCommands+sum(list(vip.values()),[])
        elif isAdmin        :commands += adminCommandsw
        if msgAuthor in vip :commands += vip[msgAuthor]
        commands=[i.lower() for i in commands]

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
    if c.args[0].startswith(c.prefix):
        # HandleCommand()
        handleCommand()
    else:
        # Handle responses and such
        handleElse(c)

    if not c.isBotChannel:
        return
    c.args[0] = fns.commandHandler(c.prefix,c.args[0],c.commands)

    if args[0] in commands:
        await msg.add_reaction('???')
    else:return

    if args[0] == 'help':
        r ='List of commands: '+', '.join(userCommands)
        if isAdmin: r+='\n\nList of admin commands: '+', '.join(adminCommands)
        if isOwner: r+='\n\nList of owner commands: '+', '.join(ownerCommands)

    elif c.args[0] == 'prefix':
        if len(c.args)<2:
            r=f'Current prefix: "{c.prefix}".'
        elif ' ' in c.args[1]: r="Can't have a prefix containing a space"
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
                else:
                    r=randint(1,int(args[1]))
            else:
                r=randint(int(args[1]),int(args[2]))

    elif args[0] == 'newresponse':
        d = {'replywith:': 'Reacts', 'reactwith:': 'Responses'}
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
        r='Responses: '+', '.join(list(responses.keys()))
        r+='\nReacts: '+', '.join(list(reacts.keys()))

    elif args[0] == 'flip':
        r=msg.author.mention
        if randint(0,1):r+=' heads'
        else:           r+=' tails'

    elif args[0] == 'rps':
        if len(args)<2:
            await say('Please enter rock, paper, or scissors')
            return

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
        if len(args)<2:r='Remember to search something'
        else:r='https://www.google.com/search?q='+'+'.join(args[1:])

    elif args[0] in ['yt','youtube']:
        if len(args)<2:r='Remember to search something'
        r='https://www.youtube.com/results?search_query=' + '+'.join(args[1:])
    
    elif args[0] == 'hkwiki':
        if len(args)<2:r='Remember to search something'
        else: r='https://hollowknight.fandom.com/wiki/Special:Search?query='+'+'.join(args[1:])
    
    elif args[0] == 'info':
        r=f"""
        You're admin: {isAdmin}
        You're bot owner: {isOwner}
        Replies cooldown: {replyDelay}
        {isBotChannel=}, {isReplyChannel=}, {isReactChannel=}
        """

    elif args[0] == 'delresponse':
        ValStr=' '.join(args[1:])
        if ValStr in responses:
            del data[guildID]['Responses'][' '.join(args[1:])]
            save(data)
            r=('deleted')
        else:
            r="Reply doesn't exist"
    
    elif args[0] == 'delreact' and isOwner:
        ValStr=' '.join(args[1:])
        if ValStr in reacts:
            del data[guildID]['Reacts'][' '.join(args[1:])]
            save(data)
            r='deleted'
        else:
            r="reply doesn't exist"

    elif args[0] == 'update' and isOwner and isLinux:
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

    elif args[0] == 'makefile' and isOwner:
        if len(args)<3:
            r=f'Not correct syntax\n{prefix}makefile <fileName> <contents>'
        else:
            fns.openW(extraDir+args[1],args[2])
            r=f'You wrote file {args[1]} with the contents {args[2]}'
    
    elif args[0] == 'listfiles':
        r=', '.join(os.listdir(extraDir))
    
    elif args[0] == 'testing':
        if 'TEST' in [i.name for i in msg.guild.roles]:
            r='Role already exists'
        else:
            await msg.guild.create_role(name="TEST", colour=dis.Colour.from_rgb(0,0,0))
            r='Made role'
    elif args[0] == 'mutemyself':
        if not isOwner: return
        if len(args)<2:
            await say(f"Wrong syntax. Please rephrase the command like so:\n{prefix}muteMyself <num+s> <num+m> <num+h> <num+d>\nThey can be in any order you'd like :D")
        def check(msg):
            return msg.channel == msg.channel and msg.author.id == msgAuthor

        msg = await client.wait_for("message", check=check)
        await say(msg)

        if isLinux:
            await say("work in progress")
            return
        await say('Alright will do. For how many hours?')

        def check(msg):
            return msg.channel == msg.channel and msg.author.id == msgAuthor

        msg = await client.wait_for("message", check=check)
        await say(f"You gave the time: {msg.author}!")
        await client.create_role(msg.author.server, name="MUTED-9352",
                                 colour=dis.Colour(0),
                                 permissions=dis.Permissions(permissions=''))

        user = msg.author
        role = dis.utils.get(user.server.roles, name="MUTED-9352")
        await client.add_roles(user, role)

        roleobject = dis.utils.get(msg.guild.roles, id=730016083871793163)
        await say(f"??? Muted {msg.author.name} for {duration}{unit}")
        await user.add_roles(roleobject)
        if unit == "s":
            await asySleep(duration)
        elif unit == "m":
            await asySleep(60 * duration)
        await user.remove_roles(roleobject)
        await say(f"??? {user} was unmuted")
    
    elif args[0] == 'channelids':
        r=[[i.position,i.name,i.id] for i in msg.guild.text_channels]
    
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
            r ='done'
        else:r='Not valid channel IDs'
    
    elif args[0]=='newsettings':
        (data[guildID]['Responses'],data[guildID]['Reacts'])=[fns.openR(i) for i in [respondstxtPath,reactstxtPath]]
        save(data)
        r='done'

    if r:await say(r)

async def cHighlow(F:list)->str:
    args=F['args']
    if len(args)>1 and args[1].isnumeric():
        correct=randint(1,args[1])
        await say(f'Game started. Guess a number between 1-{args[1]}')
    else:
        correct=randint(1,100)
        await say('Game started. Guess a number between 1-100')
    
    def check(msg):
        return msg.channel.id == channelID and\
        msg.author.id == msgAuthor and\
        msg.content.isnumeric()
    
    guess=-1
    while guess!=correct:
        guess = int(await client.wait_for("message", check=check).content)
        if   guess<correct:
            await say('Higher!')
        elif guess>correct:
            await say('Lower!')
    r='You won!'

async def cSettingAdded(data:dict)->str:
    for i in defaultGuildSettings:
        for j in data.values():
            if i not in j:
                for y in data:
                    data[y][i]=defaultGuildSettings[i]
                    
    return 'Done. Updated settings'

async def cEval(args:list[str])->str:
    if len(args)>2:return 'This requires two arguments minimum'
    else:
        try:return eval(' '.join(args[1:]))
        except: return 'errored'

ownerCommands = {'Update':0,'MakeFile':0,'ListFiles':0,'Backup':0,'RestoreBackup':0,'NewSettings':0,'Testing':0,'Highlow':0,'SettingAdded':cSettingAdded,'Eval':cEval}

async def handleElse(c):
    image.png


    

with open(tokenPath, encoding='utf-8') as f:
    client.run(yaml.safe_load(f)['Token'])