import discord as dis
import platform
import yaml
from random import randint, randrange
from extra.functions import *
client = dis.Client()
prefix = 'fo!'

isLinux = 0
txtpath = '../../txts'

# path of the current script
if platform.platform(True,True) == 'Windows-10':
    isLinux=0
else:
    isLinux = 1

commands = ['8ball', 'bang', 'help', 'roll', 'flip']
commands.sort()

with open(f'../../Safe/Fire-Owl-bot.yaml', encoding='utf-8') as fp:
    TOKEN = yaml.safe_load(fp)['Token']

with open(f'./extra/.yaml', encoding='utf-8') as ft:
    yamlFile = yaml.safe_load(ft)

@client.event
async def on_ready():
    print(platform.platform(True,True))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



@client.event
async def on_message(message):
    args = message.content.split(' ')

    if len(args[0])<3:
        return
    if not args[0].startswith(prefix):
        return
    
    args[0] = args[0][len(prefix):].lower() # makes the command inputted lowercase
    command = useTree(args[0],commands) # useTree is basically auto-correct
    
    # handle if autocorrect got multiple results
    if command != '':
        if type(command) is str:
            args[0] = str(command)
        else: await message.channel.send(command)

    
    if args[0] == 'help':
        await message.channel.send(f'list of commands: {", ".join(commands)}')

    elif args[0] == 'bang':
        if len(args) >= 2:
            await message.channel.send(f'https://duckduckgo.com/?q={args[1]}+{"+".join(args[2:])}')
        else: await message.channel.send('You need to include a bang, (like "!yt" for example), aswell as a search after')
        
    elif args[0] == '8ball':
        await message.channel.send(yamlFile['8ball'][randrange(0,len(yamlFile['8ball']))])

    elif args[0] == 'roll':
        if len(args) == 2:
            await message.channel.send(str(randint(1,int(args[1]))))
        else: await message.channel.send(randint(1,6))

    elif args[0] == 'newmessage':
        print(args)

    elif args[0] == 'flip':
        if randint(0,1):
            await message.channel.send(f'{message.author.mention}Heads')
        else:
            await message.channel.send(f'{message.author.mention}Tails')
client.run(TOKEN)