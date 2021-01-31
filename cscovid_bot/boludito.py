import discord, os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$oi'):
        await message.channel.send('¡Hola! ¿Qué tal?')

client.run(os.getenv('discord_bot_token'))