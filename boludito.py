from re import search
import discord, os, youtube_dl
from discord.ext import commands
from youtubesearchpython import VideosSearch
from parameters import Parameters
# import python-vlc
# import pafy
import ctypes.util as u

a = u.find_library('opus')
discord.opus.load_opus(a)
print('Opus library loaded = ' + str(discord.opus.is_loaded()))

p = Parameters()
bot = commands.Bot(command_prefix='$', help_command=None)


async def play_music(ctx, voice_client, search_str=None, key=True):
    channel = ctx.message.channel
    if voice_client.is_playing() == True:
        if key == False:
            await channel.send(p.messages['erro'][1])
        pass
    else:
        if key == True:
            song_url = p.cucaracha[0]
            titulo = p.cucaracha[1]
        else:
            video_search = VideosSearch(search_str, limit=2)
            song_url = video_search.result()['result'][0]['link']
            titulo = video_search.result()['result'][0]['title']
        with youtube_dl.YoutubeDL(p.ydl_opts) as ydl:
            song_info = ydl.extract_info(song_url, download=False)
        voice_client.play(
            discord.FFmpegPCMAudio(song_info["formats"][0]["url"], **p.FFMPEG_OPTIONS), after = lambda e: print('done')
        )
        await channel.send(p.messages['musica'][0].format(titulo))


async def clean_conn_voice(ctx, bot, clean = 0):
    conn = 0
    user = ctx.message.author
    try:
        channel = ctx.message.channel
        voice_channel = user.voice.channel   # AttributeError if not in a voice channel.
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
        await channel.send(p.messages['hola'][2])
        voice_client = None
    return voice_client


async def startGame(ctx, bot):
    pass


# async def start_def(ctx, bot):
#     search_str = ' '.join(args)
#     user = ctx.message.author
#     channel = ctx.message.channel
#     if voice_client != None:
#         if p.boludos[str(user)][1] == 1:
#             await channel.send(p.messages['hola'][1])
#         else:
#             await play_music(ctx, voice_client, search_str, False)


@bot.command()
async def ayuda(ctx):
    emb = discord.Embed(title=p.ayuda_dict['title']['ayuda'][0], description=p.ayuda_dict['title']['ayuda'][1])
    for cmd in p.ayuda_dict['add_file'].keys():
        emb.add_field(name=cmd, value=p.ayuda_dict['add_file'][cmd], inline=False)
    await ctx.message.channel.send(embed=emb)


@bot.command()
async def hola(ctx):
    voice_client = await clean_conn_voice(ctx, bot)
    user = ctx.message.author
    channel = ctx.message.channel
    if voice_client != None:
        if p.boludos[str(user)][1] == 1:
            await channel.send(p.messages['hola'][1])
        else:
            await channel.send(p.messages['hola'][0].format(str(user)))
            await play_music(ctx, voice_client)
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
        if p.boludos[str(user)][1] == 1:
            await channel.send(p.messages['hola'][1])
        else:
            await play_music(ctx, voice_client, search_str, False)
    else:
        pass


@bot.command()
async def blackjack(ctx, *args):
    user = ctx.message.author
    channel = ctx.message.channel
    if channel != None:
        if p.boludos[str(user)][1] == 1:
            await channel.send(p.messages['hola'][1])
        else:
            await channel.send(p.messages['acoes'][0])
            await startGame(ctx)


bot.run(os.getenv('DISCORD_BOT_TOKEN'))