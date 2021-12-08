import requests
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from dotenv import load_dotenv
import os
from models import delete_cm, filter_name, filter_server, filter_url, get_url


bot = commands.Bot(command_prefix='-', description="ChadPaaaaad")

load_dotenv()
fb = os.getenv('FIREBASE_API')


@bot.event
async def on_ready():
    print('I have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="-sos"))


@bot.command(name='sos')
async def help1(ctx):
    r = requests.get(
        f'{fb}/commands.json')
    jr = r.json()
    cmms = filter_server(jr, str(ctx.guild.id))
    embed = discord.Embed(
        title='ChadPad Commands For this server',
        description="""""",
        colour=discord.Colour.dark_teal(),
    )
    if cmms:
        commands_txt = ""
        for cm in cmms:
            commands_txt += f'{jr[cm]["name"]} , '
    else:
        commands_txt = "No commands added for now"
    embed.set_footer(text='Use this bot like a CHAD!')
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/878977444873371678/887722269508513852/avatars-JinSVqyNLhx1tPzL-xSS9Sw-t500x500.jpg")
    embed.add_field(name="Add sound", value="-add <name> <url>")
    embed.add_field(name="Delete sound", value="-del <name>")
    embed.add_field(name="Play Sound", value="-p <name>")
    embed.add_field(name="Disconnect", value="-dc")
    embed.add_field(name='Comamnds', value=commands_txt, inline=False)
    await ctx.channel.send(embed=embed)


@bot.command(name='add')
async def add(ctx, *args):
    embed = discord.Embed()
    r = requests.get(
        f'{fb}/commands.json')
    jr = r.json()
    if ctx.author.guild_permissions.administrator or ctx.author.id == 687701334467543100:
        if args:
            try:
                name = args[0]
                url = args[1]
            except:
                await ctx.send('`-add "<name>" "<url>"`')

            server_id = str(ctx.guild.id)
            if filter_server(filter_name(jr, name), server_id):
                await ctx.send('`A command with this name already exists`')
            elif filter_server(filter_url(jr, url), server_id):
                await ctx.send('`A command with this url already exists`')
            else:
                try:
                    payload = '{"url":"' + str(url) + '","name": "' + \
                        str(name) + '","server":"' + str(server_id) + '"}'
                    r = requests.post(
                        f'{fb}/commands.json', data=payload)
                except:
                    await ctx.send(f'Contact MatiYo, DB has encountered problems.')
                if r.status_code == 200:
                    await ctx.send(f'Created ✅')
        else:
            await ctx.send('`-add "<name>" "<url>"`')
    else:
        await ctx.send('`Only admins can add`')


@bot.command(name='del')
async def delete(ctx, args):
    if ctx.author.guild_permissions.administrator or ctx.author.id == 687701334467543100:
        r = requests.get(
            f'{fb}/commands.json')
        jr = r.json()
        # admin permission
        command = filter_name(filter_server(jr, str(ctx.guild.id)), args)
        try:
            if command:
                r = delete_cm(command)
                if r.status_code == 200:
                    await ctx.send('`Deleted ❌`')
            else:
                await ctx.send(f'`No such command with {args}`')
        except:
            await ctx.send('`Couldnt delete, Reach MatiYo`')
    else:
        await ctx.send('`Only admins can delete`')


@bot.command(name='p')
async def play(ctx, args):
    # everyone except banned
    r = requests.get(
        f'{fb}/commands.json')
    jr = r.json()
    command = filter_name(filter_server(jr, str(ctx.guild.id)), args)
    url = get_url(command)

    if command:
        channel = ctx.author.voice.channel
        try:
            voice = await channel.connect()
        except:
            voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(url)
        player = voice.play(source)
    else:
        await ctx.send('`No such command.404`')


@ bot.command(name='dc')
async def disconnect(ctx):
    try:
        await ctx.guild.voice_client.disconnect()
    except:
        await ctx.send("`I'm not connected`")
