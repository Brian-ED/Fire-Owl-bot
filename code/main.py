import discord as dis
import yaml
from random import randint,random
import extra.functions as fns
from os import getcwd
client = dis.Client()

prefix = 'fo!'
respondstxtPath = getcwd()+'/extra/responds.txt'
recommendsPath = getcwd()+'/extra/recommends.txt'
tokenPath = getcwd()+'/../../Safe/Fire-Owl-bot.yaml'

commands = ['8ball', 'help', 'roll', 'flip', 'rps','google','youtube','yt','listresponses','info','hkwiki','recommend']
adminCommands=['newresponse','delresponse']
commands.sort()

global responses
responses:dict=fns.openR(respondstxtPath)

with open(tokenPath, encoding='utf-8') as f:
    TOKEN = yaml.safe_load(f)['Token']

@client.event
async def on_ready():
    await client.change_presence(activity=dis.Game('subscribe to FIRE OWL'))
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
        print('debug')
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
        await say(ball8[randint(0,len(ball8['8ball'])-1)])

    elif args[0] == 'roll':
        if len(args) > 2:
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
        resStr=' '.join(args[1:index])
        repStr=' '.join(args[index+1:])

        responses=fns.openR(respondstxtPath)        
        responses[resStr]=repStr
        fns.openW(respondstxtPath,responses)

        await say(f'Alas it is done')

    elif args[0] == 'listresponses':
        await say('responses: '+', '.join(list(responses.keys())))

    elif args[0] == 'flip':
        if randint(0,1):r=' heads'
        else: r=' tails'
        await say(message.author.mention+r)

    elif args[0] == 'rps':
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
        else: await say(f'https://hollowknight.fandom.com/wiki/Special:Search?query={args[1]}')
    
    elif args[0] == 'info':
        if not isBrian:
            await say('is admin: '+str(isAdmin)+'\nyour user ID: '+str(message.author.id))
        elif isBrian:
            await say('is admin: '+'well yes... but actually no'+'\nyour user ID: '+str(message.author.id))

    elif args[0] == 'delresponse':
        responses=fns.openR(respondstxtPath)
        try:
            responses.pop(' '.join(args[1:]))
            await say('deleted')
        except:
            await say("reply doesn't exist")
        fns.openW(respondstxtPath,responses)
    
    elif args[0] == 'recommend':
        if len(args)<2:await say('Remember to recommend something')
        else:
            r=fns.openR(recommendsPath)
            r+=' '.join(args[1:])+'\n\n'
            fns.openW(recommendsPath,r)
            await say('Thanks for helping the bot out! :D')


client.run(TOKEN)
