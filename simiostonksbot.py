import discord
import requests
import os
import re
import bs4
from dotenv import load_dotenv
from discord.ext import commands
from gbm import get_symbol

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

async def extract_info(ctx, soup):
    stock_price = soup.findAll(
        class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].text
    stock_name = soup.findAll(class_="D(ib) Fz(18px)")[0].text
    try:
        stock_variation = soup.findAll(
            class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")[0].text
    except:
        try:
            stock_variation = soup.findAll(
                class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)")[0].text
        except:
            stock_variation = soup.findAll(
                class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)")[0].text
    response = f"```diff\n{stock_name}\n${stock_price}\n{stock_variation}\n```"
    await ctx.send(response)


def get_search(arg):
    url = "https://finance.yahoo.com/lookup"
    full_url = url + "?s=" + arg.upper()
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(full_url, headers=HEADERS).content
    soup = bs4.BeautifulSoup(response, 'html.parser')
    return soup


def get_price(arg):
    url = "https://finance.yahoo.com/quote/"
    full_url = url + arg.upper() + ".MX"
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
    response = requests.get(full_url, headers=HEADERS).content
    soup = bs4.BeautifulSoup(response, 'html.parser')
    return soup


def get_price_mx(arg):
    url = "https://finance.yahoo.com/quote/"
    full_url = url + arg.upper()
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(full_url, headers=HEADERS).content
    soup = bs4.BeautifulSoup(response, 'html.parser')
    return soup


@bot.command(name='bmv')
async def bmv(ctx, arg):
    soup = get_price(arg)
    try:
        await extract_info(ctx, soup)
    except:
        print("searching")
        soup = get_search(arg)
        new_url = soup.find('a', attrs={'data-symbol': re.compile("\.MX$")})
        url = new_url['data-symbol']
        soup = get_price_mx(url)
        await extract_info(ctx, soup)

@bot.command(name='gbm')
async def bmv(ctx, arg):
    data = get_symbol(arg)
    sign = ""
    if data['percentageChange'] > 0:
        sign = "+"
    response = f"```diff\n{data['issueName']} - {data['issueID']}\n Ultimo precio: ${data['lastPrice']}\nCambio: {sign}{data['percentageChange']}\nVolumen de compra: {data['askVolume']} a ${data['askPrice']}\nVolumen de venta: {data['bidVolume']} a ${data['bidPrice']}\n```"
    await ctx.send(response)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)
