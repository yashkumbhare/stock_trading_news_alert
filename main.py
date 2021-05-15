import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "JPM9GKC1E9PYXM0W"
NEWS_API_KEY = "b8af43d67830432d98f60a7d18a55686"
TWILIO_SID = "AC55075011c4122196239665992923d523"
TWILIO_AUTH_TOKEN = "1934335cdc89ba2d8835aacc2b53698c"
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_closing_price = data_list[0]["4. close"]
print(yesterday_closing_price)
#Get the day before yesterday's closing stock price

day_before_yesterday_closing_price = data_list[1]["4. close"]
print(day_before_yesterday_closing_price)
#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
diff = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(diff)
#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = (diff / float(yesterday_closing_price)) * 100
print(diff_percent)
#If percentage is greater than 3 then print("Get News").
if diff_percent > 3:
    print("Get News")
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#use the News API to get articles related to the COMPANY_NAME.
if diff_percent > 3:
    news_params = {
        "apiKey" : NEWS_API_KEY,
        "qInTitle" : COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)
    #Use Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]
    print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

    #Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"Headline: {article['title']}. \nBrief:{article['description']}" for article in three_articles]
#send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+16179172546",
            to="+918989772336"
        )
