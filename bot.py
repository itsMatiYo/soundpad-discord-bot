import os

import discord
import requests
from discord import FFmpegPCMAudio, colour
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

from models import delete_cm, filter_name, filter_server, filter_url, get_url

# reply to playing command
# and reply to other

bot = commands.Bot(command_prefix='-', description="ChadPaaaaad")

load_dotenv()
fb = os.getenv('FIREBASE_API')


# Embed
chad_pic = "https://cdn.discordapp.com/attachments/878977444873371678/887722269508513852/avatars-JinSVqyNLhx1tPzL-xSS9Sw-t500x500.jpg"


@bot.event
async def on_ready():
    print('I have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="-sos"))


@bot.command(name='sos')
async def help1(ctx):
    r = requests.get(
        f'{fb}/commands.json')
    if r.status_code != 200:
        await ctx.reply('Could not connect to db')
        return
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
        url=chad_pic)
    embed.add_field(name="Add sound", value="-add <name> <url>")
    embed.add_field(name="Delete sound", value="-del <name>")
    embed.add_field(name="Play Sound", value="-p <name>")
    embed.add_field(name="Disconnect", value="-dc")
    embed.add_field(name='Comamnds', value=commands_txt, inline=False)
    await ctx.reply(embed=embed)


@bot.command(name='add')
async def add(ctx, args):
    embed = discord.Embed(colour=discord.Colour.dark_red())
    r = requests.get(
        f'{fb}/commands.json')
    jr = r.json()
    if ctx.author.guild_permissions.administrator or ctx.author.id == 687701334467543100:
        if args:
            try:
                global name, url
                name, url = args.split(' ')
            except:
                embed.title = 'Add voice using this command:\n-add "<name>" "<url>"'
                await ctx.reply(embed=embed)

            server_id = str(ctx.guild.id)
            if filter_server(filter_name(jr, name), server_id):
                embed.title = 'A command with this name already exists'
                await ctx.reply(embed=embed)
            elif filter_server(filter_url(jr, url), server_id):
                embed.title = 'A command with this url already exists'
                await ctx.reply(embed=embed)
            else:
                try:
                    payload = '{"url":"' + str(url) + '","name": "' + \
                        str(name) + '","server":"' + str(server_id) + '"}'
                    r = requests.post(
                        f'{fb}/commands.json', data=payload)
                except:
                    embed.title = 'Contact MatiYo, DB has encountered problems.'
                    await ctx.reply(embed=embed)
                if r.status_code == 200:
                    embed.colour = discord.Colour.green()
                    embed.title = 'Created ✅'
                    await ctx.reply(embed=embed)
        else:
            embed.title = 'Add voice using this command:\n-add "<name>" "<url>"'
            await ctx.reply(embed=embed)
    else:
        embed.title = 'Only admins can add'
        await ctx.reply(embed=embed)


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
                    await ctx.reply('`Deleted ❌`')
            else:
                await ctx.reply(f'`No such command with {args}`')
        except:
            await ctx.reply('`Couldnt delete, Reach MatiYo`')
    else:
        await ctx.reply('`Only admins can delete`')


@bot.command(name='p')
async def play(ctx, args):
    # everyone except banned
    r = requests.get(
        f'{fb}/commands.json')
    jr = r.json()
    command = filter_name(filter_server(jr, str(ctx.guild.id)), args)

    if command:
        url = get_url(command)
        global voice
        channel = ctx.author.voice.channel
        if ctx.guild.voice_client:
            ch = ctx.guild.voice_client.channel
            # same channel as the person?
            if ch != channel:
                await ctx.guild.voice_client.disconnect()
                voice = await channel.connect()
            else:
                voice = ctx.guild.voice_client
        else:
            voice = await channel.connect()
        try:
            source = FFmpegPCMAudio(url)
            player = voice.play(source)
            embed = discord.Embed(
                title=f'Playing {args}🎧', colour=discord.Colour.green(), description=url)
        except:
            embed = discord.Embed(
                title=f'Could not play {args}', colour=discord.Colour.red())
        embed.set_thumbnail(url=chad_pic)
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title=f'No such command ({args})', colour=discord.Colour.dark_red())
        embed.set_thumbnail(url=chad_pic)
        await ctx.reply(embed=embed)


@bot.command(name='dc')
async def disconnect(ctx):
    try:
        await ctx.guild.voice_client.disconnect()
        await ctx.reply()
    except:
        await ctx.reply("`I'm not connected`")


@bot.event
async def on_message(msg):
    msg_content = msg.content.lower()
    # moderating chat
    mentions = ['@everyone', '@here']
    if str(msg_content[1:-2]).strip().replace(' ', '') == '' and msg_content != '.' and len(msg_content) > 5:
        await msg.delete()
    elif any(x in msg_content for x in mentions) or str(msg_content).startswith('whо is first?') :
        if not(msg.author.guild_permissions.mention_everyone):
            await msg.delete()
            try:
                role = get(msg.guild.roles, name='Muted')
                await msg.author.add_roles(role, reason="scam link (mentioning everyone or here)")
            except:
                await msg.channel.send('`Deleted mentioning everyone , because sender does not have permissions. If you wish to give these spammers a role, create a role named "Muted".`')
    elif str(msg_content).startswith('-dc'):
        await disconnect(msg)
    elif str(msg_content).startswith('-sos') or str(msg_content).startswith('-help'):
        await help1(msg)
    elif str(msg_content).startswith('-p'):
        await play(msg, msg_content[3:])
    elif str(msg_content).startswith('-add'):
        await add(msg, msg_content[5:])
    elif str(msg_content).startswith('-del'):
        await delete(msg, msg_content[5:])
