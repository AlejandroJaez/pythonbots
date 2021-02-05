import discord
import requests
import os
import bs4
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='bmv')
async def bmv(ctx, arg):

    url = "https://finance.yahoo.com/quote/"

    full_url = url + arg + ".mx"

    response = requests.get(full_url).content

    soup = bs4.BeautifulSoup(response, 'html.parser')

    try:
        stock_price = soup.findAll(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].text
        response = f"{arg.upper()} cotiza a ${stock_price}."
    except IndexError:
        response = f"no lo encontré, :face_with_monocle: ¿esta bien escrito?"
    await ctx.send(response)



@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)