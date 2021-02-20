import discord
from discord.ext import commands
import db
from math import floor
import ref

with open('token.txt', 'r') as f: TOKEN = f.read()
PREFIX = 'h!'
client = commands.Bot(command_prefix=PREFIX)

client.remove_command('help')

data = db.DB('data')

lcs = lambda n: int((n ** 2) + n + 2) / 2

async def create_account(user):
    data.set([user, 'hp'], 100)
    data.set([user, 'lvl'], 1)
    data.set([user, 'exp'], 0)

async def add_exp(ctx, user, exp):
    data.set([str(user), 'exp'], data.get([str(user), 'exp']) + exp)

    crexp = data.get([str(user), 'exp'])
    a = 0
    while floor(crexp / 100 + 1) >= int(lcs(a)):
        a += 1

    lvlup = data.get([str(user), 'lvl']) < a - 1

    data.set([str(user), 'lvl'], a - 1)

    if lvlup:
        if type(ctx) == discord.message.Message:
            await ctx.channel.send(f'Great job {ctx.author.name}! You leveled up to level {a}.')
        else:
            await ctx.send(f'Great job {ctx.message.author.name}! You leveled up to level {a}.')

@client.command()
async def help(ctx):
    embed = discord.Embed(color=discord.Color.purple(), timestamp=ctx.message.created_at)
    embed.set_author(name="Help", icon_url=ctx.author.avatar_url)
    # embed.title("Help")
    embed.add_field(name="Commands",
                    value="h!help - This.\nh!ping - Tells you my respond time.\nh!profile - Shows you your profile.",
                    inline=False)
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
async def stats(ctx):
    user = str(ctx.message.author.id)

    if not data.has_key([], user):
        await create_account(user)

    await add_exp(ctx, user, 0)

    exp = data.get([user, "exp"])
    lvl = data.get([user, "lvl"])

    embed = discord.Embed(color=discord.Color.purple(), timestamp=ctx.message.created_at)

    embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)

    embed.add_field(name='Homie-Points <:homiepoint:812798235185774672>', value=data.get([user, 'hp']), inline=False)

    embed.add_field(name='Level', value=lvl + 1, inline=False)

    embed.add_field(name='Experience', value=f'{int(exp - ((lcs(lvl - 0)) - 1) * 100)}/{(lvl + 1) * 100}',
                    inline=False)

    await ctx.send(embed=embed)

'''@client.command()
async def debug(ctx, i):
    await buy_pet(ctx.message.author.id, i)'''


'''@client.command()
async def chexp(ctx, exp):
    await add_exp(ctx, str(ctx.message.author.id), int(exp))'''


@client.event
async def on_message(message):
    if not message.author.bot:
        if not message.content.startswith(PREFIX):

            if not data.has_key([], str(message.author.id)):
                await create_account(str(message.author.id))
            await add_exp(message, message.author.id, 5)

        await client.process_commands(message)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='h!help to see commands.'))
    print('Bot is Online!')


client.run(TOKEN)
