def commandHandler(prefix:str,cmd:str,commands:list[str])->str:
    if cmd == prefix:
        cmd+='help'
    validityTable=[i.startswith(cmd[len(prefix):].lower()) for i in commands]
    if 1==sum(validityTable):
        return commands[validityTable.index(1)]
    else:
        return ''

def rps(userChoice,botChoice):
    if userChoice == botChoice:
        r="Ah we drew the game m'lad, well played"

    elif userChoice == 'rock':
        if botChoice == 'scissors':
            r='Ha i see, my scissors seem to be no match for thy mighty rock <:hmm:975072362083012668>'
        elif botChoice == 'paper':
            r='Haha i got ya there! you see my paper is basically made of steel so you never had a chance with that sand-particle worth of a rock!'

    elif userChoice == 'scissors':
        if botChoice=='rock':
            r='Ha i won! My beutiful rock never fails against your unsharpened baby scissors <:KEKW:975072362083012668>'
        elif botChoice=='paper':
            r="Oh i lost! Y'know i got that paper from my grandma before she died... :(... ha just kidding, totally got you there :)"
    return (userChoice,botChoice,r)

def openR(path):
    with open(path, "r", encoding="utf-8") as f:
        return eval(str(f.read()))
def openW(path:str,value):
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(value))
