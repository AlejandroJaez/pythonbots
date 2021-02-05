import discord
import requests
import os
import re
import bs4
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='bmv')
async def bmv(ctx, arg):

    url = "https://finance.yahoo.com/lookup"

    full_url = url + "?s=" + arg.upper()
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }

    response = requests.get(full_url, headers=HEADERS).content

    soup = bs4.BeautifulSoup(response, 'html.parser')

    # response = f"no lo encontré, :face_with_monocle: ¿esta bien escrito?"
    new_url = soup.find('a',attrs={'data-symbol' : re.compile("\.MX$")})
# <a href="/quote/CEMEXCPO.MX?p=CEMEXCPO.MX" title="CEMEX S.A.B. DE C.V." data-symbol="CEMEXCPO.MX" class="Fw(b)" data-reactid="66">CEMEXCPO.MX</a>
    url = new_url['href']

    response = requests.get("https://finance.yahoo.com"+url).content

    soup = bs4.BeautifulSoup(response, 'html.parser')

    stock_price = soup.findAll(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].text
    stock_name = soup.findAll(class_="D(ib) Fz(18px)")[0].text
    try:
        stock_variation = soup.findAll(class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")[0].text
    except:
        stock_variation = soup.findAll(class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)")[0].text
    response = f"```diff\n{stock_name}\n${stock_price}\n{stock_variation}\n```"
    await ctx.send(response)



@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)