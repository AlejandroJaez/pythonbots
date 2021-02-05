import requests
import bs4
import re
import pprint

url = "https://finance.yahoo.com/quote/"
arg = "aeromexico"

full_url = url + arg
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

response = requests.get(full_url, headers=HEADERS).content

soup = bs4.BeautifulSoup(response, 'html.parser')

new_url = soup.find('a',attrs={'data-symbol' : re.compile("\.MX$")})
# <a href="/quote/CEMEXCPO.MX?p=CEMEXCPO.MX" title="CEMEX S.A.B. DE C.V." data-symbol="CEMEXCPO.MX" class="Fw(b)" data-reactid="66">CEMEXCPO.MX</a>
url = new_url['href']

response = requests.get("https://finance.yahoo.com"+url).content

soup = bs4.BeautifulSoup(response, 'html.parser')

stock_price = soup.findAll(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].text
stock_name = soup.findAll(class_="D(ib) Fz(18px)")[0].text
response = f"{stock_name} cotiza a ${stock_price}."
print(new_url)

pprint.pprint(response)