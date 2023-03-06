import nextcord
import requests
import json
from nextcord.ext import commands
from nextcord import Member
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord import FFmpegPCMAudio

from apikeys import *

intents = nextcord.Intents.all()
intents.members = True

queues = {}


def check_queue(ctx, id):
    if queue[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)


client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.playing, name='Organon'))
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

    querystring = {"limit": "1", "page": "1"}

    headers = {
        "X-RapidAPI-Key": JOKEAPI,
        "X-RapidAPI-Host": "jokes34.p.rapidapi.com"
    }

    response = requests.request(
        "GET", jokeurl, headers=headers, params=querystring)

    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Wellcome to the server")
    await channel.send(json.loads(response.text)[0]['joke'])


@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('hallo-gais.wav')
        player = voice.play(source)
    else:
        await ctx.send("You are not in a voice channe, you must be in a voice channel to run this command!")


@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")


@client.command(pass_context=True)
async def pause(ctx):
    voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('At the moment, there is no audio playing in the voice channel!')


@client.command(pass_context=True)
async def resume(ctx):
    voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.pause():
        voice.resume()
    else:
        await ctx.send('At the moment, no song is paused!')


@client.command(pass_context=True)
async def stop(ctx):
    voice = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command(pass_context=True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(
        ctx, ctx.message.guild.id))


@client.command(pass_context=True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = source

    await ctx.send('Added to queue')


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: nextcord.Member, *, reason=None):
    await member.kick(reaseon=reason)
    await ctx.send(f'User{member} has been kicked')


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick people!")


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: nextcord.Member, *, reason=None):
    await member.ban(reaseon=reason)
    await ctx.send(f'User{member} has been banned')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban people!")

    @client.event
    async def on_message(message):

        if message.content == "Anjing":
            await message.delete()
            await message.channel.send("Don't Send That Message Again!!")


@client.command()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to run this command!")


client.run(TOKEN)
