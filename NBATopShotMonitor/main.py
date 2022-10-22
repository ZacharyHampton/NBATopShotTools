import discord
import requests
import time
import sys

token = 'discordtoken'
bot = discord.Client()


def getStock():

    headers = {
        'authority': 'api.nba.dapperlabs.com',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.487',
        'content-type': 'application/json',
        'origin': 'https://www.nbatopshot.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.nbatopshot.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    data = '{"operationName":"GetPackListing","variables":{"input":{"packListingId":"62c1fd69-a1b5-412a-98d2-b73b90f73753"}},"query":"query GetPackListing($input: GetPackListingInput!) {\n  getPackListing(input: $input) {\n    data {\n      id\n      price\n      title\n      remaining\n      totalPackCount\n      description\n      expiryDate\n      forSale\n      images {\n        url\n        type\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}'

    response = requests.post('https://api.nba.dapperlabs.com/marketplace/graphql?GetPackListing', headers=headers, json={"operationName":"GetPackListing","variables":{"input":{"packListingId":"62c1fd69-a1b5-412a-98d2-b73b90f73753"}},"query":"query GetPackListing($input: GetPackListingInput!) {\n  getPackListing(input: $input) {\n    data {\n      id\n      price\n      title\n      remaining\n      totalPackCount\n      description\n      expiryDate\n      forSale\n      images {\n        url\n        type\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"})
    print(response.text)
    if response.json()['data']['getPackListing']['data']['forSale']:
        print('in stock')
        return True
    else:
        print('oos')
        return False

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    while True:
        time.sleep(1)
        isOOS = getStock()
        if isOOS:
            channel = bot.get_channel(740034579741802536)
            await channel.send("https://www.nbatopshot.com/listings/pack/62c1fd69-a1b5-412a-98d2-b73b90f73753 sniveling bot detects drop")
            sys.exit(0)
        else:
            pass




bot.run(token, bot=False)