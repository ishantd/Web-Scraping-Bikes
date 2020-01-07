import pandas as pd
import requests
from bs4 import BeautifulSoup

boongg_wd = requests.get(
    'https://www.boongg.com/rent/search/pune/any/any/any?start_date=1578976200000&end_date=1579062600000&timezone=Asia/Calcutta'
)
boongg_we = requests.get(
    'https://www.boongg.com/rent/search/pune/any/any/any?start_date=1579321800000&end_date=1579408200000&timezone=Asia/Calcutta'
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

    # print(df)
    df.to_csv('boongg.csv')


boongg_scrap(boongg_wd, boongg_we)
