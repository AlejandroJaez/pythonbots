import discord
import requests
import bs4
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # Running commands list to help make use of bot easier
    commands_list = ['!help', '!commands', '!ayuda']
    if any(command in message.content.lower() for command in commands_list):
        msg = 'Hola {0.author.mention}'.format(message)
        response = msg + ', el unico comando activo es !bmv "empresa".'
        await message.channel.send(response)

    # Utilizing BeautifulSoup and Requests to web scrape price data from Yahoo.
    elif message.content.startswith('!bmv'):
        # Splitting the input from !price to read input text from user.
        stock = message.content.split(' ')[1]
        url = "https://finance.yahoo.com/quote/"

        full_url = url + stock + ".mx"

        response = requests.get(full_url).content

        soup = bs4.BeautifulSoup(response, 'html.parser')

        try:
            stock_price = soup.findAll(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].text
            response = f"{stock.upper()} cotiza a ${stock_price}."
        except IndexError:
            response = f"no lo encontré, :face_with_monocle: ¿esta bien escrito?"

        await message.channel.send(response)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
