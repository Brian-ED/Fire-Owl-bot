@client.event
async def on_message_delete(msg):
    if msg.author.bot or not msg.guild:return
    
    history=await msg.channel.history(limit=200).flatten()
    historyCon=[i.content for i in history]

    if msg.content in historyCon:
        pos=historyCon.index(msg.content)
        if history[pos-1].author.id == client.user.id:
            await history[pos-1].delete()

list(i.content for i in await (await client.fetch_channel(981681987897143376)).history(limit=200).flatten())