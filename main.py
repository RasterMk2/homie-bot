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

'''async def lcs(n):
    return int(((n ** 2) + n + 2) / 2)'''

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


async def buy_pet(user, pet):
    user = str(user)
    if not data.has_key([user], 'pets'):
        data.set([user, 'pets'], {})
    pets = len(data.get([user, 'pets']).keys())

    data.set([user, 'pets', str(pets)], {
        'name': None, 'type': 'dog', 'lvl': 0, 'exp': 0
    })


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

    embed.add_field(name='Homie-Points:tm:', value=data.get([user, 'hp']), inline=False)

    embed.add_field(name='Level', value=lvl + 1, inline=False)

    embed.add_field(name='Experience', value=f'{int(exp - ((lcs(lvl - 0)) - 1) * 100)}/{(lvl + 1) * 100}',
                    inline=False)

    await ctx.send(embed=embed)
    # await ctx.send(f'You have {data.get([str(ctx.message.author.id), "hp"])} Homie-Points:tm:')


@client.command()
async def shop(ctx, branchf='shop'):
    branch = ref.SHOP[branchf.lower()]

    embed = discord.Embed(color=discord.Color.purple(), timestamp=ctx.message.created_at)

    if branchf == 'shop':
        for i in branch:
            embed.add_field(name=i[0], value=i[1], inline=False)
    else:
        for i in branch:
            embed.add_field(name=f'{i[0]} - {i[2]}HP:tm:$', value=f'{i[1]}\nCode: {i[3]}', inline=False)

    await ctx.send(embed=embed)


@client.command()
async def buy(ctx, item=None, qnt=1):
    user = str(ctx.message.author.id)

    if item:
        itype = ref.ITYPE[item]

        if itype == 'boost':
            await add_exp(ctx, user, ref.BOOSTS[item])
        elif itype == 'pet':
            pass
    else:
        ctx.send('Please specify the item that you want to buy!')


@client.command()
async def pet(ctx, action, pet=None):
    user = str(ctx.message.author.id)
    action = str(action).lower()

    if not pet:
        pet = len(data.get([user, 'pets']).keys()) - 1

    if action == 'name':
        data.set([user, 'pets', pet, 'name'], )



@client.command()
async def debug(ctx, i):
    await buy_pet(ctx.message.author.id, i)


@client.command()
async def chexp(ctx, exp):
    await add_exp(ctx, str(ctx.message.author.id), int(exp))


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
