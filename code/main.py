from asyncio import sleep as asySleep
import os
import discord as dis
import yaml
from random import randint,random
import functions as fns
from platform import platform
from shutil import rmtree, copytree
from imports.zote import zoteQuotes
isLinux = platform(True,True) != 'Windows-10'

# APL stuff::
if not isLinux:
    from imports.pynapl import APL
    apl=APL.APL()
    APLSafeEval=apl.fn("⎕se.Dyalog.Utils.repObj 1 ns∘Safe.Exec")
    apl.eval("⎕FIX 'file://',¯1↓⊃1⎕NPARTS'./imports/safe.dyalog/'⋄ns←⎕NS ⍬")
#apl=APL.APL(dyalog='/usr/bin/dyalog')

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

userCommands  = ['8ball', 'Help', 'Roll', 'Flip', 'rps','yt','Google','Youtube','yt','ListResponses','Info','hkWiki','Recommend','Rick','Zote','APLSafeEval','muteMyself']
adminCommands = ['NewResponse','DelResponse','DelReact','EmergencyQuit','SetReplyChannels','SetReactChannels','SetBotChannels','ChannelIDs','Prefix','ReplyDelay','ReplyChance']
ownerCommands = ['Update','MakeFile','ListFiles','Backup','RestoreBackup','NewSettings','Testing']
userCommands.sort()
adminCommands.sort()
ownerCommands.sort()


defaultGuildSettings={'Prefix'          :'fo!',
                      'Bot channels'    :[],
                      'Replies channels':[],
                      'Reacts channels' :[],
                      'Reply delay'     :0,
                      'Replies per min' :10,
                      'Chance for reply':1,
                      'Reacts'          :fns.defaultReactsList,
                      'Responses'       :fns.defaultResponsesList}

global replyDelayList
replyDelayList=[]

def save(data):
    fns.openW(datatxtPath,data)

def randItem(i):
    return i[randint(0,len(i)-1)]

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
    if not msg.guild:
        await msg.channel.send("I don't work in DMs sadly.")
        return

    say     = msg.channel.send
    args    = msg.content.split(' ')
    lArgs   = msg.content.lower().split(' ')
    isOwner = msg.author.id == 671689100331319316
    isAdmin = msg.author.top_role.permissions.administrator or isOwner

    if   isOwner: commands = [i.lower() for i in userCommands+adminCommands+ownerCommands]
    elif isAdmin: commands = [i.lower() for i in userCommands+adminCommands]
    else:         commands = [i.lower() for i in userCommands]
    

    guildID     = msg.guild.id
    channelID   = msg.channel.id
    msgAuthor   = msg.author.id

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
    isBotChannel   = (channelID in botChannels)    or (not botChannels)
    isReplyChannel = channelID in replyChannels  or not replyChannels
    isReactChannel = channelID in reactsChannels or not reactsChannels
    chanceForReply = data[guildID]['Chance for reply']

    # r will be the reply message
    r=''

    if not args[0].startswith(prefix):

        if isReactChannel:
            for i in lArgs:
                if i in reacts:
                    await msg.add_reaction(reacts[i])
                    break

        global replyDelayList
        if (channelID not in replyDelayList and isReplyChannel and random()<=chanceForReply) or isBotChannel:
            for i in lArgs:
                if i in responses:
                    await say(responses[i])
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
        r=f"You're admin: {isAdmin}\nYou're bot owner: {isOwner}\nReplies cooldown: {replyDelay}"

    elif args[0] == 'delresponse':
        try:
            data[guildID]['Responses'].pop(' '.join(args[1:]))
            save(data)
            r=('deleted')
        except:
            r="Reply doesn't exist"
    
    elif args[0] == 'delreact' and isOwner:
        try:
            data[guildID]['Reacts'].pop(' '.join(args[1:]))
            save(data)
            r='deleted'
        except:
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
        os.system("python3 main.py")
        await asySleep(0.5)
        quit()
    
    elif args[0] == 'aplsafeeval':
        if isLinux:       r='This command is still a work in progress'
        elif len(args)<2: r='You need to give something for me to evaluate'
        else:             r=APLSafeEval(' '.join(args[1:]))
    
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
        await say(f"✅ Muted {msg.author.name} for {duration}{unit}")
        await user.add_roles(roleobject)
        if unit == "s":
            await asySleep(duration)
        elif unit == "m":
            await asySleep(60 * duration)
        await user.remove_roles(roleobject)
        await say(f"✅ {user} was unmuted")
    
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

with open(tokenPath, encoding='utf-8') as f:
    client.run(yaml.safe_load(f)['Token'])