import requests
import datetime
import os
from selenium import webdriver
import asyncio
import time


def getxid(sessionCookie, setID, playID):
    headers = {
        'authority': 'www.nbatopshot.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.396',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://www.nbatopshot.com/listings/p2p/{setID}+{playID}',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': f"__cfduid=d7b6cda4ef9ef74646962d6ec412b53551613591901; sid=a476cd98-897e-4b24-a04f-a501f6e41f6a; INGRESSCOOKIE=dab1893bf9ceb97bba056d5c96bfc6fd; ts:session={sessionCookie}",
    }

    response = requests.get('https://www.nbatopshot.com/api/auth0/session', headers=headers)
    return response.json()['session']['idToken']


def getFlowId(x_id_token, momentId):
    headers = {
        'Host': 'api.nba.dapperlabs.com',
        'Connection': 'keep-alive',
        'accept': '*/*',
        'x-id-token': x_id_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.396',
        'content-type': 'application/json',
        'Origin': 'https://www.nbatopshot.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.nbatopshot.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = {
        "operationName": "GetMintedMoment",
        "variables": {
            "momentId": momentId
        },
        "query": "query GetMintedMoment($momentId: ID!) {\n  getMintedMoment(momentId: $momentId) {\n    data {\n      ...MomentDetails\n      play {\n        ... on Play {\n          ...PlayDetails\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MomentDetails on MintedMoment {\n  id\n  version\n  sortID\n  set {\n    id\n    flowName\n    flowSeriesNumber\n    setVisualId\n    __typename\n  }\n  setPlay {\n    ID\n    flowRetired\n    circulationCount\n    __typename\n  }\n  assetPathPrefix\n  play {\n    id\n    stats {\n      playerID\n      playerName\n      primaryPosition\n      teamAtMomentNbaId\n      teamAtMoment\n      dateOfMoment\n      playCategory\n      __typename\n    }\n    __typename\n  }\n  price\n  listingOrderID\n  flowId\n  owner {\n    dapperID\n    username\n    profileImageUrl\n    __typename\n  }\n  flowSerialNumber\n  forSale\n  __typename\n}\n\nfragment PlayDetails on Play {\n  id\n  description\n  stats {\n    playerID\n    playerName\n    primaryPosition\n    currentTeamId\n    dateOfMoment\n    jerseyNumber\n    awayTeamName\n    awayTeamScore\n    teamAtMoment\n    homeTeamName\n    homeTeamScore\n    totalYearsExperience\n    teamAtMomentNbaId\n    height\n    weight\n    currentTeam\n    birthplace\n    birthdate\n    awayTeamNbaId\n    draftYear\n    nbaSeason\n    draftRound\n    draftSelection\n    homeTeamNbaId\n    draftTeam\n    draftTeamNbaId\n    playCategory\n    homeTeamScoresByQuarter {\n      quarterScores {\n        type\n        number\n        sequence\n        points\n        __typename\n      }\n      __typename\n    }\n    awayTeamScoresByQuarter {\n      quarterScores {\n        type\n        number\n        sequence\n        points\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  statsPlayerGameScores {\n    blocks\n    points\n    steals\n    assists\n    minutes\n    rebounds\n    turnovers\n    plusMinus\n    flagrantFouls\n    personalFouls\n    playerPosition\n    technicalFouls\n    twoPointsMade\n    blockedAttempts\n    fieldGoalsMade\n    freeThrowsMade\n    threePointsMade\n    defensiveRebounds\n    offensiveRebounds\n    pointsOffTurnovers\n    twoPointsAttempted\n    assistTurnoverRatio\n    fieldGoalsAttempted\n    freeThrowsAttempted\n    twoPointsPercentage\n    fieldGoalsPercentage\n    freeThrowsPercentage\n    threePointsAttempted\n    threePointsPercentage\n    __typename\n  }\n  statsPlayerSeasonAverageScores {\n    minutes\n    blocks\n    points\n    steals\n    assists\n    rebounds\n    turnovers\n    plusMinus\n    flagrantFouls\n    personalFouls\n    technicalFouls\n    twoPointsMade\n    blockedAttempts\n    fieldGoalsMade\n    freeThrowsMade\n    threePointsMade\n    defensiveRebounds\n    offensiveRebounds\n    pointsOffTurnovers\n    twoPointsAttempted\n    assistTurnoverRatio\n    fieldGoalsAttempted\n    freeThrowsAttempted\n    twoPointsPercentage\n    fieldGoalsPercentage\n    freeThrowsPercentage\n    threePointsAttempted\n    threePointsPercentage\n    __typename\n  }\n  __typename\n}\n"
    }

    response = requests.post('https://api.nba.dapperlabs.com/marketplace/graphql?GetMintedMoment',
                             headers=headers, json=data)

    return response.json()['data']['getMintedMoment']['data']['flowId']


def startPurchase(x_id_token, momentID, flowSerialNumber, price, sellerID):
    headers = {
        'Host': 'api.nba.dapperlabs.com',
        'Connection': 'keep-alive',
        'accept': '*/*',
        'x-id-token': x_id_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.396',
        'content-type': 'application/json',
        'Origin': 'https://www.nbatopshot.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.nbatopshot.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    momentFlowID = getFlowId(x_id_token, momentID)

    data = {
        "operationName": "PurchaseP2PMomentMutation",
        "variables": {
            "input": {
                "momentID": momentID,
                "momentFlowID": f"{momentFlowID}",
                "momentName": f"#{flowSerialNumber}",
                "momentDescription": "",
                "momentImageURL": "https://google.com/",
                "price": price,
                "sellerID": sellerID,
                "redirectURL": "https://www.nbatopshot.com/order/moment-purchase/{{ORDER_ID}}"
            }
        },
        "query": "mutation PurchaseP2PMomentMutation($input: PurchaseP2PMomentInput!) {\n  purchaseP2PMoment(input: $input) {\n    orderID\n    __typename\n  }\n}\n"
    }

    response = requests.post('https://api.nba.dapperlabs.com/marketplace/graphql?PurchaseP2PMomentMutation',
                             headers=headers, json=data)

    return response.json()['data']['purchaseP2PMoment']['orderID']


def getCheckoutLink(x_id_token, orderID):
    time.sleep(1)
    headers = {
        'Host': 'api.nba.dapperlabs.com',
        'Connection': 'keep-alive',
        'accept': '*/*',
        'x-id-token': x_id_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.396',
        'content-type': 'application/json',
        'Origin': 'https://www.nbatopshot.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.nbatopshot.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = {
        "operationName": "GetUserP2PPurchaseOrder",
        "variables": {
            "input": {
                "orderID": orderID
            }
        },
        "query": "query GetUserP2PPurchaseOrder($input: GetUserP2PPurchaseOrderInput) {\n  getUserP2PPurchaseOrder(input: $input) {\n    data {\n      id\n      state\n      purchaseIntentID\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    response = requests.post('https://api.nba.dapperlabs.com/marketplace/graphql?GetUserP2PPurchaseOrder',
                             headers=headers, json=data)
    if "purchaseIntentID" in response.text:
        if response.json()['data']['getUserP2PPurchaseOrder']['data']['purchaseIntentID'] != "":
            return response.json()['data']['getUserP2PPurchaseOrder']['data']['purchaseIntentID']

    return None


def getListingInformation(price, setID, playID, fileContent):
    headers = {
        'Host': 'api.nba.dapperlabs.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.396',
        'content-type': 'application/json',
        'Origin': 'https://www.nbatopshot.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.nbatopshot.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = {
        "operationName": "GetUserMomentListingsDedicated",
        "variables": {
            "input": {
                "setID": setID,
                "playID": playID
            }
        },
        "query": "query GetUserMomentListingsDedicated($input: GetUserMomentListingsInput!) {\n  getUserMomentListings(input: $input) {\n    data {\n      flowRetired\n      version\n      set {\n        id\n        flowName\n        flowSeriesNumber\n        __typename\n      }\n      play {\n        ... on Play {\n          ...PlayDetails\n          __typename\n        }\n        __typename\n      }\n      assetPathPrefix\n      priceRange {\n        min\n        max\n        __typename\n      }\n      momentListings {\n        id\n        moment {\n          id\n          price\n          flowSerialNumber\n          owner {\n            dapperID\n            username\n            profileImageUrl\n            __typename\n          }\n          setPlay {\n            ID\n            flowRetired\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      momentListingCount\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PlayDetails on Play {\n  id\n  description\n  stats {\n    playerID\n    playerName\n    primaryPosition\n    currentTeamId\n    dateOfMoment\n    jerseyNumber\n    awayTeamName\n    awayTeamScore\n    teamAtMoment\n    homeTeamName\n    homeTeamScore\n    totalYearsExperience\n    teamAtMomentNbaId\n    height\n    weight\n    currentTeam\n    birthplace\n    birthdate\n    awayTeamNbaId\n    draftYear\n    nbaSeason\n    draftRound\n    draftSelection\n    homeTeamNbaId\n    draftTeam\n    draftTeamNbaId\n    playCategory\n    homeTeamScoresByQuarter {\n      quarterScores {\n        type\n        number\n        sequence\n        points\n        __typename\n      }\n      __typename\n    }\n    awayTeamScoresByQuarter {\n      quarterScores {\n        type\n        number\n        sequence\n        points\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  statsPlayerGameScores {\n    blocks\n    points\n    steals\n    assists\n    minutes\n    rebounds\n    turnovers\n    plusMinus\n    flagrantFouls\n    personalFouls\n    playerPosition\n    technicalFouls\n    twoPointsMade\n    blockedAttempts\n    fieldGoalsMade\n    freeThrowsMade\n    threePointsMade\n    defensiveRebounds\n    offensiveRebounds\n    pointsOffTurnovers\n    twoPointsAttempted\n    assistTurnoverRatio\n    fieldGoalsAttempted\n    freeThrowsAttempted\n    twoPointsPercentage\n    fieldGoalsPercentage\n    freeThrowsPercentage\n    threePointsAttempted\n    threePointsPercentage\n    __typename\n  }\n  statsPlayerSeasonAverageScores {\n    minutes\n    blocks\n    points\n    steals\n    assists\n    rebounds\n    turnovers\n    plusMinus\n    flagrantFouls\n    personalFouls\n    technicalFouls\n    twoPointsMade\n    blockedAttempts\n    fieldGoalsMade\n    freeThrowsMade\n    threePointsMade\n    defensiveRebounds\n    offensiveRebounds\n    pointsOffTurnovers\n    twoPointsAttempted\n    assistTurnoverRatio\n    fieldGoalsAttempted\n    freeThrowsAttempted\n    twoPointsPercentage\n    fieldGoalsPercentage\n    freeThrowsPercentage\n    threePointsAttempted\n    threePointsPercentage\n    __typename\n  }\n  __typename\n}\n"
    }

    response = requests.post('https://api.nba.dapperlabs.com/marketplace/graphql?GetUserMomentListingsDedicated',
                             headers=headers, json=data)
    try:
        for x in response.json()['data']['getUserMomentListings']['data']['momentListings']:
            if (float(x['moment']['price']) <= price) and (str(x) not in fileContent):
                print("Found item.")
                with open("bought.txt", "a+") as writeToFile:
                    writeToFile.write(str(x) + "\n")
                return [x['moment']['id'], x['moment']['flowSerialNumber'], x['moment']['price'],
                        x['moment']['owner']['dapperID']]
    except TypeError:  # or json.decocder.JSONDecodeError
        print(response.json()['data']['getUserMomentListings']['data']['momentListings'])
        return None

    print("No underpriced items. | " + str(datetime.datetime.now()))
    return None


def getDapperAccessToken(dapperSessionCookie):
    cookies = {
        '__cfduid': 'd964e38e19722a298b68255987aab9d291613507270',
        'a0:session': dapperSessionCookie
    }

    headers = {
        'Host': 'accounts.meetdapper.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.396',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://accounts.meetdapper.com/checkout/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get('https://accounts.meetdapper.com/api/access-token', headers=headers, cookies=cookies)
    return response.json()['accessToken']


def getPurchaseReq(accessToken, orderID, option: int):
    headers = {
        'Host': 'flow-wallet-graphql-api.app.dapperlabs.com',
        'Connection': 'keep-alive',
        'accept': '*/*',
        'Authorization': accessToken,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.396',
        'content-type': 'application/json',
        'Origin': 'https://accounts.meetdapper.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://accounts.meetdapper.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = {
        "operationName": "GetPurchase",
        "variables": {
            "input": {
                "requestID": orderID
            }
        },
        "query": "query GetPurchase($input: GetPurchaseInput!) {\n  getPurchase(input: $input) {\n    ...PurchaseInfo\n    __typename\n  }\n}\n\nfragment PurchaseInfo on Purchase {\n  id\n  recipient\n  recipientMetadata {\n    username\n    __typename\n  }\n  recipientFlowAccountID\n  asset {\n    id\n    name\n    description\n    imageURL\n    __typename\n  }\n  redirectURL\n  coinbaseChargeURL\n  requireFlowAccount\n  recipientFlowAccountID\n  paymentOptions {\n    id\n    amount\n    feeAmount\n    currency\n    paymentType\n    merchantAccountAddress\n    flexiblePriceEnabled\n    __typename\n  }\n  selectedOption {\n    id\n    amount\n    currency\n    feeAmount\n    cardID\n    paymentType\n    flexiblePriceEnabled\n    __typename\n  }\n  status\n  client {\n    id\n    name\n    logoURI\n    __typename\n  }\n  processedAt\n  cardNotHonored\n  amountPaid\n  __typename\n}\n"
    }

    response = requests.post('https://flow-wallet-graphql-api.app.dapperlabs.com/graphql?GetPurchase', headers=headers,
                             json=data)
    return response.json()['data']['getPurchase']['paymentOptions'][option]['id']


def purchaseItem(accessToken, orderID, option):
    selectedOptionID = getPurchaseReq(accessToken, orderID, option)

    headers = {
        'Host': 'flow-wallet-graphql-api.app.dapperlabs.com',
        'Connection': 'keep-alive',
        'accept': '*/*',
        'Authorization': accessToken,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.396',
        'content-type': 'application/json',
        'Origin': 'https://accounts.meetdapper.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://accounts.meetdapper.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    if option == 1:  # purchase with card
        data = {
            "operationName": "ConfirmPurchase",
            "variables": {
                "input": {
                    "requestID": orderID,
                    "selectedOptionID": selectedOptionID,
                    "cardID": "carduuid"
                }
            },
            "query": "mutation ConfirmPurchase($input: ConfirmPurchaseInput!) {\n  confirmPurchase(input: $input) {\n    ...PurchaseInfo\n    __typename\n  }\n}\n\nfragment PurchaseInfo on Purchase {\n  id\n  recipient\n  recipientMetadata {\n    username\n    __typename\n  }\n  recipientFlowAccountID\n  asset {\n    id\n    name\n    description\n    imageURL\n    __typename\n  }\n  redirectURL\n  coinbaseChargeURL\n  requireFlowAccount\n  recipientFlowAccountID\n  paymentOptions {\n    id\n    amount\n    feeAmount\n    currency\n    paymentType\n    merchantAccountAddress\n    flexiblePriceEnabled\n    __typename\n  }\n  selectedOption {\n    id\n    amount\n    currency\n    feeAmount\n    cardID\n    paymentType\n    flexiblePriceEnabled\n    __typename\n  }\n  status\n  client {\n    id\n    name\n    logoURI\n    __typename\n  }\n  processedAt\n  cardNotHonored\n  amountPaid\n  __typename\n}\n"
        }
    elif option == 0:  # purchase with balance
        data = {
            "operationName": "ConfirmPurchase",
            "variables": {
                "input": {
                    "requestID": orderID,
                    "selectedOptionID": selectedOptionID,
                }
            },
            "query": "mutation ConfirmPurchase($input: ConfirmPurchaseInput!) {\n  confirmPurchase(input: $input) {\n    ...PurchaseInfo\n    __typename\n  }\n}\n\nfragment PurchaseInfo on Purchase {\n  id\n  recipient\n  recipientMetadata {\n    username\n    __typename\n  }\n  recipientFlowAccountID\n  asset {\n    id\n    name\n    description\n    imageURL\n    __typename\n  }\n  redirectURL\n  coinbaseChargeURL\n  requireFlowAccount\n  recipientFlowAccountID\n  paymentOptions {\n    id\n    amount\n    feeAmount\n    currency\n    paymentType\n    merchantAccountAddress\n    flexiblePriceEnabled\n    __typename\n  }\n  selectedOption {\n    id\n    amount\n    currency\n    feeAmount\n    cardID\n    paymentType\n    flexiblePriceEnabled\n    __typename\n  }\n  status\n  client {\n    id\n    name\n    logoURI\n    __typename\n  }\n  processedAt\n  cardNotHonored\n  amountPaid\n  __typename\n}\n"
        }

    response = requests.post('https://flow-wallet-graphql-api.app.dapperlabs.com/graphql?ConfirmPurchase',
                             headers=headers, json=data)
    try:
        return response.json()['data']['confirmPurchase']['redirectURL']
    except:
        return response.json()


async def getTopShotCookie(driver):
    driver.refresh()
    cookies_dict = {}
    for cookie in driver.get_cookies():
        cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict['ts:session']


def main():
    fileContents = open('bought.txt', "r+")
    boughtContent = fileContents.read().split('\n')

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    chromepath = BASE_DIR + r'\chromedriver.exe'
    chromepath = chromepath.replace("\\", "/")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--user-data-dir=userdatadirectory")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options, executable_path=chromepath)
    driver.get("https://www.nbatopshot.com/")

    input("Press enter to grab cookies.")

    TSCookie = asyncio.run(getTopShotCookie(driver))
    print(TSCookie)

    setID = input("Set ID: ")
    playID = input("Play ID: ")
    dapperCookie = input("Dapper Session Cookie: ")
    price = int(input("Max Price: "))
    option = 0
    gotLink = False
    counter = 0

    while True:
        a = getListingInformation(price, setID, playID, boughtContent)
        counter += 1
        if counter == 120:
            TSCookie = asyncio.run(getTopShotCookie(driver))
            counter = 0
        if a is not None:
            b = getxid(TSCookie, setID, playID)
            c = startPurchase(b, a[0], a[1], a[2], a[3])
            while gotLink is False:
                d = getCheckoutLink(b, c)
                if d is None:
                    print(f"Waiting... | {a[0]}")
                else:
                    e = getDapperAccessToken(dapperCookie)
                    f = purchaseItem(e, d, option)
                    boughtContent = fileContents.read().split('\n')
                    gotLink = False
                    a = None
                    print(f)
                    requests.post(
                        'discordwebhookurl',
                        headers={'content-type': 'application/json'},
                        json={"content": "@everyone", "embeds": [{"title": "Checkout Link", "url": f, "color": None}]})
                    break
                    # return 1


if __name__ == '__main__':
    main()
