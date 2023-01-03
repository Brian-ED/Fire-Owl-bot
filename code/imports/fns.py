from functools import reduce
import inspect
import youtube_dl as ytdl
import discord as dis
from asyncio import run_coroutine_threadsafe, TimeoutError, create_task
from typing import Iterable, MutableSequence, Union, Any, Callable

# These useless classes are for IDE autocompletion+coloring
class ChannelID(int):1
class TimeType(float):1
class UserID(int):1
ChannelID, UserID = type('int', (object,), vars(int).copy()), type('int', (object,), vars(int).copy())
TimeType = type('float', (object,), vars(float).copy())

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)
    def __matmul__(self, x):
        print("works")
        print(x)

def InV2(text:str, searchIn:Union[str,list]):
    searchStr=' '.join(searchIn) if type(searchIn)==list else searchIn
    return ' '+text+' ' in searchStr or text==searchStr or searchStr.startswith(text+' ') or searchStr.endswith(' '+text)

def Curry(f:Callable,*x,**xx:Any)->Callable:
    def g(*y,**yy):
        yl=list(y)
        return f(*(i if i!=Any else yl.pop() for i in x),*yl,**yy,**xx)
    return g


# Roll=BQNfn("""
# •rand.Range{∧´𝕩∾⊸∊'0'+↕10?
#     ≠◶⟨𝔽6,𝔽 1+⍟≤⊑,(⊣+⟜𝔽 1+-˜)´∧⟩10⊸×⊸+˜´∘⌽∘-⟜'0'¨𝕩
#     ;"This command only accepts integers"⋈1+𝕩/⟜↕⟜≠˜¬𝕩∧´∘∊¨<'0'+↕10
# }""")

def Join(i)->str:
    return ', '.join(sorted(i))

#rps=BQNfn("""{
#draw←"Ah we drew the game m'lad, well played"
#sciRock←"Ha i see, my scissors seem to be no match for thy mighty rock <:hmm:987400356877176912>"
#paperRock←"Haha i got ya there! you see my paper is basically made of steel so you never had a chance with that sand-particle worth of a rock!"
#rockScissors←"Ha i won! My beutiful rock never fails against your unsharpened baby scissors <:KEKW:987400181140041729>"
#paperScissors←"Oh i lost! Y'know i got that paper from my grandma before she died... :(... Ha just kidding, totally got you there :)"
#rockPaper←"Did... did you just wrap your paper around my rock and assume i can't still throw it?.. wdym it's in the rules?.. God damnit"
#scissorsPaper←"Ha my mighty metal scissors can cut throgh any paper! Y'know, your paper might aswell be taken right out of the toilet roll for how much of a fight it put up!"
#map←[
#    draw‿paperRock‿paperScissors
#    rockPaper‿draw‿scissorsPaper
#    rockScissors‿paperScissors‿draw
#]
#rps←𝕨
#Lower←+⟜(32×1="A["⊸⍋)
#3 •rand.Range⊸{botChoice 𝕊 userChoice:
#    "You chose **"∾(𝕩⊑rps)∾"**. I (the bot) chose **"∾(𝕨⊑rps)∾"**.
#    "∾𝕩‿𝕨⊑map
#}⊑1⊐˜rps≡¨<Lower 𝕩
#}""")

def openR(path:str):
    with open(path, "r", encoding="utf-8") as f:
        return eval(f.read())
def openW(path:str,value):
    with open(path, "w", encoding="utf-8") as f:
        f.write(repr(value))

def game(boardSize,maxMoves=None): # none means infinite
    1

def isMetheusEmote(x:str):
    return x[:8] in {':P1Relic',':P2Relic'}

def indexInto(indexables:list[list],indexes:Iterable[int]):
    return tuple(tuple(z[i]for i in indexes)for z in indexables)

def ext(l:list[int]):
    return l+(6-len(l))*[l[-1]]
    
def Min(*x):
    if len(x)==1:return x[0]
    else: return min(*x)

def Max(*x):
    if len(x)==1:return x[0]
    else: return max(*x)

def min2(s:MutableSequence[int])->list[int,int]:
    z=Min(*s)
    s.remove(z)
    return [z,Min(*s)]

async def metheus(client:dis.Client,msg:dis.Message,say):
    x='>'.join(msg.content.split('<')).split('>')[1::2]
    p1,p2=(tuple('<'+i+'>' for i in x if (i[2]==z and isMetheusEmote(i))) for z in '12')
    if len(p1)!=6 or len(p2)!=6:
        return'Wrong syntax. Please include 6 symbols for each player, which means 6 that start with P1, and 6 that start with P2'
    await say('Succesful input. Your input was:',''.join(p1),''.join(p2))

    def Outside(m):
        try:
            return m.emoji[0]
        except:return ""

    def check(m:dis.Reaction,author):
        return all((
            author==msg.author,
            sentMsg.id==m.message.id,
            Outside(m).isnumeric() or m.emoji in{'🛑','↩'}
        ))

    notSolution=[0,1]

    while len(notSolution)-2!=6:
        print(notSolution)
        await say(*(''.join(i[:3])+'\n'+''.join(i[3:]) for i in indexInto([p1,p2],ext(notSolution))))
        sentMsg=await say('How many yellows?')
        async def addReactions(msg):
            for i in ("0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","🛑","↩"):
                if not (sentMsg is msg):break
                await msg.add_reaction(i)
        create_task(addReactions(sentMsg))
        try:
            emoji:str=(await client.wait_for(
                'reaction_add',
                check=check,
                timeout=10*60
            ))[0].emoji
        except TimeoutError:
            return'Waited for too long'
        if emoji=='🛑':
            return'Game stopped'
        elif emoji=='↩':
            notSolution=notSolution[:2]+notSolution[2:-1]
        inp=int(emoji[0])
        if inp==6:return'Done'
        x=inp-len(notSolution)+2
        s=lambda i:{0,1,2,3,4,5}.difference(i)
        if x==1:
            if Max(*notSolution)+2>Max(*s(notSolution)):
                notSolution[-2]=Max(*s(notSolution))
                notSolution.pop()
                notSolution+=min2(s(notSolution))
            else:
                notSolution[-2:]=[i for i in s(notSolution) if i > notSolution[-1]][:2]
        elif x==0:
            print(notSolution)

            notSolution[-1]=notSolution.pop()
            notSolution+=min2(s(notSolution))
        elif x==2:
            notSolution.pop()
            notSolution+=min2(s(notSolution))
        else:
            await say("That's an impossible configuration")

async def in_voice_channel(msg):
    """Checks that the command sender is in the same voice channel as the bot."""
    voice = msg.author.voice
    bot_voice = msg.guild.voice_client
    return voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel

FFMPEG_BEFORE_OPTS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
#Command line options to pass to `ffmpeg` before the `-i`.
#See https://stackoverflow.com/questions/43218292/youtubedl-read-error-with-discord-py/44490434#44490434 for more information.
#Also, https://ffmpeg.org/ffmpeg-protocols.html for command line option reference.

def play_song(msg, data, client):
    data[msg.guild.id]['MusicSkipVotes']=set() # clear skip votes
    source = dis.PCMVolumeTransformer(
        dis.FFmpegPCMAudio(
            data[msg.guild.id]['MusicPlaylist'][0]["formats"][0]["url"],
            before_options=FFMPEG_BEFORE_OPTS),
        volume=80)

    def after_playing(unused): #unused variable here is for preventing error
        data[msg.guild.id]['MusicPlaylist'].pop(0)
        if data[msg.guild.id]['MusicPlaylist']:
            play_song(msg,data,client)
        else:
            run_coroutine_threadsafe(msg.guild.voice_client.disconnect(),client.loop)
    msg.guild.voice_client.play(source, after=after_playing)

def get_Video(video_url):
    with ytdl.YoutubeDL({
        "default_search" : "ytsearch",
        "format"         : "bestaudio/best",
        "quiet"          : True,
        "extract_flat"   : "in_playlist"}
    ) as ydl:
        info = ydl.extract_info(video_url, download=False)
    if "_type" in info and info["_type"] == "playlist":
        return get_Video(info["entries"][0]["url"])  # get info for first video
    else: return info

def Get(items,*indexs):
    if 1==len(indexs):
        r= items[indexs[0]]
    elif 2==len(indexs):
        r= items[indexs[0]:indexs[1]]
    elif 3==len(indexs):
        r= items[indexs[0]:indexs[1]:indexs[2]]
    else:
        r= items
    return r


C=lambda x:lambda*_,**a:x

def ArgCount(func:Callable)->int:
    return func.__code__.co_argcount-len(func.__defaults__ if func.__defaults__ else())

def HasInfArgs(Func:Callable)->bool:
    x=' '+str(inspect.signature(Func))[1:]
    return bool(x.count(' *') - x.count(' **'))

def HasInfKWArgs(Func):
    return'**'in str(inspect.signature(Func))

def intoAsync(F:Callable):
    if inspect.iscoroutinefunction(F):
        return F
    async def G(*args,**KWARGS):
        return F(*args,**KWARGS)
    return G

SToF=lambda p:lambda*x:reduce(eval(f"lambda a,b:a {p} b"),x)if len(x)!=1 else x[0]

# Function argument types abuse:
def ValidKWARGForFunc(Function,kwargs):
    anotations=*inspect.signature(Function).parameters.values(),
    kwargNames=*(i.name for i in anotations if i.default!=inspect._empty),
    tooManyArgs=set(kwargNames)-kwargs.keys()
    if tooManyArgs:
        raise Exception('Non existant kwarg: '+Join(tooManyArgs))

def getTypesOfFunc(F:Callable)->tuple:
    anotations=*inspect.signature(F).parameters.values(),
    kwargNames=*(i.name for i in anotations if i.default!=inspect._empty),
    isInfArged=0
    typesTuple=()
    for i in anotations:
        if i.default!=inspect._empty:
            break
        if i.annotation!=inspect._empty:
            typesTuple+=i.annotation,
            if i.kind==inspect._ParameterKind.VAR_POSITIONAL:
                isInfArged=1
                break
        else:
            typesTuple+=0,
    return typesTuple,isInfArged,kwargNames

async def ApplyType(value:str,typeClass:type,client:dis.Client):
    def ToFloat(x:str):
        if x.lower().replace('.','',1).replace('E','',1).isdecimal():
            return float(x)

    if int==typeClass:
        if value.isdecimal():
            return int(value)
    
    elif float==typeClass:
        return ToFloat(value)
    
    elif bool==typeClass:
        if value.lower()in('true','1','yes','agree'):
            return True
        elif value.lower()in('false','0','no','disagree'):
            return False

    elif ChannelID==typeClass:
        x=value.removeprefix('<#').removesuffix('>')
        if x.isdecimal():
            return int(x)

    elif dis.TextChannel==typeClass:
        x=value.removeprefix('<#').removesuffix('>')
        if x.isdecimal():
            return await client.fetch_channel(x)

    elif dis.User==typeClass:
        x=value.removeprefix('<@').removeprefix('!').removesuffix('>')
        if x.isdecimal():
            return await client.fetch_user(x)

    elif UserID==typeClass:
        x=value.removeprefix('<@').removeprefix('!').removesuffix('>')
        if x.isdecimal():
            return int(x)
        
    elif TimeType==typeClass:
        if value[-1]in'smhd'and value[:-1].replace('.','',1).isdecimal():
            return float(value[:-1])*(1,60,3600,86400)['smhd'.index(value[-1])]

    elif tuple==typeClass:
        return value.replace(',','_').split('_')
    
    else:
        return value

async def FitIntoFunc(Function:Callable,client:dis.Client,args,kwargs):
    argCount=ArgCount(Function)
    isInfArged=HasInfArgs(Function)
    typeMap,_,kwargNames=getTypesOfFunc(Function)

    tooManyArgs=set(kwargNames)-kwargs.keys()
    if tooManyArgs:
        return 1,'Non existant kwarg: '+Join(tooManyArgs)

    if isInfArged:
        reTypedArgs=*[await ApplyType(i,j,client) for i,j in zip(args[:len(typeMap)-1],typeMap[:-1])],
        reTypedArgs+=(*[await ApplyType(i,typeMap[-1],client)for i in args[len(typeMap)-1:]],)
    else:
        reTypedArgs=*[await ApplyType(i,j,client)for i,j in zip(args,typeMap)],

    if None in reTypedArgs:
        return 1,('Incompatable type:',
            args[reTypedArgs.index(None)])
    

    
    if argCount>len(args):
        return 1,(
            'You input too few arguments for the command.',
            f'The command needs minimum {argCount} arguments, not {len(args)}'
        )

    if not isInfArged and argCount<len(args):
        return 1,(
            'Too many arguments for the command.',
            f'The command needs {argCount} arguments, not {len(args)}'
        )
    return 0,reTypedArgs            
