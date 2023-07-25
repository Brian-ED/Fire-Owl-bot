import io, random, shortuuid, chess, discord as dis, numpy as np
from threading import Timer
from datetime import datetime
from PIL import Image
from typing import Union
C = lambda x:x
print(np.empty(8,8))
def outer(dyOp, vec1, vec2):
    l1, l2 = map(len,(vec1,vec2))
    r = empty(l1, l2)
    for i in range(len(A)):
        for j in range(len(B)):
            r[i,j] = dyOp(vec1[i], vec2[j])

def addLog(player, time): 
    return {
        "player"   :player,
        "timestamp":time,
        "totals"   :0,
        "wins"     :0,
        "loses"    :0,
    }

# region generator

layout = (
    range(0, 8 ),
    range(8, 16),
    range(16,24),
    range(24,32),
    range(32,40),
    range(40,48),
    range(48,56),
    range(56,64),
)


def generate(board: chess.BaseBoard) -> Image:
    chessboard = Image.open("resources/chessboard.png")

    for y in range(8):
        for x in range(8):
            piece = board.piece_at(layout[y][x])

            if piece is None:
                continue

            piece = Image.open(path(piece)).convert("RGBA")
            
            chessboard.paste(piece, (25+84.5*x, 25+84.5*y), piece)

    return chessboard

def path(piece: chess.Piece) -> Union[str, None]:
    path = "resources/"

    if piece.color == chess.WHITE: path += "white/"
    if piece.color == chess.BLACK: path += "black/"

    if piece.piece_type == chess.PAWN  : path += "pawn.png"
    if piece.piece_type == chess.KNIGHT: path += "knight.png"
    if piece.piece_type == chess.BISHOP: path += "bishop.png"
    if piece.piece_type == chess.ROOK  : path += "rook.png"
    if piece.piece_type == chess.QUEEN : path += "queen.png"
    if piece.piece_type == chess.KING  : path += "king.png"

    return path

# endregion generator



def makeInvite(challenger: dis.Member, challenged: dis.Member, guild: dis.Guild):
    x = {
        'invites':[],
        'challenger':challenger,
        'challenged':challenged,
        'guild'     :guild,
        'timestamp' :datetime.now().strftime("%d-%m-%Y %H:%M"),
    }
    def expire(invite):
        

        if invite in data[guildID]["invites"]:
            data[guildID]["invites"].pop(invite)
    Timer(300.0, expire, x).start()
    return x

def makeGame(white: dis.Member, black: dis.Member, guild: dis.Guild):
    return {
        'id':shortuuid.ShortUUID().random(length = 6),
        'white':white, 'black':black,
        'guild':guild,
        'board':chess.Board(),
    }

def get_member_by_name(guild: dis.Guild, name: str) -> dis.Member:
    for member in guild.members:
        if member.name.lower() == name.lower():
            return member
            
        if member.nick is not None and member.nick.lower() == name.lower():
            return member

### Example

def DelDataSlot(slot,*arguments,data={},guildID=0,Save=0,**_):
    ValStr=' '.join(arguments)
    if ValStr in data[guildID][slot]:
        del data[guildID][slot][ValStr]
        Save(data)
        return'deleted'
    return"Reply doesn't exist"

# Sends an invite for a new match to a specified `user`
def new(ctx, user = None): # create invite
    author, guild = ctx.message.author, ctx.message.author.guild

    user = get_member_by_name(guild, user)

    if author == user: 
        return "You cannot challenge yourself"

    if user is None:
        return "Please specify a valid user to challenge"

    if get_game_from_user(user):
        return "You cannot send invitations to a person who is already playing"

    if get_game_from_user(author): 
        return "You cannot send other invitations while you are in the middle of a match"

    for invite in data[guildID]["invites"]:
        if invite.challenger == author and invite.challenged == user and invite.guild == guild:
            return "You have already invited this user"

    data[guildID]["invites"].append((author, user, guild))

    return f"{user.mention}, {author.name} wants to play a chess match against you! Use `!chess accept {author.name}` if you want to accept the invite"

# Accepts an invite sent by a specified `user` and starts a new match
async def accept(ctx, user = None, say=C):
    author, guild = ctx.message.author, ctx.message.author.guild
    user = get_member_by_name(guild, user)

    if user is None:
        return "Please, specify a valid user to accept his invite"

    if get_game_from_user(user):
        return "The selected player is already playing, wait until he is done"

    if get_game_from_user(author): 
        return "You cannot accept other invitations while you are in the middle of a match"

    invite = None

    for index, element in enumerate(data[guildID]["invites"]):
        if (element["challenged"], element["challenger"], element["guild"]) == (user, author, guild):
            invite = element
            del data[guildID]["invites"][index]
            break

    if invite is None:
        return "No invite has been sent by the selected user"

    white, black = random.sample([author, user], 2)
    
    game = Game(white, black, guild)
    data[guildID]["games"].append(game)

    file = get_binary_board(game.board)

    def Name(user:dis.Member):
        return user.nick if user.nick else user.display_name

    await say((
        "Match started!"
        f"{Name(white)} as white!"
        "VS"
        f"{Name(black)} as black!"
        f"**Match ID: {game.id}**"
    ), file = file)


# Shows every out-going and in-coming invites for the context user
async def invites(msg=C, **_):
    author, guild = msg.message.author, msg.message.author.guild

    embed = dis.Embed(title = f"Invitations for {author.name}", color = 0x00ff00)
    outcoming, incoming = str(), str()

    for invite in data[guildID]["invites"]:
        if invite.challenger == author and invite.guild == guild:
            challenged = invite.challenged
            outcoming += f"You to {challenged.name} - {invite.timestamp}\n"; continue
            
        if invite.challenged == author and invite.guild == guild:
            challenger = invite.challenger
            incoming += f"{challenger.name} to you - {invite.timestamp}\n"; continue

    if not outcoming: outcoming = "No out-coming invitations for you"
    embed.add_field(name = ":arrow_right: Out-coming invites", value = outcoming, inline = False)

    if not incoming: incoming = "No in-coming invitations for you"
    embed.add_field(name = ":arrow_left: In-coming invites", value = incoming, inline = False)

    await say(embed = embed)

async def move(ctx, initial, final):
    author = ctx.message.author

    game = get_game_from_user(author)

    if game is None:
        return "You are not playing any match in this server"

    color = None

    if game.white == author: color = chess.WHITE
    if game.black == author: color = chess.BLACK

    if color is not game.board.turn:
        return "It is not your turn to make a move"

    message = f"{game.white.mention} VS {game.black.mention} - Actual turn: `{('BLACK', 'WHITE')[not game.board.turn]}`"

    try: initial = chess.parse_square(initial)
    except ValueError: return "The initial square is invalid. Check that its format is correct: <Letter from A to H> + <Number from 1 to 8>"

    try: final = chess.parse_square(final)
    except ValueError: return  "The final square is invalid. Check that its format is correct: <Letter from A to H> + <Number from 1 to 8>"

    move = chess.Move(initial, final)

    if move not in game.board.legal_moves: 
        return "Illegal move for the selected piece"

    game.board.push(move)

    if game.board.is_checkmate():
        message = f"**Match Finished** - {game.white.mention} VS {game.black.mention} - `{author.name}` won the chess match, CONGRATULATIONS!"
        Game.games.remove(game)
        if color == chess.WHITE: update_statitics(game.white, game.black)
        if color == chess.BLACK: update_statitics(game.black, game.white)

    file = get_binary_board(game.board)
    await ctx.send(message, file = file)

# Shows the current match chessboard disposition
async def ShowChessboard(ctx):
    author = ctx.message.author

    game = get_game_from_user(author)

    if game is None:
        return "You are not playing any match in this server"

    file = get_binary_board(game.board)

    await say(f"{game.white.mention} VS {game.black.mention} - Actual turn: `{('BLACK', 'WHITE')[game.board.turn]}`", file = file)

# Surrender and lose the current match
async def surrender(ctx):
    author = ctx.message.author

    game = get_game_from_user(author)

    if game is None:
        return "You are not playing any match in this server"

    assert author in (game['white'], game['black']) 
    winner = game['black'] if game['white'] == author else game['white']

    data[guildID][games].pop(game)
    if game.white == author: update_statitics(game.black, game.white)
    if game.black == author: update_statitics(game.white, game.black)

    await ctx.send(f"{game.white.mention} VS {game.black.mention} - `{author.name}` surrended, `{winner.name}` won the match, CONGRATULATIONS!")

# Shows the statistics of a Discord user who played at least one match. If `user` is omitted, the context user stats will be shown
async def statistics(ctx, user = None):
    author, guild = ctx.message.author, ctx.message.author.guild

    member = get_member_by_name(guild, user or author.name)

    if member is None:
        return "No user found in the current server"

    embed = dis.Embed(color = 0x0000ff)

    try: 
        statistics = data[guildID]["games"][member.id]
        
        value = (
            f":vs: Number of matches played: {statistics['totals']}\n\n"
            f":blue_circle: Number of matches won: {statistics['wins']}\n"
            f":red_circle: Number of matches lost: {statistics['loses']}\n\n"
            f":clock4: Last match date: {statistics['timestamp'].strftime('%d-%m-%Y %H:%M')}"
        )

        embed.add_field(name = f"Chess-Bot Statistics of {member['name']}#{member['discriminator']}", value = value)
    except: 
        embed.add_field(name = "Information:", value = "The selected player has never played a game, his stats are therefore not available")

    await ctx.send(embed = embed)

def get_game_from_user(user: dis.Member) -> dict:
    for game in data[guildID]['games']:
        if user in (game['white'], game['black']):
            return game

def get_binary_board(board) -> dis.File:
    size = 500, 500

    with io.BytesIO() as binary:
        board = generate(board).resize(size, Image.ANTIALIAS)
        board.save(binary, "PNG"); binary.seek(0)
        return dis.File(fp = binary, filename = "board.png")

def update_statitics(winner: dis.Member, loser: dis.Member):
    winner = data[guildID][winner.id]
    loser  = data[guildID][loser.id]
    winner['wins' ] += 1
    loser ['loses'] += 1

    now = datetime.now()
    for i in (winner, loser):
        i['totals'] += 1
        i['timestamp'] = now