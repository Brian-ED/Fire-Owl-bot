from asyncio import sleep as asySleep
import os
import discord as dis
import yaml
from random import randint,random
import functions as fns
from platform import platform
client = dis.Client()

prefix = 'fo!'
respondstxtPath='./extra/responds.txt'
reactstxtPath='./extra/reacts.txt'
tokenPath = '../../Safe/Fire-Owl-bot.yaml'
recommendsPath = './extra/recommends.txt'
botDir = '../'
codeDir='./'
isLinux=not (platform(True,True) == 'Windows-10')
if not isLinux:
    loc='C:/Users/brian/Persinal/discBots/'
    recommendsPath=loc+'Fire-Owl-bot/code/extra/recommends.txt'
    respondstxtPath=loc+'Fire-Owl-bot/code/extra/responds.txt'
    reactstxtPath=loc+'Fire-Owl-bot/code/extra/reacts.txt'
    tokenPath=loc+'Safe/Fire-Owl-bot.yaml'

commands = ['8ball', 'help', 'roll', 'flip', 'rps','google','youtube','yt','listresponses','info','hkwiki','recommend','rick','zote']
commands.sort()
adminCommands=['newresponse','delresponse','delreact']

global responses
responses:dict = fns.openR(respondstxtPath)
global reacts
reacts:dict = fns.openR(reactstxtPath)

@client.event
async def on_ready():
    await client.change_presence(activity=dis.Game('subscribe to FIRE OWL'))
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
    isAdmin=(msg.author.top_role.permissions.administrator and (str(msg.guild.id)=='497131548282191892')) or isBrian
    global responses
    global reacts
    
    if not args[0].startswith(prefix):
        argsL=[x.lower() for x in args]
        for i in responses.keys():
            if fns.isSublist(argsL,i.split(' ')):
                await say(responses[i])
                break
        for i in reacts.keys():
            if fns.isSublist(argsL,i.split(' ')):
                await msg.add_reaction(reacts[i])
                break
        return

    if len(args[0]) == len(prefix):
        args[0]=prefix+'help'
    
    args[0] = args[0][len(prefix):].lower() # makes the command inputted lowercase
    command = fns.useTree(args[0],commands) # useTree is basically auto-correct
    
    # handle if autocorrect got multiple results
    if command != '':
        if type(command) is str:
            args[0] = str(command)
        else: return
    
    if args[0] == 'test':
        await say('worked!')

    if args[0] == 'rick':
        await msg.author.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        await asySleep(15)
        await msg.author.send('Ok i am so sorry... please forgive me. here are some cats :D\nhttps://www.youtube.com/watch?v=VZrDxD0Za9I')
        await asySleep(200)
        await msg.author.send('cope')
        await asySleep(5)
        await msg.author.send('this can help :)\nhttps://www.youtube.com/watch?v=Lc6db8qfZEw')
    
    if args[0] == 'help':
        if isAdmin: 
            result=', '+', '.join(adminCommands)
        else:
            result=''
        await say(f'list of commands: {", ".join(commands)}'+result)

    elif args[0] == '8ball':
        ball8=['Yes','No','Not sure','You know it','Absolutely not',
               'Absolutely yes','Cannot tell','Sure','Mmm, I have no idea',
               'Haha ye boi','What? no!','Yep','Nope','Maybe',"I'm too afraid to tell",
               "Sorry that's too hard to answer.",'Most likely.']
        await say(ball8[randint(0,len(ball8)-1)])

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

        resStr=' '.join(args[1:indexOf])
        repStr=' '.join(args[indexOf+1:])

        if isReact:
            reacts=fns.openR(reactstxtPath)
            reacts[resStr]=repStr
            fns.openW(reactstxtPath,reacts)
        else:
            responses=fns.openR(respondstxtPath)
            responses[resStr]=repStr
            fns.openW(respondstxtPath,responses)

        await say(f'Alas it is done')

    elif args[0] == 'listresponses':
        await say('responses: '+', '.join(list(responses.keys()))+'\nReacts: '+', '.join(list(reacts.keys())))

    elif args[0] == 'flip':
        if randint(0,1):r=' heads'
        else: r=' tails'
        await say(msg.author.mention+r)

    elif args[0] == 'rps':
        if len(args)<2:
            return f'Please enter rock, paper, or scissors'
        (userChoice,botChoice,result)=fns.rps(args)
        await say(f'You chose **{userChoice}**. I (the bot) chose **{botChoice}**.\n{result}')
    
    elif args[0] == 'google':
        if len(args)<2:await say('Remember to search something')
        await say('https://www.google.com/search?q='+'+'.join(args[1:]))

    elif (args[0] == 'yt') or (args[0] == 'youtube'):
        if len(args)<2:await say('Remember to search something')
        await say('https://www.youtube.com/results?search_query=' + '+'.join(args[1:]))
    
    elif args[0] == 'hkwiki':
        if len(args)<2:await say('Remember to search something')
        else: await say('https://hollowknight.fandom.com/wiki/Special:Search?query='+'+'.join(args[1:]))
    
    elif args[0] == 'info':
        await say(f"You're admin: {isAdmin}\nYour user ID: {msg.author.id}\nThis server's ID: {msg.guild.id}")

    elif args[0] == 'delresponse':
        responses=fns.openR(respondstxtPath)
        try:
            responses.pop(' '.join(args[1:]))
            await say('deleted')
        except:
            await say("reply doesn't exist")
        fns.openW(respondstxtPath,responses)
    
    elif args[0] == 'delreact':
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
    
    elif (args[0] == 'update') and isBrian and isLinux:
        os.system('cd '+botDir)
        os.system('git pull')
        os.system('cd '+codeDir)
        os.system("python3 main.py")
        await say("updating...")
        asySleep(2)
        quit()
    
    elif args[0] == 'zote':
        await say(fns.zoteQuotes[randint(0,len(fns.zoteQuotes)-1)])

with open(tokenPath, encoding='utf-8') as f:
    client.run(yaml.safe_load(f)['Token'])