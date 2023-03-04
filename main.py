import discord
import requests
from discord.ext import commands

from apikeys import *

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    print("Bot is ready for use!")
    print("---------------------")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am Organon Bot")


@client.command()
async def list(ctx):
    await ctx.send("Mau List apa??")


@client.event
async def on_member_join(member):

    jokeurl = "https://jokes34.p.rapidapi.com/v1/jokes"

    # querystring = {"exclude-tags": "nsfw", "keywords": "rocket", "min-rating": "7",
    #                "include-tags": "one_liner", "number": "3", "max-length": "200"}

    headers = {
        "X-RapidAPI-Key": JOKEAPI,
        "X-RapidAPI-Host": "jokes34.p.rapidapi.com"
    }

    response = requests.request(
        "GET", jokeurl, headers=headers)

    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Wellcome to the server")
    await channel.send(response.text)


@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channe, you must be in a voice channel to run this command!")


@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")


client.run(TOKEN)
