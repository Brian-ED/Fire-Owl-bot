from random import randint
from time import time
import discord as dis
from typing import Union
from asyncio import create_task
async def Input(
        client:dis.Client,
        msg:dis.Message,
        sayThis="",
        expect:Union[list,str]="", # emojies or messages
        waitForReact=False
    ):
    """`x` can be emotes to wait for,
    or can be message to wait for,
    or a function that gets every message in the current channel as input.
    The syntax is like so:
    ```
    def f(x:dis.message):
        return 1 # one means this message does fit the criteria
    ```"""
    
    ## This code is for if we have more true/false options than just waiting for react or message
    # condListNames="waitForReact","waitForMessage"
    # if 1<sum(condList):
    #     raise Exception(
    #         "Input() got too many options being True, which were:",
    #         ' '.join((condListNames[i] for i,j in enumerate(condList) if j))
    #     )

    sentMsg= msg if type(msg)==object else await msg.channel.send(msg,wait=1)

    if waitForReact:
        async def addReactions(msg):
            for i in validEmotes:
                if not (sentMsg is msg):break
                await msg.add_reaction(i)
        create_task(addReactions(sentMsg))
        validEmotes=expect if type(expect)==list else [expect]

        def check(m:dis.Reaction,author):
            return all((
                author==msg.author,
                sentMsg.id==m.message.id,
                m.emoji in validEmotes
            ))
        emoji:str=(await client.wait_for(
            'reaction_add',
            check=check,
            timeout=10*60
        ))[0].emoji
    else:
        def check(m:dis.Message):
            return m.author==msg.author
        messageGotten:str=await client.wait_for(
            'message',
            check=check,
            timeout=10*60
        )


async def FireOwlMathGame(client:dis.Client,msg:dis.Message,say,throw):

    #variables
    validEmotes='1️⃣','2️⃣','3️⃣','➖'
    gameSelect = ""
    rules="""Functions Game Rules

    The computer will randomly generate a polynomial function (linear, quadratic or cubic) and will prompt you to guess what it is.
    Each turn, you may choose any integer between -3 and 3 as an input to put into the function.
    The computer will return an output which you can use to solve for the function.
    You have only 5 turns to beat the game, good luck!

    Press enter to return to the main menu"""

    #random function generator
    degX = randint(1, 3)
    constant = randint(-3, 3)
    coX = randint(1,3)*(-1,1)[randint(0,1)]
    if constant != 0:
        coX=abs(coX)
    if constant > 0:
        coX = -coX
    
    #check if degree is 1 and set int value to string
    degXStr = f"^{degX}"*(degX!=1)

    #check if degree is 1 or -1 and set int value to string
    coXStr = "-" if coX == -1 else str(coX)*(1!=coX)

    #print(functionStr)
    functionStr = ''.join((
        coXStr,"x",degXStr,'+'*(constant>0),str(constant)*(constant!=0)))
    
    #main menu
    startTime = time()
    while gameSelect != "s":
        print("Welcome to Functions Game!",
            "Rules (r)",
            "Start (s)")
        gameSelect = input()
        if gameSelect == "r":
            input(rules)
        if gameSelect != "s":
            continue
        

        
        for turns in range(1,7): # game loop
            sentMsg = say("\nChoose an x-value within the domain [-3,3]\nf(?): ")

            try:
                emoji:str=(await client.wait_for(
                    'reaction_add',
                    check=check,
                    timeout=10*60
                ))[0].emoji
                negate=1
                if emoji == '➖':
                    negate=-1
                    await say("Pick the number you want the negative version of")
                    emoji:str=(await client.wait_for(
                        'reaction_add',
                        check=check,
                        timeout=10*60
                    ))[0].emoji
                xInput = (1+validEmotes.index(emoji))*negate
            except TimeoutError:
                return await throw(f'Waited for too long')
            
            say(f"f({xInput}) = {xInput * coX ** degX + constant}",
            "Guess the function (e.g -3x^2+1)",
            "f(x) = ?")
            
            def checkDisMsg(m:dis.Message):
                return all((
                    m.author==msg.author,
                    sentMsg.id==m.message.id,
                    m.emoji in validEmotes
                ))
            try:
                emoji:str=(await client.wait_for(
                    'message',
                    check=checkDisMsg,
                    timeout=10*60
                ))[0].emoji
            except TimeoutError:
                return await throw(f'Waited for too long')

            if fGuess == functionStr:
                finalTime = round(time() - startTime, 2)
                score = 500 - round(finalTime) + turns * -50
                print("\nYou got the right function!",
                "Turns:",turns,
                f"Time:\n{finalTime}s",
                f"Score:\n{score}pts")
                exit()
            else:
                print("Incorrect Function")
        print("\nGame over",
        "The correct function was f(x) = " + functionStr)