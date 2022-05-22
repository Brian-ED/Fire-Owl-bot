from random import randint
from typing import List, Any
def useTree(message: str, treeIN: List[str])->str:
    tree=treeIN[:]
    for m in range(0, len(message)):
        for t in range(0,len(tree)):
            try:
                if tree[t][m] != message[m]:
                    tree[t] = ""
            except: ""
    while "" in tree:
        tree.remove("")
    if len(tree) == 1:
        output = tree[0]
    elif len(tree) > 1:
        output = f"be more spesific. possible options:\n{', '.join(tree)}"
    elif len(tree) < 1:
        output = ""
    return output

#test:
#Commands = ["helloworld","helloyou","helli","iwuaigd"]
#message = "hello"
#print(useTree(message, Commands))

async def say(message,whatNeedsToBeSaid:str):
    await message.channel.send(whatNeedsToBeSaid)

def rps(args):
    RPS=['rock','paper','scissors']
    userChoice = args[1].lower()
    if not (userChoice in RPS):
        return f'Please enter one of the following items: {", ".join(RPS)}'
    botChoice  = RPS[randint(0,2)]
    if userChoice == botChoice:
        result="Ah we drew the game m'lad, well played"

    elif userChoice == 'rock':
        if botChoice == 'scissors':
            result='Ha i see, my scissors seem to be no match for thy mighty rock <:hmm:975072362083012668>'
        elif botChoice == 'paper':
            result='Haha i got ya there! you see my paper is basically made of steel so you never had a chance with that sand-particle worth of a rock!'

    elif userChoice == 'scissors':
        if botChoice=='rock':
            result='Ha i won! My beutiful rock never fails against your unsharpened baby scissors <:KEKW:975072362083012668>'
        elif botChoice=='paper':
            result="Oh i lost! Y'know i got that paper from my grandma before she died... :(... ha just kidding, totally got you there :)"

def openR(path):
    with open(path, "r", encoding="utf-8") as f:
        return eval(str(f.read()))
def openW(path,value):
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(value))

# Credits to daanolav for helping out with this one :D
# also Credits to SonOfDiclonius for spotting the case where sublist is bigger 
def isSublist(a: List[Any] , b:List[Any]) -> bool:
    #Check if b is a sublist of a
    m, n = len(a), len(b)
    if m<n: return False
    for i in range(m-n+1):
        if a[i:i+n]==b:
            return True
    return False