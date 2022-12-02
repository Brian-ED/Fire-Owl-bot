# credits to EdelfQ for the lovely TicTacToe code :D
# I will largely ignore this code for optimization because 
# i didn't make it and it works fine so far.

import discord as dis
from asyncio import create_task
from PIL import Image
import turtle


async def inputV2(client,say,inputText,emotes):
    sentMsg=await say(inputText,file=dis.File('_temporaryFiles/tictactoe.png'))
    async def addReactions(msg):
        for i in emotes:
            if not (sentMsg is msg):break
            await msg.add_reaction(i)
    create_task(addReactions(sentMsg))

    def check(m:dis.Reaction,author):
        return all((
            not author.bot,
            sentMsg.id==m.message.id,
            m.emoji in emotes
        ))
    try:
        emoji:str=(await client.wait_for(
            'reaction_add',
            check=check,
            timeout=10*60
        ))[0].emoji
    except TimeoutError:
        await say(f'Waited for too long')
        return
    return int(emoji[0])

async def TurtleGame(client,say): #Made by EdelfQ!! only thing changed was the input function
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-180, 180)
    turtle.pendown()
    turtle.goto(-180, -180)
    turtle.goto(-180, 60)
    turtle.forward(360)
    turtle.backward(5)
    turtle.penup()
    turtle.goto(-180, -60)
    turtle.pendown()
    turtle.forward(360)
    turtle.goto(180, -180)
    turtle.goto(180, 180)
    turtle.goto(-180, 180)
    turtle.goto(-180, -180)
    turtle.goto(180, -180)
    turtle.goto(60, -180)
    turtle.goto(60, 180)
    turtle.goto(-60, 180)
    turtle.goto(-60, -180)
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = 0
    i = 0
    move = 0
    unchangingEmotes="1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"
    emotes=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
    while 1:
        turtle.pencolor('red')
        turtle.getcanvas().postscript(file="_temporaryFiles/tictactoe.ps", colormode='color')
        psimage=Image.open('_temporaryFiles/tictactoe.ps')
        psimage.save('_temporaryFiles/tictactoe.png')
        index=(await inputV2(client,say,'Which tile are you going to place in?(1-9)',emotes))-1
        move = "abcdefghi"[index]
        emotes.remove(unchangingEmotes[index])

        if move == 'a':
            if a == 0:
                turtle.penup()
                turtle.goto(-180, 180)
                turtle.pendown()
                turtle.goto(-60, 60)
                turtle.goto(-180, 60)
                turtle.goto(-60, 180)
                a = 1
        if move == 'b':
            if b == 0:
                turtle.penup()
                turtle.goto(-60, 180)
                turtle.pendown()
                turtle.goto(60, 60)
                turtle.goto(-60, 60)
                turtle.goto(60, 180)
                b = 1
            b = 1
        if move == 'c':
            if c == 0:
                turtle.penup()
                turtle.goto(60, 180)
                turtle.pendown()
                turtle.goto(180, 60)
                turtle.goto(60, 60)
                turtle.goto(180, 180)
                c = 1
        if move == 'd':
            if d == 0:
                turtle.penup()
                turtle.goto(-180, 60)
                turtle.pendown()
                turtle.goto(-60, -60)
                turtle.goto(-180, -60)
                turtle.goto(-60, 60)
                d = 1
        if move == 'e':
            if e == 0:
                turtle.penup()
                turtle.goto(-60, 60)
                turtle.pendown()
                turtle.goto(60, -60)
                turtle.goto(-60, -60)
                turtle.goto(60, 60)
                e = 1
        if move == 'f':
            if f == 0:
                turtle.penup()
                turtle.goto(60, 60)
                turtle.pendown()
                turtle.goto(180, -60)
                turtle.goto(60, -60)
                turtle.goto(180, 60)
                f = 1
        if move == 'g':
            if g == 0:
                turtle.penup()
                turtle.goto(-180, -60)
                turtle.pendown()
                turtle.goto(-60, -180)
                turtle.goto(-180, -180)
                turtle.goto(-60, -60)
                g = 1
        if move == 'h':
            if h == 0:
                turtle.penup()
                turtle.goto(-60, -60)
                turtle.pendown()
                turtle.goto(60, -180)
                turtle.goto(-60, -180)
                turtle.goto(60, -60)
                h = 1
        if move == 'i':
            if i == 0:
                turtle.penup()
                turtle.goto(60, -60)
                turtle.pendown()
                turtle.goto(180, -180)
                turtle.goto(60, -180)
                turtle.goto(180, -60)
                i = 1
        if a == 1 and b == 1 and c == 1:
            await say('red wins')
            break
        if d == 1 and e == 1 and f == 1:
            await say('red wins')
            break
        if g == 1 and h == 1 and i == 1:
            await say('red wins')
            break
        if a == 1 and d == 1 and g == 1:
            await say('red wins')
            break
        if b == 1 and e == 1 and h == 1:
            await say('red wins')
            break
        if c == 1 and f == 1 and i == 1:
            await say('red wins')
            break
        if a == 1 and e == 1 and i == 1:
            await say('red wins')
            break
        if c == 1 and e == 1 and g == 1:
            await say('red wins')
            break
        if emotes==[]:
            await say('draw')
            break
        turtle.pencolor('blue')

        turtle.getcanvas().postscript(file="_temporaryFiles/tictactoe.ps", colormode='color')
        psimage=Image.open('_temporaryFiles/tictactoe.ps')
        psimage.save('_temporaryFiles/tictactoe.png')
        index=(await inputV2(client,say,'Which tile are you going to place in?(1-9)',emotes))-1
        move = "abcdefghi"[index]
        emotes.remove(unchangingEmotes[index])
        if move == 'a':
            if a == 0:
                turtle.penup()
                turtle.goto(-180, 180)
                turtle.pendown()
                turtle.goto(-60, 60)
                turtle.goto(-180, 60)
                turtle.goto(-60, 180)
                a = 2
        if move == 'b':
            if b == 0:
                turtle.penup()
                turtle.goto(-60, 180)
                turtle.pendown()
                turtle.goto(60, 60)
                turtle.goto(-60, 60)
                turtle.goto(60, 180)
                b = 2
            b = 2
        if move == 'c':
            if c == 0:
                turtle.penup()
                turtle.goto(60, 180)
                turtle.pendown()
                turtle.goto(180, 60)
                turtle.goto(60, 60)
                turtle.goto(180, 180)
                c = 2
        if move == 'd':
            if d == 0:
                turtle.penup()
                turtle.goto(-180, 60)
                turtle.pendown()
                turtle.goto(-60, -60)
                turtle.goto(-180, -60)
                turtle.goto(-60, 60)
                d = 2
        if move == 'e':
            if e == 0:
                turtle.penup()
                turtle.goto(-60, 60)
                turtle.pendown()
                turtle.goto(60, -60)
                turtle.goto(-60, -60)
                turtle.goto(60, 60)
                e = 2
        if move == 'f':
            if f == 0:
                turtle.penup()
                turtle.goto(60, 60)
                turtle.pendown()
                turtle.goto(180, -60)
                turtle.goto(60, -60)
                turtle.goto(180, 60)
                f = 2
        if move == 'g':
            if g == 0:
                turtle.penup()
                turtle.goto(-180, -60)
                turtle.pendown()
                turtle.goto(-60, -180)
                turtle.goto(-180, -180)
                turtle.goto(-60, -60)
                g = 2
        if move == 'h':
            if h == 0:
                turtle.penup()
                turtle.goto(-60, -60)
                turtle.pendown()
                turtle.goto(60, -180)
                turtle.goto(-60, -180)
                turtle.goto(60, -60)
                h = 2
        if move == 'i':
            if i == 0:
                turtle.penup()
                turtle.goto(60, -60)
                turtle.pendown()
                turtle.goto(180, -180)
                turtle.goto(60, -180)
                turtle.goto(180, -60)
                i = 2
        if a == 2 and b == 2 and c == 2:
            await say('blue wins')
            break
        if d == 2 and e == 2 and f == 2:
            await say('blue wins')
            break
        if g == 2 and h == 2 and i == 2:
            await say('blue wins')
            break
        if a == 2 and d == 2 and g == 2:
            await say('blue wins')
            break
        if b == 2 and e == 2 and h == 2:
            await say('blue wins')
            break
        if c == 2 and f == 2 and i == 2:
            await say('blue wins')
            break
        if a == 2 and e == 2 and i == 2:
            await say('blue wins')
            break
        if c == 2 and e == 2 and g == 2:
            await say('blue wins')
            break

    turtle.reset()

