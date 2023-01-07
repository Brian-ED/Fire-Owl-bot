import openai
from yaml import safe_load
with open('../../Safe/Fire-Owl-bot.yaml', encoding='utf-8') as f:
    openai.api_key = safe_load(f)['AIToken']

async def send_message(msg,content):
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
            return await msg.channel.send(response.replace('<@','<'))
        if "```" in response:
            parts = response.split("```")
            await msg.channel.send(parts[0].replace('<@','<'))
            code_block = parts[1].split("\n")
            formatted_code_block = ""
            for line in code_block:
                while len(line) > 1900:
                    formatted_code_block += line[:1900] + "\n"
                    line = line[1900:]
                formatted_code_block += line + "\n"

            for chunk in [formatted_code_block[i:i+1900] for i in range(0, len(formatted_code_block), 1900)]:
                await msg.channel.send(f"```{chunk}```".replace('<@','<'))

            if len(parts) >= 3:
                await msg.channel.send(parts[2].replace('<@','<'))
            return
            
        response_chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
        for chunk in response_chunks:
            await msg.channel.send(chunk.replace('<@','<'))
    except Exception as e:
        await msg.channel.send("> **Error: Something went wrong, please try again later!**")
        print(f"Error while sending message: {e}")

