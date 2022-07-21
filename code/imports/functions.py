def commandHandler(prefix:str,command:str,commands:set[str],ifEmpty='help')->str:
    if command == prefix:
        return ifEmpty
    posValues=[]
    for i in commands:
        if i.startswith(command[len(prefix):].lower()):
            posValues.append(i)
    if len(posValues)==1:
        return posValues[0]
    else:
        return ''

def rps(userChoice,botChoice):
    if userChoice == botChoice:
        r="Ah we drew the game m'lad, well played"

    elif userChoice == 'rock':
        if botChoice == 'scissors':
            r='Ha i see, my scissors seem to be no match for thy mighty rock <:hmm:987400356877176912>'
        elif botChoice == 'paper':
            r='Haha i got ya there! you see my paper is basically made of steel so you never had a chance with that sand-particle worth of a rock!'

    elif userChoice == 'scissors':
        if botChoice=='rock':
            r='Ha i won! My beutiful rock never fails against your unsharpened baby scissors <:KEKW:987400181140041729>'
        elif botChoice=='paper':
            r="Oh i lost! Y'know i got that paper from my grandma before she died... :(... Ha just kidding, totally got you there :)"
    elif userChoice == 'paper':
        if botChoice == 'rock':
            r="Did... did you just wrap your paper around my rock and assume i can't still throw it?.. wdym it's in the rules?.. God damnit"
        elif botChoice =='scissors':
            r="Ha my mighty metal scissors can cut throgh any paper! Y'know, your paper might aswell be taken right out of the toilet roll for how much of a fight it put up!"
    return (userChoice,botChoice,r)

def openR(path):
    with open(path, "r", encoding="utf-8") as f:
        return eval(str(f.read()))
def openW(path:str,value):
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(value))


def game(boardSize,maxMoves=None): # none means infinite
    1