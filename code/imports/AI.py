import openai
from yaml import safe_load
import discord as dis
NN=dis.AllowedMentions(everyone=False, users=False, roles=False)
with open('../../Safe/Fire-Owl-bot.yaml', encoding='utf-8') as f:
    openai.api_key = safe_load(f)['AIToken']
OFF=False
async def send_message(msg,content):
    if OFF and msg.guild.id==497131548282191892:
        await msg.channel.send("this command was turned off temporarily by Brian")
        return
    aiResponse = openai.Completion.create(
        model="text-davinci-003",
        prompt=content,
        temperature=0.7,
        max_tokens=2048,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    ).choices[0].text
    try:
        response = f"> **{msg.author.display_name}**\n\n{content}{aiResponse}"
        if len(response) <= 1900:
            return await msg.channel.send(response,allowed_mentions=NN)
        if "```" in response:
            parts = response.split("```")
            await msg.channel.send(parts[0],allowed_mentions=NN)
            code_block = parts[1].split("\n")
            formatted_code_block = ""
            for line in code_block:
                while len(line) > 1900:
                    formatted_code_block += line[:1900] + "\n"
                    line = line[1900:]
                formatted_code_block += line + "\n"

            for chunk in [formatted_code_block[i:i+1900] for i in range(0, len(formatted_code_block), 1900)]:
                await msg.channel.send(f"```{chunk}```",allowed_mentions=NN)

            if len(parts) >= 3:
                await msg.channel.send(parts[2],allowed_mentions=NN)
            return
            
        response_chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
        for chunk in response_chunks:
            await msg.channel.send(chunk,allowed_mentions=NN)
    except Exception as e:
        await msg.channel.send("> **Error: Something went wrong, please try again later!**")
        print(f"Error while sending message: {e}")

