# import youtube_dl as ytdl
import discord as dis
from . import vars

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
    return r

def openR(path):
    with open(path, "r", encoding="utf-8") as f:
        return eval(str(f.read()))
def openW(path:str,value):
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(value))


def game(boardSize,maxMoves=None): # none means infinite
    1


from typing import Iterable, MutableSequence


def isMetheusEmote(x:str):
    return x[:8] in {':P1Relic',':P2Relic'}


def throw(x):
    print(x)
    quit()

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

def min2(s:MutableSequence[int])->list[int]:
    z=Min(*s)
    s.remove(z)
    return [z,Min(*s)]
from asyncio import TimeoutError
async def metheus(client,msg,say,throw):

    x='>'.join(msg.content.split('<')).split('>')[1::2]

    p1,p2=(tuple('<'+i+'>' for i in x if (i[2]==z and isMetheusEmote(i))) for z in '12')
    if len(p1)!=6 or len(p2)!=6:
        return await throw('Wrong syntax. Please include 6 symbols for each player, which means 6 that start with P1, and 6 that start with P2')
    await say('Succesful input. Your input was:',''.join(p1),''.join(p2))

    def check(m:dis.Message):
        if m.channel == msg.channel\
            and m.content.isnumeric()\
            and int(m.content)in{0,1,2,3,4,5,6}\
            and int(m.content)-(len(notSolution)-2) in {0,1,2}\
            or m.content=='stop'\
            or m.content=='undo':return 1
        else:return 0

    notSolution=[0,1]

    while len(notSolution)-2!=6:
        await say(*(''.join(i[:3])+'\n'+''.join(i[3:]) for i in indexInto([p1,p2],ext(notSolution))))
        await say('How many yellows?')
        timeout=10*60
        try:inputMessage=await client.wait_for('message',check=check,timeout=timeout)
        except TimeoutError:await throw(f'Waited for too long. the time limit for this command is {timeout}')
        if inp == 'stop':return await say('Alright i stopped')
        inp=int(inputMessage.content)
        if inp==6:break
        x=inp-(len(notSolution)-2)
        if x==1:
            if Max(*notSolution)+2>Max(*{0,1,2,3,4,5}.difference(notSolution)):
                notSolution[-2]=Max(*{0,1,2,3,4,5}.difference(notSolution))
                notSolution.pop
                notSolution+=min2({0,1,2,3,4,5}.difference(notSolution))
            else:
                notSolution[-2:]=[i for i in {0,1,2,3,4,5}.difference(notSolution) if i > notSolution[-1]][:2]
        elif x==0:
            notSolution[-1]=notSolution.pop()
            notSolution+=min2({0,1,2,3,4,5}.difference(notSolution))
        elif x==2:
            notSolution.pop()
            notSolution+=min2({0,1,2,3,4,5}.difference(notSolution))
    await say('done')







class Video:
    """Class containing information about a particular video."""

    def __init__(self, url_or_search, requested_by):
        """Plays audio from (or searches for) a URL."""
        with ytdl.YoutubeDL(vars.YTDL_OPTS) as ydl:
            video = self._get_info(url_or_search)
            video_format = video["formats"][0]
            self.stream_url = video_format["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.uploader = video["uploader"] if "uploader" in video else ""
            self.thumbnail = video["thumbnail"] if "thumbnail" in video else None
            self.requested_by = requested_by

    def _get_info(self, video_url):
        with ytdl.YoutubeDL(vars.YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][0]["url"])  # get info for first video
            else:
                video = info
            return video

    def get_embed(self):
        """Makes an embed out of this Video's information."""
        embed = dis.Embed(
            title=self.title, description=self.uploader, url=self.video_url)
        embed.set_footer(
            text=f"Requested by {self.requested_by.name}",
            icon_url=self.requested_by.avatar_url)
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        return embed

