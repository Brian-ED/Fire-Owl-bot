from asyncio import sleep as asySleep
import os
import discord as dis
import yaml
from random import randint,random
import functions as fns
from platform import platform
from sympy import S as mathEval
from shutil import rmtree, copytree

client = dis.Client()

prefix = 'fo!'
respondstxtPath='./extra/responds.txt'
reactstxtPath='./extra/reacts.txt'
tokenPath = '../../Safe/Fire-Owl-bot.yaml'
recommendsPath = './extra/recommends.txt'
botDir = '../'
codeDir='./'
extraDir='./extra'
savestateDir = "../../data/data/Fire-Owl-data"
isLinux=platform(True,True) != 'Windows-10'
if not isLinux:
    loc             = 'C:/Users/brian/Persinal/discBots/'
    savestateDir    = loc+"data/Fire-Owl-data"
    extraDir        = loc+'Fire-Owl-bot/code/extra/'
    recommendsPath  = extraDir+'recommends.txt'
    respondstxtPath = extraDir+'responds.txt'
    reactstxtPath   = extraDir+'reacts.txt'
    tokenPath       = loc+'Safe/Fire-Owl-bot.yaml'
    botDir          = loc+'Fire-Owl-bot/'
    codeDir         = botDir+'code/'


rmtree(extraDir)
copytree(savestateDir, extraDir)

userCommands = ['8ball', 'help', 'roll', 'flip', 'rps','google','youtube','yt','listresponses','info','hkwiki','recommend','rick','zote','calculate']
userCommands.sort()
adminCommands=['newresponse','delresponse','delreact','restorebackup']
adminCommands.sort()
global responses,reacts
responses:dict = fns.openR(respondstxtPath)
reacts:dict = fns.openR(reactstxtPath)

@client.event
async def on_ready():
    global dataChannel
    dataChannel = client.get_channel(979056674503540806)
    await client.change_presence(activity=dis.Game(f'subscribe to FIRE OWL {client.guilds[0].member_count}'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# syntax for writing emotes is <:shroompause:976245280041205780> btw
@client.event
async def on_message(msg):
    say=msg.channel.send
    args = msg.content.split(' ')

    if msg.author.bot:return
    isBrian=str(msg.author.id)=='671689100331319316'
    isAdmin=msg.author.top_role.permissions.administrator and msg.guild.id=='497131548282191892' or isBrian
    if isAdmin: commands = userCommands+adminCommands
    else: commands = userCommands
    global responses,reacts,dataChannel
    
    if not args[0].startswith(prefix):
        argsL=[x.lower() for x in args]
        for i in responses.keys():
            if fns.isSublist(argsL,i.split(' ')):
                r=responses[i].split(' ')
                if len(r)>2 and 'replydelay:'==r[-2]:
                    try:
                        asySleep(int(r[-1]))
                        r=r[:-2]
                    except: print('not a number')
                await say(' '.join(r))
                break
                    
        for i in reacts.keys():
            if fns.isSublist(argsL,i.split(' ')):
                r=reacts[i].split(' ')
                if len(r)>2 and 'replydelay:'==r[-2]:
                    try:
                        asySleep(int(r[-1]))
                        r=r[1]
                    except: print('not a number')
                    await msg.add_reaction(r)
                break
        return

    args[0] = fns.commandHandler(prefix,args[0],commands)

    if args[0] == 'rick':
        await msg.author.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        await asySleep(15)
        await msg.author.send('Ok i am so sorry... please forgive me. here are some cats :D\nhttps://www.youtube.com/watch?v=VZrDxD0Za9I')
        await asySleep(200)
        await msg.author.send('cope')
        await asySleep(5)
        await msg.author.send('this can help :)\nhttps://www.youtube.com/watch?v=Lc6db8qfZEw')
    
    
    if args[0] == 'help':
        await say('list of commands:'+', '.join(commands))

    elif args[0] == '8ball':
        ball8=['Yes','No','Not sure','You know it','Absolutely not',
               'Absolutely yes','Cannot tell','Sure','Mmm, I have no idea',
               'Haha ye boi','What? no!','Yep','Nope','Maybe',"I'm too afraid to tell",
               "Sorry that's too hard to answer.",'Most likely.']
        await say(fns.randItem(ball8))

    elif args[0] == 'roll':
        if len(args)<2:
            r=randint(1,6)
        elif len(args) == 2:
            if '0'==args[1]:
                r=random()
            else:
                r=randint(1,int(args[1]))
        else:
            r=randint(int(args[1]),int(args[2]))
        await say(r)

    elif args[0] == 'newresponse' and isAdmin :
        try:
            indexOf=args.index('replywith:')
            isReact=0
        except ValueError:
            try:
                indexOf=args.index('reactwith:')
                isReact=1
            except ValueError:
                await say('You need to include " replywith: " or " reactwith: " in the message. Not both btw.')
                return

        aStr=' '.join(args[1:indexOf])
        bStr=' '.join(args[indexOf+1:])
        
        if args[-2] == 'replydelay:' and not args[-1].isnumeric():
            await say('the delay needs to be a number')
            return

        if isReact:
            reacts=fns.openR(reactstxtPath)
            reacts[aStr]=bStr
            fns.openW(reactstxtPath,reacts)
        else:
            responses=fns.openR(respondstxtPath)
            responses[aStr]=bStr
            fns.openW(respondstxtPath,responses)

        await say(f'Alas it is done')

    elif args[0] == 'listresponses':
        await say('Responses: '+', '.join(list(responses.keys()))+'\nReacts: '+', '.join(list(reacts.keys())))
    
    elif args[0] == 'calculate':
        if len(args)>1:
            await say(mathEval(' '.join(args[1:])))
        else:
            await say('Add an expression')

    elif args[0] == 'flip':
        if randint(0,1):r=' heads'
        else: r=' tails'
        await say(msg.author.mention+r)
    
    elif args[0] == 'muteMyself':
        await say('Alright will do. For how many hours?')
        

    elif args[0] == 'rps':
        if len(args)<2:
            await say('Please enter rock, paper, or scissors')
            return

        RPS = ['rock','paper','scissors']    
        userChoice = args[1].lower()
        botChoice = fns.randItem(RPS)
        if not (userChoice in RPS):
            return f'Please enter one of the following items: {", ".join(RPS)}'
        (userChoice,botChoice,r)=fns.rps(userChoice,botChoice)
        await say(f'You chose **{userChoice}**. I (the bot) chose **{botChoice}**.\n{r}')
    
    elif args[0] == 'recommend':
        if len(args)!=1:
            await client.get_channel(980859412564553738).send(' '.join(args[1:]))
            await say('Thanks for the recommendation :D')
        else:
            await say(f'Remember to recommend something\n{prefix}recommend <recommendation>')

    elif args[0] == 'google':
        if len(args)<2:await say('Remember to search something')
        await say('https://www.google.com/search?q='+'+'.join(args[1:]))

    elif args[0] in ['yt','youtube']:
        if len(args)<2:await say('Remember to search something')
        await say('https://www.youtube.com/results?search_query=' + '+'.join(args[1:]))
    
    elif args[0] == 'hkwiki':
        if len(args)<2:await say('Remember to search something')
        else: await say('https://hollowknight.fandom.com/wiki/Special:Search?query='+'+'.join(args[1:]))
    
    elif args[0] == 'info':
        await say(f"You're admin: {isAdmin}\nYour user ID: {msg.author.id}\nThis server's ID: {msg.guild.id}")

    elif args[0] == 'delresponse' and isAdmin:
        responses=fns.openR(respondstxtPath)
        try:
            responses.pop(' '.join(args[1:]))
            await say('deleted')
        except:
            await say("reply doesn't exist")
        fns.openW(respondstxtPath,responses)
    
    elif args[0] == 'delreact' and isBrian:
        reacts=fns.openR(reactstxtPath)
        try:
            reacts.pop(' '.join(args[1:]))
            fns.openW(reactstxtPath,reacts)
            await say('deleted')
        except:
            await say("reply doesn't exist")
    
    elif args[0] == 'recommend':
        if len(args)<2:
            await say('Remember to recommend something')
        else:
            r=fns.openR(recommendsPath)
            r+=' '.join(args[1:])+'\n\n'
            fns.openW(recommendsPath,r)
            await say('Thanks for helping the bot out! :D')

    elif args[0] == 'update' and isBrian and isLinux:
        await say("updating...")

        rmtree(savestateDir)
        copytree(extraDir, savestateDir)

        asySleep(.5)
        
        os.system('cd '+botDir)
        os.system('git reset --hard')
        os.system('git clean -fd')
        os.system('git pull')
        os.system('cd '+codeDir)
        os.system("python3 main.py")
        await say("done")
        asySleep(0.5)
        quit()
    
    elif args[0] == 'restorebackup':
        rmtree(extraDir)
        copytree(savestateDir, extraDir)
    
    elif args[0] == 'zote':
        await say(fns.zoteQuotes[randint(0,len(fns.zoteQuotes)-1)])
    #work in progress:::
    #elif args[0] == 'emergencybreak':
    #    if len(args)==1:
    #        await say('spesify how many hours (recommended is 1)')
    #    else:
    #        print(args[0])
    #        sleep(int(args[1]))

    elif args[0] == 'test' and isBrian:
        args.index("replydelay:")
        #await dataChannel.send('Reacts:',file=dis.File(reactstxtPath))
        #data=await dataChannel.history(limit=100).flatten()


with open(tokenPath, encoding='utf-8') as f:
    client.run(yaml.safe_load(f)['Token'])