from typing import Iterable, MutableSequence


args=['!metheus', '\n<:P1RelicNightmareFuel:1000927757448007813><:P1RelicCarrot:1000927181247103138><:P1RelicWalkingCane:1000927732693205144>', '<:P1RelicPurpleGem:1000927665932488786>', '', '', '<:P1RelicThulicite:1000927843938750545>', '<:P1RelicPurpleGem:1000927665932488786>\n<:P2Relic1:1000927494158950522>', '<:P2Relic1:1000927494158950522>', '<:P2Relic4:1000927212108787773>', '<:P2Relic9:1000927154424533042>', '<:P2Relic3:1000927196933804112>', '<:P2Relic8:1000927713458139136>\n<@975188865415536661>']
x='>'.join(''.join(args).split('<')).split('>')[1::2]

def isMetheusEmote(x:str):
    return x[:8] in {':P1Relic',':P2Relic'}

p1,p2=(tuple('<'+i+'>' for i in x if (i[2]==z and isMetheusEmote(i))) for z in '12')
print(p1,p2,sep='\n')

def throw(x):
    print(x)
    quit()

if len(p1)!=6 or len(p2)!=6:
    throw('Wrong syntax. Please include 6 symbols for each player, which means 6 that start with P1, and 6 that start with P2')

def indexInto(indexables:list[list],indexes:Iterable[int]):
    return tuple(tuple(z[i]for i in indexes)for z in indexables)

def getInput():
    inp=''
    while not inp.isnumeric() or int(inp)not in{0,1,2,3,4,5,6}:
        inp=input('How many yellows?')
    return int(inp)

def ext(l:list[int]):
    return l+(6-len(l))*[l[-1]]

def Min(*x):
    if len(x)==1:return x[0]
    else: return min(*x)

def Max(*x):
    if len(x)==1:return x[0]
    else: return max(*x)

def min2(s:MutableSequence[int])->list[int]:
    z=Min(*s)
    s.remove(z)
    return [z,Min(*s)]

notSolution=[0, 5, 1, 2, 3]

while len(notSolution)-2!=6:
    print(notSolution)
    inp=4
    found=len(notSolution)-2
    if inp-found==1:
        if Max(*notSolution)+2>Max(*{0,1,2,3,4,5}.difference(notSolution)):
            notSolution[-2]=Max(*{0,1,2,3,4,5}.difference(notSolution))
            notSolution[-1:]=min2({0,1,2,3,4,5}.difference(notSolution[:-1]))
        else:notSolution[-2:]=[i for i in {0,1,2,3,4,5}.difference(notSolution) if i > notSolution[-1]][:2]
    elif inp-found==0:
        notSolution[-1]=notSolution.pop()
        notSolution+=min2({0,1,2,3,4,5}.difference(notSolution))
    elif inp-found==2:
        notSolution.pop()
        notSolution+=min2({0,1,2,3,4,5}.difference(notSolution))


print('done')