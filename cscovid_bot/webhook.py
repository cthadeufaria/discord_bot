def webhook():
    import discord
    from discord import Webhook, RequestsWebhookAdapter, File
    print(os.getenv('discord_id'))
    # Create webhook
    webhook = Webhook.partial(os.getenv('discord_id'), os.getenv('discord_token'),\
    adapter=RequestsWebhookAdapter())
    
    print(os.getenv('discord_id'))
    # Send temperature as text
    # webhook.send('!play poze do rodo anos 80 II', username='Bot')
    
    # Upload image to server
    # webhook.send(file=discord.File(&quot;latest_img.jpg&quot;))

webhook()