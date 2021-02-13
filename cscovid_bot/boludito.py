import discord, os, pafy, vlc, youtube_dl
from discord.ext import commands
from youtubesearchpython.__future__ import *

bot = commands.Bot(command_prefix='$')

boludos = {
    'DonHabraone#2093' : ['Victor', 1],
    'J Cresta#1514' : ['Tonecito', 0]
}
messages = {
    'hola' : [
        '¡Hola! ¿Qué tal, {}?', 
        'No hablo con boludos, manito.',
        'Entra al canal de voz para escucharme, manito.'
    ],
    'esp' : 
        '¡No entiendo, puto! Solo hablo español.',
}
cucaracha = 'https://www.youtube.com/watch?v=jp9vFhyhNd8'


@bot.command()
async def hola(ctx):
    user = ctx.message.author
    channel = ctx.message.channel
    
    voice_channel = user.voice.channel
    voice_client = await voice_channel.connect()
    
    with youtube_dl.YoutubeDL() as ydl:
        song_info = ydl.extract_info(cucaracha, download=False)
    
    voice_client.play(
        discord.FFmpegPCMAudio(song_info["formats"][0]["url"]), after=lambda e: print('done', e)
    )


    @bot.command()
    async def para(ctx):
        voice_client.stop()





# bot events:
    # @bot.event
    # async def on_ready():
    #     print('We have logged in as {0.user}'.format(bot))

    # @bot.event
    # async def on_message(message):
    #     if message.author == bot.user:
    #         return

    #     # # excessão boludos
    #     # if str(message.author) in boludos.keys():
    #     #     await message.channel.send(messages['hola'][1])
    #     # #

    #     if message.content.startswith('oi'):
    #         await message.channel.send(messages['esp'])

    #     elif message.content.startswith('hola, manito'):
    #         await message.channel.send(
    #             messages['hola'][0].format(str(message.author))
    #         )

bot.run(os.getenv('discord_bot_token'))