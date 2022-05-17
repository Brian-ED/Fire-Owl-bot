import discord as dis
import platform
import yaml
from random import randint,random
import extra.functions as fns
client = dis.Client()
prefix = 'fo!'
txtpath = '../../txts'
respondstxtPath='../../data/Fire-Owl-bot/responds.txt'
tokenPath = '../../Safe/Fire-Owl-bot.yaml'

# path of the current script
if platform.platform(True,True) == 'Windows-10':
    isLinux=0
else:
    isLinux = 1

commands = ['8ball', 'bang', 'help', 'roll', 'flip', 'rps','google','youtube','yt','listresponses']
adminCommands=['newresponse']
commands.sort()

with open(respondstxtPath, "r", encoding="utf-8") as f:
    global responses
    responses=eval(str(f.read()))

with open(tokenPath, encoding='utf-8') as f:
    TOKEN = yaml.safe_load(f)['Token2']

with open(f'./extra/.yaml', encoding='utf-8') as ft:
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
    isAdmin=message.author.top_role.permissions.administrator
    global responses
    args = message.content.split(' ')

    if not args[0].startswith(prefix):
        for i in responses.keys():
            if i in ' '.join(args):
                await message.channel.send(responses[i])
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
        await message.channel.send(f'list of commands: {", ".join(commands)}'+result)

    elif args[0] == 'bang':
        if len(args) >= 2:
            await message.channel.send(f'https://duckduckgo.com/?q={args[1]}+{"+".join(args[2:])}')
        else: await message.channel.send('You need to include a bang, (like "!yt" for example), aswell as a search after')

    elif args[0] == '8ball':
        await message.channel.send(yamlFile['8ball'][randint(0,len(yamlFile['8ball'])-1)])

    elif args[0] == 'roll':
        if len(args) == 3:
            await message.channel.send(str(randint(int(args[1]),int(args[2]))))
        if len(args) == 2:
            await message.channel.send(str(randint(1,int(args[1]))))
        elif '0'==args[1]:
            await message.channel.send(random)
        else:
            await message.channel.send(randint(1,6))

    elif isAdmin and (args[0] == 'newresponse'):
        try:
            index=args.index('replywith:')
        except ValueError:
            await message.channel.send('You need to include "replywith:" in the message')
            return
        initiateStr=' '.join(args[1:index])
        replyStr=' '.join(args[index+1:])

        with open(respondstxtPath, "r", encoding="utf-8") as f:
            responses=eval(str(f.read()))
        
        print(responses)
        responses[initiateStr]=replyStr
        print(responses)

        with open(respondstxtPath, "w", encoding="utf-8") as f:
            f.write(str(responses))

        await message.channel.send(f'Alas it is done')

    elif args[0] == 'listresponses':
        await message.channel.send(responses)

    elif args[0] == 'flip':
        if randint(0,1):
            await message.channel.send(f'{message.author.mention} heads')
        else:
            await message.channel.send(f'{message.author.mention} tails')

    elif args[0] == 'rps':
        (userChoice,botChoice,result)=fns.rps(args)
        await message.channel.send(f'You chose **{userChoice}**. I (the bot) chose **{botChoice}**.\n{result}')
    
    elif args[0] == 'google':
    	await message.channel.send('https://www.google.com/search?q='+'+'.join(args[1:]))
    	
    elif (args[0] == 'yt') or (args[0] == 'youtube'):
    	await message.channel.send('https://www.youtube.com/results?search_query=' + '+'.join(args[1:]))

client.run(TOKEN)
