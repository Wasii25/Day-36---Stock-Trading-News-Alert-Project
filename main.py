from http import client

import requests
from dask.array import positive
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = "feb4df33cba749d9873d80c92b0b3b5e"
TWILIO_SID = "AC5105128009de68144e9649428a332ee6"
TWILIO_AUTH_TOKEN = "044558c04c3a55e9fe20e91e8d452f81"


STOCK_API_KEY = "5F96DOI9DXYHB8BE"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]


day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]


positive_difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if positive_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

positive_difference_percentage = round((positive_difference / float(yesterday_closing_price)) * 100)

if abs(positive_difference_percentage) > 5:
    news_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,

    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response.json()["articles"]

    three_articles = articles[:3]


    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{positive_difference_percentage}%\nHeadline: {article['title']}. \nBrief: {article ['description']} \n" for article in three_articles]
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="whatsapp:+14155238886",
            to="whatsapp:+919742418818",
        )
