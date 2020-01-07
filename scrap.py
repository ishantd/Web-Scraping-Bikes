import json
import pandas as pd
from pandas import DataFrame
import requests
from bs4 import BeautifulSoup

boongg_wd = requests.get(
    'https://www.boongg.com/rent/search/pune/any/any/any?start_date=1578976200000&end_date=1579062600000&timezone=Asia/Calcutta'
)
boongg_we = requests.get(
    'https://www.boongg.com/rent/search/pune/any/any/any?start_date=1579321800000&end_date=1579408200000&timezone=Asia/Calcutta'
)

wheelstreet_wd = requests.get(
    'https://www.wheelstreet.com/search/1578417852376550'
)

wheelstreet_we = requests.get(
    'https://www.wheelstreet.com/search/1578418067201136'
)

gobikes_wd = requests.get(
    'https://api.gobikes.co.in/bikes?from-date=1578976200000&to-date=1579062600000&city=5'
)

gobikes_we = requests.get(
    'https://api.gobikes.co.in/bikes?from-date=1579321800000&to-date=1579408200000&city=5'
)


def per_hour(prices):
    for x in range(0, len(prices)):
        prices[x] = prices[x].strip('.00')
        prices[x] = int(prices[x])
        prices[x] = prices[x]/24


def create_df(name, wdPrices, wePrices):
    df = pd.DataFrame(
        {
            'names': name,
            'WeekDay Prices': wdPrices,
            'Weekend Prices': wePrices
        }
    )
    return df


def names(className, result):
    bike_names = [item.find(class_=className).get_text()
                  for item in result]
    return bike_names


def prices(className, result):
    bike_prices = [item.find(class_=className).get_text()
                   for item in result]
    return bike_prices


def to_csv(df, name):
    df.to_csv(name + '.csv')


def boongg_scrap(weekday, weekend):
    wd = BeautifulSoup(weekday.content, 'html.parser')
    we = BeautifulSoup(weekend.content, 'html.parser')

    results = wd.find(class_="bike-listing-area")
    results_we = we.find(class_="bike-listing-area")

    bike_items = results.find_all(class_="bike-item")
    bike_items_we = results_we.find_all(class_="bike-item")

    # print(bike_items_we)

    bike_names = names('searchBikeName', bike_items)

    bike_prices_wd = prices('actualPrice', bike_items)
    bike_prices_we = prices('actualPrice', bike_items_we)

    per_hour(bike_prices_wd)
    per_hour(bike_prices_we)

    df = create_df(bike_names, bike_prices_wd, bike_prices_we)

    to_csv(df, "boongg")


def wheelstreet_scrap(weekday, weekend):
    wd = BeautifulSoup(weekday.content, 'html.parser')
    we = BeautifulSoup(weekend.content, 'html.parser')

    print(wd)

    results = wd.find(class_="searchPage__resultMain")
    results_we = we.find(class_="searchPage__resultMain")

    print(results)


def gobikes_scrap(weekday, weekend):
    wd = weekday.json()
    we = weekend.json()
    # getting json object for weekday
    data_wd = pd.DataFrame(wd)
    Export = data_wd.to_json(
        r'wheelstreet_wd.json')
    with open('wheelstreet_wd.json') as f:
        weekday_data = json.load(f)
    # getting json object for weekend
    data_we = pd.DataFrame(we)
    Export = data_we.to_json(
        r'wheelstreet_we.json')
    with open('wheelstreet_we.json') as f:
        weekend_data = json.load(f)

    n = len(weekend_data["data"])

    names = [None] * n

    for i in range(0, n):
        names[i] = weekend_data["data"][str(
            i)]["brand"] + " " + weekend_data["data"][str(i)]["name"]

    prices_wd = [None] * n
    prices_we = [None] * n

    for i in range(0, n):
        prices_wd[i] = weekday_data["data"][str(
            i)]["BikeHubs"][0]["bike"]["prices"][1]/24

        prices_we[i] = weekend_data["data"][str(
            i)]["BikeHubs"][0]["bike"]["prices"][1]/24

    df = create_df(names, prices_wd, prices_we)
    to_csv(df, "gobikes")


gobikes_scrap(gobikes_wd, gobikes_we)
# wheelstreet_scrap(wheelstreet_wd, wheelstreet_we)
# boongg_scrap(boongg_wd, boongg_we)
