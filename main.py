import asyncio,discord,os,json,requests
from dicebot import *

client = discord.Client()

Channels=["dice","ダイス"]
AnalysisURL=os.environ["AnalysisURL"]

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_guild_join(guild):
    requests.post(AnalysisURL,json.dumps({"action":"join", "guildid":f"{guild.id}" }),headers={'Content-Type': 'application/json'})

@client.event
async def on_guild_remove(guild):
    requests.post(AnalysisURL,json.dumps({"action":"remove", "guildid":f"{guild.id}" }),headers={'Content-Type': 'application/json'})

@client.event
async def on_message(message):
    if message.author == client.user:
            return

    if str(message.channel).startswith("Direct Message with"):
        canDiceroll = True
    elif message.channel.name in Channels:
        canDiceroll = True
    else:
        canDiceroll = False


    try:
        #--character--
        if message.content.startswith('!character make'):
            await message.channel.send(f'{message.author.mention} ' +str(character.make()))
        if message.content.startswith('!character load'):
            index = message.content.replace("!character load ","")
            await message.channel.send(f'{message.author.mention} ' +str(character.load(index)))

        #--dice--
        if canDiceroll == True:

            if message.content.startswith('!help'):
                await message.channel.send(f'{message.author.mention} こちらを参照してください。\nhttps://github.com/32ba/TRPGTool/blob/master/README.md' )
                return

            try:
                n,d = map(int,message.content.split('d'))
            except ValueError:
                return
            else:
                await message.channel.send(f'{message.author.mention} result : '+ str(dice.roll(n,d)))
    except discord.errors.Forbidden:
        await message.channel.send("権限不足です。\n新しく追加された機能を使う際、Botの再連携が必要な場合があります。\n詳しくは下記のURLを参照してください。\nhttps://github.com/32ba/TRPGTool/blob/master/README.md")
        

client.run(os.environ["SECRET_TOKEN"])