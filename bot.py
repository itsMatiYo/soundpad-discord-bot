import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from models import Command, validate_command_name, validate_command_url


bot = commands.Bot(command_prefix='-', description="ChadPaaaaad")


@bot.event
async def on_ready():
    print('I have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="-sos"))


@bot.command(name='sos')
async def help1(ctx):
    commands = Command.select().where(Command.server_id == int(ctx.guild.id))
    embed = discord.Embed(
        title='ChadPad Commands For this server',
        description="""""",
        colour=discord.Colour.dark_teal(),
    )
    if commands:
        commands_txt = ""
        for cm in commands:
            commands_txt += f"{cm.name} ,"
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
    if ctx.author.guild_permissions.administrator:
        if args:
            try:
                name = args[0]
                url = args[1]
                server_id = int(ctx.guild.id)
                if not(validate_command_name(name, server_id)):
                    await ctx.send('`A command with this name already exists`')
                elif not(validate_command_url(url, server_id)):
                    await ctx.send('`A command with this url already exists`')
                else:
                    c1 = Command.create(
                        name=args[0], url=args[1], server_id=ctx.guild.id,)
                    await ctx.send(f'Created ✅')
            except:
                await ctx.send('`-add "<name>" "<url>"`')
        else:
            await ctx.send('`-add "<name>" "<url>"`')
    else:
        await ctx.send('`Only admins can add`')


@bot.command(name='del')
async def delete(ctx, args):
    if ctx.author.guild_permissions.administrator:
        # admin permission
        obj = Command.get_or_none(Command.name == args,
                                  Command.server_id == ctx.guild.id)
        try:
            if obj:
                obj.delete_instance()
                await ctx.send('`Deleted`')
            else:
                await ctx.send(f'`No such command with {args}`')
        except:
            await ctx.send('`Couldnt delete, Reach MatiYo`')
    else:
        await ctx.send('`Only admins can delete`')


@bot.command(name='p')
async def play(ctx, args):
    # everyone except banned
    obj = Command.get_or_none(Command.name == args,
                              Command.server_id == ctx.guild.id)
    if obj:
        channel = ctx.author.voice.channel
        try:
            voice = await channel.connect()
        except:
            voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(obj.url)
        player = voice.play(source)
    else:
        await ctx.send('`No such command.404`')


@bot.command(name='dc')
async def disconnect(ctx):
    try:
        await ctx.guild.voice_client.disconnect()
    except:
        await ctx.send("`I'm not connected`")


# banned people
