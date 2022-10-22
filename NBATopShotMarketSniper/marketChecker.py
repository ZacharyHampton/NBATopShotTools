import requests
import discord
from discord.ext import commands

token = 'discordtoken'
tokendev = 'discordtoken'
bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='resistance')
async def getListingInformation(ctx, urlinfo):
    try:
        urlinfo = urlinfo[40:113]
        urlSplit = urlinfo.split('+')
        setID = urlSplit[0]
        playID = urlSplit[1]
    except:
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(name=f'Error has occured.',
                        value=f'The information you provide is malformed, try getting the url information again.',
                        inline=False)
        embed.set_footer(text="Sniveling's Bots | Made by Sniveling#3757",
                         icon_url="https://cdn.discordapp.com/avatars/168490512293036033/e8fd8710a111539ab2414710d9cc7825.png?size=128")
        await ctx.send(embed=embed)
        return

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

    theorderdict = {}

    try:
        response.json()['data']['getUserMomentListings']['data']['momentListings'][0]
    except TypeError:
        embed = discord.Embed(color=0xFF0000)
        embed.set_footer(text="Sniveling's Bots | Made by Sniveling#3757",
                         icon_url="https://cdn.discordapp.com/avatars/168490512293036033/e8fd8710a111539ab2414710d9cc7825.png?size=128")
        embed.add_field(name=f'Error has occured.',
                        value=f'The information you provide is malformed, try getting the url information again.',
                        inline=False)
        await ctx.send(embed=embed)
        return

    for x in response.json()['data']['getUserMomentListings']['data']['momentListings']:
        if x['moment']['price'] in theorderdict:
            theorderdict[x['moment']['price']] += 1
        else:
            theorderdict[x['moment']['price']] = 1

    # print(tabulate({"Price": theorderdict.keys(), "Orders": theorderdict.values()}, headers="keys", tablefmt="fancy_grid"))

    embed = discord.Embed(color=0x459ce8)
    count = 0
    for x in theorderdict.keys():
        if theorderdict[x] >= 5:
            embed.add_field(name=f'${round(float(x))}', value=f'{theorderdict[x]} sell orders', inline=False)
        else:
            count += 1

    if count == len(theorderdict.keys()):
        embed.add_field(value="This item has low resistance.", name="Resistance", inline=False)

    embed.set_footer(text="Sniveling's Bots | Made by Sniveling#3757",
                     icon_url="https://cdn.discordapp.com/avatars/168490512293036033/e8fd8710a111539ab2414710d9cc7825.png?size=128")
    await ctx.send(embed=embed)
    await ctx.send(ctx.author.mention)
    print('sent')


bot.remove_command('help')


@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(color=0x459ce8)
    embed.add_field(name=".resistance", value="Usage: .resistance [moment url]", inline=False)
    embed.set_footer(text="Sniveling's Bots | Made by Sniveling#3757",
                     icon_url="https://cdn.discordapp.com/avatars/168490512293036033/e8fd8710a111539ab2414710d9cc7825.png?size=128")
    await ctx.send(embed=embed)
    await ctx.send(ctx.author.mention)


def main():
    bot.run(token, bot=True)


if __name__ == '__main__':
    main()
