from localjwt import is_jwt_valid
import requests
import os
import json
from dotenv import load_dotenv
import datetime
from pprint import pprint

load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
token = ''
token_dict = {}
market_data = {}
latest_market = datetime.datetime.now()


def get_token(tokene):
    global token
    global token_dict
    if token:
        if is_jwt_valid(token):
            print("token is valid.")
            return token
        else:
            refresh_token(token_dict['refreshToken'])
    else:
        url = 'https://auth.gbm.com/api/v1/session/user'

        payload = '{\"clientId\":\"7c464570619a417080b300076e163289\",\"user\":\""+ {USERNAME}+ "\",\"password\":\""+ {PASSWORD}+ "\"}'
        payload = {'clientId': '7c464570619a417080b300076e163289',
                   'user': USERNAME, 'password': PASSWORD}
        headers = {
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

        # response = requests.request("POST", url, headers=headers, data=json.dumps(payload, indent=2))
        r = requests.post(url, headers=headers,
                          data=json.dumps(payload, indent=2))
        token_dict = json.loads(r.content)
        print("new token")
        token = token_dict['accessToken']
        return token


def refresh_token(token_refresher):
    url = 'https://auth.gbm.com/api/v1/session/user/refresh'

    payload = '{\"clientId\":\"7c464570619a417080b300076e163289\",\"user\":\""+ {USERNAME}+ "\",\"password\":\""+ {PASSWORD}+ "\"}'
    payload = {"refreshToken": token_refresher,
               "clientId": "7c464570619a417080b300076e163289"}
    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    # response = requests.request("POST", url, headers=headers, data=json.dumps(payload, indent=2))
    r = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    token_dict = json.loads(r.content)
    print("new token")
    token = token_dict['accessToken']
    return token


def get_market(token):
    global market_data
    url = "https://homebroker-api.gbm.com/GBMP/api/Market/GetMarketPriceMonitorDetail/"

    payload = {"isOnLine": "true", "instrumentType": 0}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json', }

    r = requests.post(url, headers=headers, data=json.dumps(payload, indent=2))
    market_data = json.loads(r.content)
    return market_data


def check_market(token):
    global market_data
    global latest_market
    if market_data:
        now = datetime.datetime.now()
        if latest_market + datetime.timedelta(seconds=60) < now:
            print("new market data2")
            latest_market = datetime.datetime.now()
            return get_market(token)
        else:
            print("cached market data")
            return market_data
    else:
        latest_market = datetime.datetime.now()
        print("new market data")
        return get_market(token)


def get_symbol(stock):
    market = check_market(get_token(token))
    symbol = filter(lambda person: stock.upper() in person['symbol'], market)
    for i in symbol:
        if i:
            pprint(i)
            return i
