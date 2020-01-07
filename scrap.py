import json
import pandas as pd
from pandas import DataFrame
import requests
from bs4 import BeautifulSoup
# from requests_html import HTMLSession
# session = HTMLSession()
from selenium import webdriver

boongg_wd = requests.get(
    'https://www.boongg.com/rent/search/pune/any/any/any?start_date=1578976200000&end_date=1579062600000&timezone=Asia/Calcutta'
)
boongg_we = requests.get(
    'https://www.boongg.com/rent/search/pune/any/any/any?start_date=1579321800000&end_date=1579408200000&timezone=Asia/Calcutta'
)

rb_wd = requests.get(
    'https://www.royalbrothers.com/search?utf8=%E2%9C%93&city_id=47&city_name=Mumbai&city=mumbai&current_service_type=bike-rentals&pickup=14+Jan%2C+2020&pickup_submit=14-01-2020&pickup_time=10%3A00+AM&dropoff=15+Jan%2C+2020&dropoff_submit=15-01-2020&dropoff_time=10%3A00+AM'
    )
rb_we = requests.get(
    'https://www.royalbrothers.com/search?utf8=%E2%9C%93&city_id=47&city_name=Mumbai&city=mumbai&current_service_type=bike-rentals&pickup=14+Jan%2C+2020&pickup_submit=14-01-2020&pickup_time=10%3A00+AM&dropoff=15+Jan%2C+2020&dropoff_submit=15-01-2020&dropoff_time=10%3A00+AM'
    )

# wsd_driver = webdriver.Firefox(
#     executable_path=r'/home/ishant/ishant_linux/geckodriver-v0.26.0-linux64/geckodriver')
# wse_driver = webdriver.Firefox(
#     executable_path=r'/home/ishant/ishant_linux/geckodriver-v0.26.0-linux64/geckodriver')

# wsd_driver.get('https://www.wheelstreet.com/search/1578417852376550')
# wse_driver.get('https://www.wheelstreet.com/search/1578418067201136')

# html_wd = wsd_driver.page_source
# html_we = wse_driver.page_source

# wheelstreet_wd = session.get('https://www.wheelstreet.com/search/1578417852376550')

# wheelstreet_we = session.get('https://www.wheelstreet.com/search/1578418067201136')
# wheelstreet_wd.html.render()
# wheelstreet_we.html.render()


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


# def wheelstreet_scrap(weekday, weekend):
#     wd = BeautifulSoup(weekday)
#     we = BeautifulSoup(weekend)

#     results_wd = wd.find(class_="searchPage__resultMain")
#     results_we = we.find(class_="searchPage__resultMain")

#     bike_items_wd = results_wd.find_all(class_='searchPage__bikeCard ng-scope')
#     bike_items_we = results_we.find_all(class_='searchPage__bikeCard ng-scope')

#     bike_names = names('searchPage__bikeCardInfoName ng-binding',bike_items_wd)

#     bike_prices_wd = prices('searchPage__bikeCardInfoPricing', bike_items_wd)
#     bike_prices_we = prices('searchPage__bikeCardInfoPricing', bike_items_we)

#     print(bike_names)
#     print(bike_items_wd)


def gobikes_scrap(weekday, weekend):
    wd = weekday.json()
    we = weekend.json()
    # getting json object for weekday
    data_wd = pd.DataFrame(wd)
    Export = data_wd.to_json(
        r'gobikes_wd.json')
    with open('gobikes_wd.json') as f:
        weekday_data = json.load(f)
    # getting json object for weekend
    data_we = pd.DataFrame(we)
    Export = data_we.to_json(
        r'gobikes_we.json')
    with open('gobikes_we.json') as f:
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

def royalbrother_scrap(weekday, weekend):
    wd = BeautifulSoup(weekday.content, 'html.parser')
    we = BeautifulSoup(weekend.content, 'html.parser')

    results_wd = wd.find(class_="col l12 m12 s12 pad0 search_container")
    results_we = we.find(class_="col l12 m12 s12 pad0 search_container")

    bike_items_wd = results_wd.find_all(class_="tarif-desc-body col m5 l3 s10 offset-s1 z-depth-1")
    bike_items_we = results_we.find_all(class_="tarif-desc-body col m5 l3 s10 offset-s1 z-depth-1")

    # print(bike_items_we)

    bike_names = names('valign-wrapper center-align bike_name', bike_items_wd)

    bike_prices_wd = [item.find(id='rental_amount').get_text()
                   for item in bike_items_wd]
    bike_prices_we = [item.find(id='rental_amount').get_text()
                   for item in bike_items_we]

    
    
    for x in range(0, len(bike_names)):
        bike_prices_wd[x] = int(bike_prices_wd[x])
        bike_prices_wd[x] = bike_prices_wd[x]/24
        bike_prices_we[x] = int(bike_prices_we[x])
        bike_prices_we[x] = bike_prices_we[x]/24
    
    

    df = create_df(bike_names, bike_prices_wd, bike_prices_we)

    to_csv(df, "royalbrothers")



royalbrother_scrap(rb_wd, rb_we)
# gobikes_scrap(gobikes_wd, gobikes_we)
# wheelstreet_scrap(html_wd, html_we)
# boongg_scrap(boongg_wd, boongg_we)
