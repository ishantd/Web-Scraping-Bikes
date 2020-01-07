import pandas as pd
import requests
from bs4 import BeautifulSoup

page = requests.get(
    'https://www.boongg.com/rent/search/pune/any/any/any?start_date=1578976200000&end_date=1579062600000&timezone=Asia/Calcutta')
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(class_="bike-listing-area")

bike_items = results.find_all(class_="bike-item")

bike_names = [item.find(class_='searchBikeName').get_text()
              for item in bike_items]

bike_prices = [item.find(class_='actualPrice').get_text()
               for item in bike_items]

for x in range(0, len(bike_prices)):
    bike_prices[x] = bike_prices[x].strip('.00')
    bike_prices[x] = int(bike_prices[x])
    bike_prices[x] = bike_prices[x]/24

bike_stuff = pd.DataFrame(
    {'names': bike_names,
     'prices': bike_prices, }
)
bike_stuff.to_csv('bike.csv')
# print(bike_stuff)
