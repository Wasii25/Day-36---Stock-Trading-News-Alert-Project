from http import client

import requests
from dask.array import positive
from twilio.rest import Client

STOCK_NAME = "<STOCK NAME>"
COMPANY_NAME = "<COMPANY NAME>"

STOCK_ENDPOINT = "<STOCK ENDPOINT>"
NEWS_ENDPOINT = "<NEWS ENDPOINT>"
NEWS_API = "<NEWS API>"
TWILIO_SID = "<TWILIO SID>"
TWILIO_AUTH_TOKEN = "<TWILIO AUTHENTICATION TOKEN>"

STOCK_API_KEY = "<STOCK API KEY>"
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
            from_="whatsapp:+<TWILIO WHATSAPP NUMBER>",
            to="whatsapp:+<YOUR WHATSAPP NUMBER>",
        )
