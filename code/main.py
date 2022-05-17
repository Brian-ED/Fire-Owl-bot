import discord as dis
import platform
import yaml
from random import randint,random
import extra.functions as fns
client = dis.Client()

prefix = 'fo!'
respondstxtPath='./extra/responds.txt'
tokenPath = '../../Safe/Fire-Owl-bot.yaml'
yamlFile='./extra/.yaml'

isLinux=not (platform.platform(True,True) == 'Windows-10')
if not isLinux:
    respondstxtPath='C:/Users/brian/Persinal/discBots/Fire-Owl-bot/code/extra/responds.txt'
    tokenPath='C:/Users/brian/Persinal/discBots/Safe/Fire-Owl-bot.yaml'
    yamlFile= 'C:/Users/brian/Persinal/discBots/Fire-Owl-bot/code/extra/.yaml'

commands = ['8ball', 'bang', 'help', 'roll', 'flip', 'rps','google','youtube','yt','listresponses','checkinfo']
adminCommands=['newresponse','delresponse']
commands.sort()

with open(respondstxtPath, "r", encoding="utf-8") as f:
    global responses
    responses=eval(str(f.read()))

with open(tokenPath, encoding='utf-8') as f:
    TOKEN = yaml.safe_load(f)['Token2']

with open(yamlFile, encoding='utf-8') as ft:
    yamlFile = yaml.safe_load(ft)

@client.event
async def on_ready():
    await client.change_presence(activity=dis.Game('subscribe to FIRE OWL'))
    print(platform.platform(True,True))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



@client.event
async def on_message(message):
    if message.author.bot:return
    isBrian=str(message.author.id)=='671689100331319316'
    isAdmin=message.author.top_role.permissions.administrator or isBrian
    global responses
    args = message.content.split(' ')
    say=message.channel.send
    if not args[0].startswith(prefix):
        for i in responses.keys():
            if i in args:
                await say(responses[i])
                break
        return
    if len(args[0]) == len(prefix):
        args[0]=prefix+'help'
    
    args[0] = args[0][len(prefix):].lower() # makes the command inputted lowercase
    command = fns.useTree(args[0],commands) # useTree is basically auto-completion
    
    # handle if autocorrect got multiple results
    if command != '':
        if type(command) is str:
            args[0] = str(command)
        else: return

    if args[0] == 'help':
        if isAdmin: 
            result=', '+', '.join(adminCommands)
        else:
            result=''
        await say(f'list of commands: {", ".join(commands)}'+result)

    elif args[0] == 'bang':
        if len(args) >= 2:
            await say(f'https://duckduckgo.com/?q={args[1]}+{"+".join(args[2:])}')
        else: await say('You need to include a bang, (like "!yt" for example), aswell as a search after')

    elif args[0] == '8ball':
        await say(yamlFile['8ball'][randint(0,len(yamlFile['8ball'])-1)])

    elif args[0] == 'roll':
        if len(args) == 3:
            await say(str(randint(int(args[1]),int(args[2]))))
        elif '0'==args[1]:
            await say(random)
        if len(args) == 2:
            await say(str(randint(1,int(args[1]))))
        else:
            await say(randint(1,6))

    elif isAdmin and (args[0] == 'newresponse'):
        try:
            index=args.index('replywith:')
        except ValueError:
            await say('You need to include "replywith:" in the message')
            return
        initiateStr=' '.join(args[1:index])
        replyStr=' '.join(args[index+1:])

        with open(respondstxtPath, "r", encoding="utf-8") as f:
            responses=eval(str(f.read()))
        
        responses[initiateStr]=replyStr

        with open(respondstxtPath, "w", encoding="utf-8") as f:
            f.write(str(responses))

        await say(f'Alas it is done')

    elif args[0] == 'listresponses':
        # send file to Discord in message
        with open(respondstxtPath, "rb") as file:
            await say("Your file is:", file=dis.File(file, "responds.txt"))

    elif args[0] == 'flip':
        if randint(0,1):
            await say(f'{message.author.mention} heads')
        else:
            await say(f'{message.author.mention} tails')

    elif args[0] == 'rps':
        (userChoice,botChoice,result)=fns.rps(args)
        await say(f'You chose **{userChoice}**. I (the bot) chose **{botChoice}**.\n{result}')
    
    elif args[0] == 'google':
        await say('https://www.google.com/search?q='+'+'.join(args[1:]))

    elif (args[0] == 'yt') or (args[0] == 'youtube'):
        await say('https://www.youtube.com/results?search_query=' + '+'.join(args[1:]))
    
    elif args[0] == 'checkinfo':
        if not isBrian:
            await say('is admin: '+str(isAdmin)+'\nyour user ID: '+str(message.author.id))
        elif isBrian:
            await say('is admin: '+'well yes... but actually no'+'\nyour user ID: '+str(message.author.id))

    elif args[0] == 'delresponse':
        with open(respondstxtPath, "r", encoding="utf-8") as f:
            responses=eval(str(f.read()))
        try:
            responses.pop(' '.join(args[1:]))
            await say('deleted')
        except:
            await say("reply doesn't exist")
        with open(respondstxtPath, "w", encoding="utf-8") as f:
            f.write(str(responses))

client.run(TOKEN)
