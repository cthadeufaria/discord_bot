from email import message
from multiprocessing.sharedctypes import Value
from re import search
from typing import List
import discord, os, youtube_dl
from discord.ext import commands
from youtubesearchpython import VideosSearch
from parameters import Parameters
import blackjack as bj
# import python-vlc
# import pafy
import ctypes.util as u
import asyncio


a = u.find_library('opus')
discord.opus.load_opus(a)
print('Opus library loaded = ' + str(discord.opus.is_loaded()))

p = Parameters()
bot = commands.Bot(command_prefix='$', help_command=None)


def compose_message(message, separator, strList):
    def iterate(message, separator, strList):
        for c in strList:
            message += separator + str(c)
        return message

    try:
        message = iterate(message, separator, strList)
    except TypeError:
        strList = [strList]
        message = iterate(message, separator, strList)
    
    print(message)

    return message


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


async def play_music(channel, voice_client, search_str=None, key=True):
    # channel = ctx.message.channel
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


async def clean_conn_voice(ctx, clean = 0, message=1):
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
        if message == 1:
            await channel.send(p.messages['hola'][2])
        voice_client = None
    return voice_client, channel, user


async def get_message(channel, message):
    await channel.send(message)
    
    def check(m):
        return m.content != None

    try:
        msg = await bot.wait_for('message', timeout=60, check=check) # 60 seconds to reply
    except asyncio.TimeoutError:
        await channel.send("Sorry, you didn't reply in time!")
        msg = 'TimeoutError'
    # else:
        # await channel.send(msg.content)

    return str(msg.content)


async def send_message(channel, message):
    await channel.send(message)
    print(message)


#functions to display cards#
async def show_some(player,dealer,channel):
    # print("\nDealer's Hand")
    # print("<card hidden>")
    # print(' ', dealer.cards[1])
    # print("\nPlayer's Hand: ", *player.cards, sep= '\n')
    await send_message(channel, p.messages['blackjack'][7])
    await send_message(channel, p.messages['blackjack'][8])
    await send_message(channel, ' ' + str(dealer.cards[1]))
    await send_message(channel, compose_message("\nMão do Jogador: ", '\n', player.cards))


async def show_all(player,dealer,channel):
    # print("\nDealer's Hand:", *dealer.cards, sep="\n")
    # print("Dealer's Hand =",dealer.value)
    # print("\nPlayer's Hand: ", *player.cards, sep= '\n')
    # print("Player's Hand = ", player.value)
    await send_message(channel, compose_message("\nMão do Dealer: ", '\n', dealer.cards))
    await send_message(channel, compose_message("Mão do Dealer =", ' ', dealer.value))
    await send_message(channel, compose_message("\nMão do Jogador: ", '\n', player.cards))
    await send_message(channel, compose_message("Mão do Jogador =", ' ', player.value))


#functions to handle game scenarios#
async def player_busts(player,dealer,chips,channel):
    # print("Player busts!")
    await send_message(channel, p.messages['blackjack'][9])
    chips.lose_bet()


async def player_wins(player,dealer,chips,channel):
    # print("Player wins!")
    await send_message(channel, p.messages['blackjack'][10])
    chips.win_bet()


async def dealer_busts(player,dealer,chips,channel):
    # print("Dealer busts!")
    await send_message(channel, p.messages['blackjack'][11])  
    chips.win_bet()
    

async def dealer_wins(player,dealer,chips,channel):
    # print("Dealer wins!")\
    await send_message(channel, p.messages['blackjack'][12])  
    chips.lose_bet()
    

async def push(player,dealer,chips,channel):
    # print("Dealer and Player tie! It's a push.")
    await send_message(channel, p.messages['blackjack'][13])
    chips.bet = 0


async def take_bet(chips, channel):
    while True:
        try:
            chips.bet = await get_message(channel, p.messages['blackjack'][17])
            chips.bet = int(chips.bet)
        except ValueError:
            # print('Sorry, a bet must be an integer')
            await channel.send(p.messages['blackjack'][5])
            print(p.messages['blackjack'][5])
        else:
            if int(chips.bet) > chips.total:
                # print("sorry, your bet cannot exceed ", chips.total)
                await channel.send(p.messages['blackjack'][6] + str(chips.total))
                print(p.messages['blackjack'][6], chips.total)
            else:
                break


async def hit_or_stand(deck, hand, channel):
    # global playing #controls while loop
    playing = True
    while True:
        # x = input('would you like to hit or stand? Enter "h" or "s" ')
        x = await get_message(channel, p.messages['blackjack'][16])
        # if x == 'h':
        if x == 'c':
            await hit(deck, hand)
            await channel.send(p.messages['blackjack'][14])
            print(p.messages['blackjack'][14])
        # elif x == 's':
        elif x == 'p':
            # print('player stands. Dealer is playing')
            await channel.send(p.messages['blackjack'][3])
            print(p.messages['blackjack'][3])
            playing = False   
        else:
            # print('Sorry, please enter a valid response. Enter "h" or "s" ')
            await channel.send(p.messages['blackjack'][4])
            print(p.messages['blackjack'][4])
            continue
        break
    
    return playing


async def ask_new_game(channel, message):
    while True:
        new_game = await get_message(channel, message)
        # if new_game == 'y':
        if new_game == 's':
            playing = True
            break
        elif new_game == 'n':
            await channel.send(p.messages['blackjack'][2])
            print(p.messages['blackjack'][2])
            playing = False
            break
        else:
            await channel.send(p.messages['blackjack'][4])
            print(p.messages['blackjack'][4])
            continue
    
    return playing, new_game


#NOW FOR THE GAME
async def play_game(channel, playing, new_game='n'):
    while True:
        # Print an opening statement
        await channel.send(p.messages['blackjack'][0])
        
        # Create & shuffle the deck, deal two cards to each player
        deck = bj.Deck()
        print(deck)
        deck.shuffle()
        
        player_hand = bj.Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = bj.Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
        
        # Set up the Player's chips
        # if new_game != 'y':
        if new_game != 's':
            player_chips = bj.Chips()

        # Prompt the Player for their bet
        await take_bet(player_chips, channel) # function not working
        
        # Show cards (but keep one dealer card hidden)
        await show_some(player_hand, dealer_hand, channel)
        
        while playing:  # recall this variable from our hit_or_stand function
            
            # Prompt for Player to Hit or Stand
            playing = await hit_or_stand(deck, player_hand, channel)
            
            # Show cards (but keep one dealer card hidden)
            await show_some(player_hand, dealer_hand, channel) 
            
            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player_hand.value >21:
                await player_busts(player_hand, dealer_hand, player_chips, channel)
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:
            
            while dealer_hand.value <17:
                hit(deck, dealer_hand)
        
            # Show all cards
            await show_all(player_hand, dealer_hand, channel)
            
            # Run different winning scenarios
            if dealer_hand.value > 21:
                await dealer_busts(player_hand, dealer_hand, player_chips, channel)

            elif dealer_hand.value > player_hand.value:
                await dealer_wins(player_hand, dealer_hand, player_chips, channel)

            elif dealer_hand.value < player_hand.value:
                await player_wins(player_hand, dealer_hand, player_chips, channel)

            else:
                await push(player_hand, dealer_hand, player_chips, channel)
            
        
        # Inform Player of their chips total
        await channel.send(p.messages['blackjack'][1] + str(player_chips.total))
        print(p.messages['blackjack'][1], player_chips.total)
        
        # Ask to play again
        # new_game = input("would you like to play again? Enter 'y' or 'n'")
        info = await ask_new_game(channel, p.messages['blackjack'][15])
        playing = info[0]
        new_game = info[1]


@bot.command()
async def ayuda(ctx):
    emb = discord.Embed(title=p.ayuda_dict['title']['ayuda'][0], description=p.ayuda_dict['title']['ayuda'][1])
    for cmd in p.ayuda_dict['add_file'].keys():
        emb.add_field(name=cmd, value=p.ayuda_dict['add_file'][cmd], inline=False)
    await ctx.message.channel.send(embed=emb)


@bot.command()
async def hola(ctx):
    voice_client = (await clean_conn_voice(ctx))[0]
    user = (await clean_conn_voice(ctx, message=0))[2]
    channel = (await clean_conn_voice(ctx, message=0))[1]
    if voice_client != None:
        if p.boludos[str(user)][1] == 1:
            await channel.send(p.messages['hola'][1])
        else:
            await channel.send(p.messages['hola'][0].format(str(user)))
            await play_music(channel, voice_client)
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
    # user = ctx.message.author
    # channel = ctx.message.channel
    voice_client = (await clean_conn_voice(ctx))[0]
    user = (await clean_conn_voice(ctx, message=0))[2]
    channel = (await clean_conn_voice(ctx, message=0))[1]
    if voice_client != None:
        if p.boludos[str(user)][1] == 1:
            await channel.send(p.messages['hola'][1])
        else:
            await play_music(channel, voice_client, search_str, False)
    else:
        pass


@bot.command()
async def blackjack(ctx):
    user = (await clean_conn_voice(ctx))[2]
    channel = (await clean_conn_voice(ctx, message=0))[1]
    if channel != None:
        if p.boludos[str(user)][1] == 1:
            await channel.send(p.messages['hola'][1])
        else:
            playing = True
            await play_game(channel, playing)



bot.run(os.getenv('DISCORD_BOT_TOKEN'))