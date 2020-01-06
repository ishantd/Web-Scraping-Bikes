import requests
from bs4 import BeautifulSoup

page = requests.get(
    'https://www.boongg.com/rent/search/pune/any/any/any?start_date=1578976200000&end_date=1579062600000&timezone=Asia/Calcutta')
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(class_="bike-listing-area")

bike_items = results.find_all(class_="bike-item")

bike_names = [item.find(class_='searchBikeName').get_text()
              for item in bike_items]
bike_price = [soup.select('.actualPrice span')
              for item in bike_items]

print(bike_price)
