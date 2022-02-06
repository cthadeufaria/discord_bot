# discord_bot

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