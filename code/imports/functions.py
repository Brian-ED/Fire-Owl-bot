import youtube_dl as ytdl
import discord as dis
from asyncio import run_coroutine_threadsafe, TimeoutError
from typing import Iterable, MutableSequence

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

D=lambda*g:lambda*a:g and D(*g[:-1])(g[-1](*a))or a[0]
T=lambda*g:lambda*a:g and T(*g[:-3])(g[-2](g[-3](*a),g[-1](*a)))or a[0]

def game(boardSize,maxMoves=None): # none means infinite
    1

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

async def in_voice_channel(msg):
    """Checks that the command sender is in the same voice channel as the bot."""
    voice = msg.author.voice
    bot_voice = msg.guild.voice_client
    return voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel

FFMPEG_BEFORE_OPTS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
"""
Command line options to pass to `ffmpeg` before the `-i`.
See https://stackoverflow.com/questions/43218292/youtubedl-read-error-with-discord-py/44490434#44490434 for more information.
Also, https://ffmpeg.org/ffmpeg-protocols.html for command line option reference.
"""

def _play_song(msg, data, client):
    data[msg.guild.id]['MusicSkipVotes']=set() # clear skip votes
    source = dis.PCMVolumeTransformer(
        dis.FFmpegPCMAudio(
            data[msg.guild.id]['MusicPlaylist'][0]["formats"][0]["url"],
            before_options=FFMPEG_BEFORE_OPTS),
        volume=80)

    def after_playing(unused): #unused variable here is for preventing error
        data[msg.guild.id]['MusicPlaylist'].pop(0)
        if data[msg.guild.id]['MusicPlaylist']:
            _play_song(msg,data,client)
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