import discord, os, pafy, vlc, youtube_dl
from discord.ext import commands
from youtubesearchpython import VideosSearch

bot = commands.Bot(command_prefix='$')

boludos = {
    'DonHabraone#2093' : ['Victor', 1],
    'J Cresta#1514' : ['Tonecito', 0],
    'carlosfaria#3773' : ['Charles', 0]
}
messages = {
    'hola' : [
        '¡Hola! ¿Qué tal, {}?', 
        'No hablo con boludos, manito.',
        'Entra al canal de voz para escucharme, manito.'
    ],
    'esp' : 
        '¡No entiendo, puto! Solo hablo español.',
    'erro' : [
        'No recordaré esta canción. Fumé mucha marihuana.',
        'Ya estoy tocando una canción, puto.'
    ]
}
cucaracha = 'https://www.youtube.com/watch?v=jp9vFhyhNd8'
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 4', 
    'options': '-vn'
}
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(etx)s',
    'quiet': False
}


def play_music(voice_client, search_str=None, key=True):
    if voice_client.is_playing() == True:
        pass
    else:
        if key == True:
            song_url = cucaracha
        else:
            # pesquisar aqui url do vídeo usando search_str
            video_search = VideosSearch(search_str, limit=2)
            song_url = video_search.result()['result'][0]['link']
            print(song_url)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            song_info = ydl.extract_info(song_url, download=False)
        voice_client.play(
            discord.FFmpegPCMAudio(song_info["formats"][0]["url"], **FFMPEG_OPTIONS), after = lambda e: print('done')
        )


async def clean_conn_voice(ctx, bot):
    conn = 0
    user = ctx.message.author
    try:
        channel = ctx.message.channel   # AttributeError if not in a voice channel.
        voice_channel = user.voice.channel
        for bot_vc in bot.voice_clients:
            if voice_channel != bot_vc.channel:
                bot_vc.stop()
                await bot_vc.disconnect()
            else:
                conn = 1
                voice_client = bot_vc
        if conn == 0:
            voice_client = await voice_channel.connect()
        else:
            pass
    except AttributeError:
        await channel.send(messages['hola'][2])
        voice_client = None
    return voice_client


@bot.command()
async def hola(ctx):
    voice_client = await clean_conn_voice(ctx, bot)
    user = ctx.message.author
    channel = ctx.message.channel
    if voice_client != None:
        if boludos[str(user)][1] == 1:
            await channel.send(messages['hola'][1])
        else:
            await channel.send(messages['hola'][0].format(str(user)))
            play_music(voice_client)
    else:
        pass


@bot.command()
async def para(ctx):
    for voice_client in bot.voice_clients:
        voice_client.stop()
        await voice_client.disconnect()


@bot.command()
async def tocar(ctx, *args):    
    search_str = ' '.join(args)
    voice_client = await clean_conn_voice(ctx, bot)
    user = ctx.message.author
    channel = ctx.message.channel
    if voice_client != None:
        if boludos[str(user)][1] == 1:
            await channel.send(messages['hola'][1])
        else:
            play_music(voice_client, search_str, False)
    else:
        pass





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