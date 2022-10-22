import requests
import time
from twocaptcha import TwoCaptcha



queueid = input("Queue ID: ")
packID = input("Pack ID: ")
cookies = input("Cookies: ")

headers = {
    'authority': 'www.nbatopshot.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.487',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.nbatopshot.com/listings/pack/{packID}?qinv=ca873fe8c241a99f9bf5975644b4bf1611c37a3627c7b2b05806cd9de7bb4be2^&queueittoken=e_basepackfeb5~q_{queueid}~ts_1612598329~ce_true~rt_afterevent~h_e3daae797d840c5b1f7965def355c60f85020ae8df70fb670ca80c90e1822faa',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': cookies,
}

response = requests.get('https://www.nbatopshot.com/api/auth0/refresh', headers=headers)
print(response.text)
xidtoken = response.json()['idToken']
print(xidtoken)
solver = TwoCaptcha('twocaptchatoken')

result = solver.recaptcha(sitekey='6LdMpd4ZAAAAAI82S4bb-R8hIdTJERTWBHz3bqas',
                          url=f'https://www.nbatopshot.com/listings/pack/{packID}', version='v2')

print(result['code'])

recaptoken = result['code']

headers = {
    'Host': 'api.nba.dapperlabs.com',
    'Connection': 'keep-alive',
    'accept': '*/*',
    'x-id-token': xidtoken,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.487',
    'content-type': 'application/json',
    'Origin': 'https://www.nbatopshot.com',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.nbatopshot.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

response = requests.post('https://api.nba.dapperlabs.com/marketplace/graphql?PurchasePack', headers=headers,
                         json={"operationName": "PurchasePack", "variables": {
                             "input": {"packListingID": packID, "price": "9",
                                       "redirectURL": "https://www.nbatopshot.com/order/packs/{{ORDER_ID}}?opening=true",
                                       "quantity": 1, "recaptchaToken": recaptoken, "queueID": queueid + "+nbats~848645aa-7f42-4235-9fda-e756dd8fdfb1"}},
                               "query": "mutation PurchasePack($input: PurchasePackInput!) {\n  purchasePack(input: $input) {\n    orderID\n    existingReservation\n    packsReserved\n    __typename\n  }\n}\n"})

orderID = response.json()['data']['purchasePack']['orderID']

success = False
while success is False:
    time.sleep(1)
    response = requests.post('https://api.nba.dapperlabs.com/marketplace/graphql?GetUserPackOrder', headers=headers,
                             json={"operationName": "GetUserPackOrder", "variables": {"input": {"orderId": orderID}},
                                   "query": "query GetUserPackOrder($input: GetUserPackOrderInput!) {\n  getUserPackOrder(input: $input) {\n    data {\n      id\n      price\n      quantity\n      status\n      state\n      dapperIntentId\n      paymentTxHash\n      packListing {\n        id\n        title\n        price\n        images {\n          url\n          __typename\n        }\n        __typename\n      }\n      packs {\n        id\n        momentIds\n        status\n        state\n        __typename\n      }\n      createdAt\n      updatedAt\n      __typename\n    }\n    __typename\n  }\n}\n"})
    if response.json()['data']['getUserPackOrder']['data']['dapperIntentId'] is not None:
        print(
            f"https://accounts.meetdapper.com/checkout/{response.json()['data']['getUserPackOrder']['data']['dapperIntentId']}")
        success = True
