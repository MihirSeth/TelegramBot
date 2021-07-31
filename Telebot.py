
import os
import telebot
from bs4 import BeautifulSoup
import requests
from flask import Flask,request
from googlesearch import search
from gnewsclient import gnewsclient
import smtplib


API_KEY = 'API KEY'
bot = telebot.TeleBot(API_KEY)
server = Flask(__name__)


@bot.message_handler(commands=['greet'])
def greet(message):
  bot.reply_to(message, "Hey! Hows it going?")

@bot.message_handler(commands=['getapple'])
def getapple(message):
  res = requests.get('https://www.marketwatch.com/investing/stock/aapl')
  score = BeautifulSoup(res.text, 'html.parser')
  score1 = score.find('div', class_= "intraday__data")
  textFind = score1.getText()
  textFind = '$' + textFind[4:12]  
  bot.send_message(message.chat.id, textFind)

@bot.message_handler(commands=['cricketscore'])
def score(message):
    sent = bot.send_message(message.chat.id, 'What two teams Cricket Match do you want the score of?')
    bot.register_next_step_handler(sent, series_or_math)

def series_or_math(pm):
    team = pm.text
    sent_msg = bot.send_message(pm.chat.id, f"You want the score of {team}. Do you want information about an Specific Series or an Match?")
    bot.register_next_step_handler(sent_msg,sorter,team)

def sorter(pm,team):
    sort = pm.text
    if sort == 'Match' or sort == 'match':
        sent_msg = bot.send_message(pm.chat.id, f"Proceeding...reply with any number or letter!!!")
        bot.register_next_step_handler(sent_msg,teams_handler,team,sort)
    elif sort == 'Series' or sort == 'series':
        sent_msg = bot.send_message(pm.chat.id, f"Proceeding...reply with any number or letter!!!")
        bot.register_next_step_handler(sent_msg,teams_handler_series,team,sort)

def teams_handler_series(pm,team,sort):
    sent_msg = bot.send_message(pm.chat.id, f"You want the score of {team} and an {sort}. What format?")
    bot.register_next_step_handler(sent_msg, format_handler_series,team,sort) 
  
def format_handler_series(pm,team,sort):
    format = pm.text
    sent_msg = bot.send_message(pm.chat.id, f"You want the score of an {format} between {team} and an {sort}. What Year is the Match From?")
    bot.register_next_step_handler(sent_msg, time_handler_series,team,format,sort) 

def time_handler_series(pm,team,format,sort):
    time = pm.text
    sent_msg = bot.send_message(pm.chat.id, f"You want the score of an {format} (an {sort}) between {team} and in {time}")
    bot.register_next_step_handler(sent_msg, searching_series,team,time,format,sort) 

def searching_series(pm,team,time,format,sort):
    team = team.split()
    match = team[0] + ' vs ' + team[2] + ' ' + format + ' ' + sort +  time 
    bot.send_message(pm.chat.id, match)
    query = match + ' Cricbuzz'
    for j in search(query, tld="co.in", num=1, stop=1, pause=1):
        bot.send_message(pm.chat.id, j)

def teams_handler(pm,team,sort):
    sent_msg = bot.send_message(pm.chat.id, f"You want the score of {team} and an {sort}. What format?")
    bot.register_next_step_handler(sent_msg, format_handler,team,sort) 
  
def format_handler(pm,team,sort):
    format = pm.text
    sent_msg = bot.send_message(pm.chat.id, f"You want the score of an {format} between {team} and an {sort}. What Year is the Match From?")
    bot.register_next_step_handler(sent_msg, time_handler,team,format,sort) 

def time_handler(pm,team,format,sort):
    time = pm.text
    sent_msg = bot.send_message(pm.chat.id, f"You want the score of an {format} (an {sort}between {team} and in {time}. What Match Number?")
    bot.register_next_step_handler(sent_msg, searching,team,time,format) 

def searching(pm,team,time,format):
    match_num = pm.text
    team = team.split()
    match = team[0] + ' vs ' + team[2] + ' ' + format + ' ' + match_num + ' match ' +  time 
    bot.send_message(pm.chat.id, match)
    query = match + ' Cricbuzz'
    for j in search(query, tld="co.in", num=1, stop=1, pause=1):
        bot.send_message(pm.chat.id, j)

@bot.message_handler(commands=['getamazon'])
def getamazon(message):
    res = requests.get('https://www.marketwatch.com/investing/stock/amzn')
    score = BeautifulSoup(res.text, 'html.parser')
    score1 = score.find('div', class_= "intraday__data")
    textFindAmazon = score1.getText()
    textFindAmazon = "$" + textFindAmazon[4:12]
    bot.send_message(message.chat.id, textFindAmazon)

@bot.message_handler(commands=['getairtel'])
def getairtel(message):
    res = requests.get('https://www.marketwatch.com/investing/stock/532454?countrycode=in')
    score = BeautifulSoup(res.text, 'html.parser')
    score1 = score.find('div', class_= "intraday__data")
    textFindAirtel = score1.getText()
    textFindAirtel = "₹" + textFindAirtel[4:12]
    bot.send_message(message.chat.id, textFindAirtel)

@bot.message_handler(commands=['gethdfc'])
def gethdfc(message):
    res = requests.get('https://www.marketwatch.com/investing/stock/500180?countrycode=in')
    score = BeautifulSoup(res.text, 'html.parser')
    score1 = score.find('div', class_= "intraday__data")
    textFindHDFC = score1.getText()
    textFindHDFC = "₹" + textFindHDFC[4:12]
    bot.send_message(message.chat.id, textFindHDFC)

@bot.message_handler(commands=['diceroll'])
def dice_roll_times(message):
    sent_msg = bot.send_message(message.chat.id, 'How many times do you want to roll the dice?')
    bot.register_next_step_handler(sent_msg, dice_roll)

def dice_roll(message):
    rolls = message.text
    dice = [1,2,3,4,5,6]
    answers = []
    rolls = int(rolls)
    for i in range(1,rolls + 1):
        choice = random.choice(dice)
        choice = str(choice)
        answers.append(choice)
    joined = ', '.join(answers)
    bot.send_message(message.chat.id, joined)

@bot.message_handler(commands=['passwordgenerator'])
def password_generator(message):
    chars = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
           '*', '(', ')', '<']
    char_str = random.choice(chars)
    word = random.choices(string.ascii_lowercase + string.digits+ string.ascii_uppercase , k = 16)
    nums = []
    for i in range(1,17):
        nums.append(i)
    index = random.choice(nums)
    word.insert(index,char_str)
    word = ''.join(word)
    bot.send_message(message.chat.id, word)

@bot.message_handler(commands=['coinflip'])
def dice_roll_times(message):
    sent_msg = bot.send_message(message.chat.id, 'How many times do you want to flip the coin?')
    bot.register_next_step_handler(sent_msg, coin_flip)

def coin_flip(message):
    flips = message.text
    flips = str(flips)  
    coin = ['Heads','Tails']
    answers = []
    rolls = int(flips)
    for i in range(1,flips + 1):
        choice = random.choice(coin)
        answers.append(choice)
    countHeads = answers.count('Heads')
    countTails = answers.count('Tails')
    bot.send_message(message.chat.id, '\nHeads is: ' + str(countHeads) +  '\nTails is: ' + str(countTails))

@bot.message_handler(commands=['countvowels'])
def count_vowels_input(message):
    sent_msg = bot.send_message(message.chat.id, 'Type a sentence to count the vowels in: ')
    bot.register_next_step_handler(sent_msg, count_vowels)

def count_vowels(message):
    sentence = message.text
    sentence = sentence.lower()
    vowels = ['a','e','i', 'o', 'u']
    count = 0
    for i in sentence:
        if i in vowels:
            count += 1
    bot.send_message(message.chat.id, f'Number of vowels in the sentence are {count}')

@bot.message_handler(commands=['rockpaperscissor'])
def rps_input(message):
    sent_msg = bot.send_message(message.chat.id, 'Choose one between Rock, Paper and Scissor ')
    bot.register_next_step_handler(sent_msg, rps)

def rps(message):
    playerchoice = message.text
    computerchoice = random.choice(['Rock','Paper','Scissor'])
    bot.send_message(message.chat.id, 'My choice is ' + computerchoice)
    if playerchoice == computerchoice:
        bot.send_message(message.chat.id,"It is a Tie! You both chose " + playerchoice)
    elif playerchoice == "Scissor":
        if computerchoice == "Rock":
            bot.send_message(message.chat.id,'You lose!')
        else:
            bot.send_message(message.chat.id,"You win!")
    elif playerchoice == "Paper":
        if computerchoice == "Scissor":
            bot.send_message(message.chat.id,'You lose!')
        else:
            bot.send_message(message.chat.id,"You win!")
    elif playerchoice == "Rock":
        if computerchoice == "Paper":
            bot.send_message(message.chat.id,'You lose!')
        else:
            bot.send_message(message.chat.id,"You win!")

@bot.message_handler(commands=['calculator'])
def calc_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What do you want to do- Add, Subtract, Multiply or Divide?')
    bot.register_next_step_handler(sent_msg, rps)

def calc_sorter(message):
    sort = message.text
    if sort == 'Add' or sort == 'add':
            sent_msg = bot.send_message(message.chat.id, 'What is the first number you want to add?')
            bot.register_next_step_handler(sent_msg, add)

    elif sort == 'Subtract' or sort == 'subtract':
            sent_msg = bot.send_message(message.chat.id, 'What is the first number you want to subtract?')
            bot.register_next_step_handler(sent_msg, subtract)
    elif sort == 'Multiply' or sort == 'multiply':
            sent_msg = bot.send_message(message.chat.id, 'What is the first number you want to multiply?')
            bot.register_next_step_handler(sent_msg, multipication)
    elif sort == 'Divide' or sort == 'divide':
            sent_msg = bot.send_message(message.chat.id, 'What is the first number you want to divide?')
            bot.register_next_step_handler(sent_msg, division)

def add(message):
    num1 = message.text
    num1 = int(num1)
    sent_msg = bot.send_message(message.chat.id, 'What is the second number you want to add?')
    bot.register_next_step_handler(sent_msg, add_total,num1)

def add_total(message,num1):
    num2 = message.text
    total = num2 + num1
    bot.send_message(message.chat.id, f'Total is {total}')

def subtract(message):
    num1 = message.text
    num1 = int(num1)
    sent_msg = bot.send_message(message.chat.id, 'What is the second number?')
    bot.register_next_step_handler(sent_msg, subtract_total,num1)

def subtract_total(message,num1):
    num2 = message.text
    ans = num2-num1
    bot.send_message(message.chat.id, f'Answer is {ans}')

def multipication(message):
    num1 = message.text
    num1 = int(num1)
    sent_msg = bot.send_message(message.chat.id, 'What is the second number?')
    bot.register_next_step_handler(sent_msg, multiply_ans,num1)

def multiply_ans(message,num1):
    num2 = message.text
    product = num2*num1
    bot.send_message(message.chat.id, f'Product is {product}')

def division(message):
    num1 = message.text
    num1 = int(num1)
    sent_msg = bot.send_message(message.chat.id, 'What is the second number?')
    bot.register_next_step_handler(sent_msg, multiply_ans,num1)
def multiply_ans(message,num1):
    num2 = message.text
    quotient = num1/num2
    bot.send_message(message.chat.id, f'Quotient is {quotient}')

@bot.message_handler(commands=['weather'])
def weather_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What place do you want the weather of?')
    bot.register_next_step_handler(sent_msg, weather)

def weather(message):
    city = message.text
    url = "https://www.google.in/search?q="+"weather"+city
    html = requests.get(url).content
 
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    bot.send_message(message.chat.id, f'Weather of {city} is {temp}')

@bot.message_handler(commands=['streamingsite'])
def streamingsite_start(message):
    sent_msg = bot.send_message(message.chat.id, 'Do you want information for a Movie or TV Show?')
    bot.register_next_step_handler(sent_msg, streamingsite_sorter)

def streamingsite_sorter(message):
    sort = message.text
    if sort == 'show' or sort == 'Show' or sort == 'TV Show' or sort == 'tv show' or sort == 'Tv show':
        sort = 'tv-show'
        sent_msg = bot.send_message(message.chat.id, f"Proceeding...reply with any number or letter!!!")
        bot.register_next_step_handler(sent_msg,streamingsite_tvshow_name)
    
    elif sort == 'Movie' or sort == 'movie':
        sort == 'movie'
        sent_msg = bot.send_message(message.chat.id, f"Proceeding...reply with any number or letter!!!")
        bot.register_next_step_handler(sent_msg,streamingsite_movie_name)

def streamingsite_tvshow_name(message):
    sent_msg = bot.send_message(message.chat.id, 'What TV show?')
    bot.register_next_step_handler(sent_msg, streamingsite_tvshow)

def streamingsite_tvshow(message): 
    show = message.text
    show = [x.strip() for x in show.split(' ')]
    tv_show = ('-').join(show)
    url = 'https://www.justwatch.com/in/tv-show/' + tv_show
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for link in soup.find_all('img'):
        try:
            title = link['alt']
            links.append(title)
        except KeyError:
            pass

    sites = []
    streaming_sites = ['Netflix','Amazon Prime Video','Hotstar','Sony Liv','Zee5']
    for i in links:
        if i in streaming_sites:
            sites.append(i)
    show = ' '.join(show)
    if len(sites) == 0:
        bot.send_message(message.chat.id, f'{show} is not available anywhere! Make sure what you want is a TV Show, also make sure the spelling is correct.')
    else:
        sites = ', '.join(sites)
        # getName = soup.find('div', class_= "title-block")
        # for i in getName:
        #     name = i.h1.text
        #     name = name[1:]
        bot.send_message(message.chat.id, f'{show} is available on {sites}!')
            
def streamingsite_movie_name(message):
    sent_msg = bot.send_message(message.chat.id, 'What Movie?')
    bot.register_next_step_handler(sent_msg, streamingsite_movie)

def streamingsite_movie(message): 
    movie_original= message.text
    movie_original = [x.strip() for x in movie_original.split(' ')]
    movie = '-'.join(movie_original)
    url = 'https://www.justwatch.com/in/movie/' + movie
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for link in soup.find_all('img'):
        try:
            title = link['alt']
            links.append(title)
        except KeyError:
            pass

    sites = []
    streaming_sites = ['Netflix','Amazon Prime Video','Hotstar','Sony Liv','Zee5']
    for i in links:
        if i in streaming_sites:
            sites.append(i)
    movie_original = ' '.join(movie_original)
    if len(sites) == 0:
        bot.send_message(message.chat.id, f'{movie_original} is not available anywhere! Make sure what you want is a Movie, also make sure the spelling is correct.')
    else:
        sites = ', '.join(sites)
        bot.send_message(message.chat.id, f'{movie_original} is available on {sites}!')

@bot.message_handler(commands=['stock'])
def stock_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What stock price do you want?')
    bot.register_next_step_handler(sent_msg, stock_get)

def stock_get(message):
    stock = message.text
    url = "https://www.google.in/search?q="+stock+"+stock+price"
    html = requests.get(url).content
 
    soup = BeautifulSoup(html, 'html.parser')
    stock_price = soup.find('div',class_="BNeawe iBp4i AP7Wnd")
    stock_price1 = soup.find('div',class_="BNeawe uEec3 AP7Wnd")
    stock_price = stock_price.getText()
    stock_price = stock_price.split()[0]

    stock_price_currency = stock_price1.getText()
    stock_price_currency = stock_price_currency.split()[8]
    bot.send_message(message.chat.id, f'Stock of {stock} is {stock_price} {stock_price_currency}')

@bot.message_handler(commands=['inrtodollar'])
def converter_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What is amount in inr?')
    bot.register_next_step_handler(sent_msg, converter_get1)

def converter_get1(message):
    inr = message.text
    res = requests.get('https://www.goodreturns.in/currency/united-states-dollar-usd-to-indian-rupee-inr-converter.html')
    dollarQuery = BeautifulSoup(res.text, 'html.parser')
    queryDollar = dollarQuery.find('div', class_= "currency-rates")
    dollarPriceQuery = queryDollar.getText()
    dollarPriceParsed = dollarPriceQuery[13:20]
    inr = float(inr)
    inr_to_dollar_rounded = inr/float(dollarPriceParsed)
    inr_to_dollar = round(inr_to_dollar_rounded, 2)
    inr_to_dollar = '$' + str(inr_to_dollar)
    bot.send_message(message.chat.id, 'Price in dollars is ' + inr_to_dollar)

@bot.message_handler(commands=['dollartoinr'])
def converter_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What is amount in dollar?')
    bot.register_next_step_handler(sent_msg, converter_get2)

def converter_get2(message):
    dollar = message.text
    res = requests.get('https://www.goodreturns.in/currency/united-states-dollar-usd-to-indian-rupee-inr-converter.html')
    dollarQuery = BeautifulSoup(res.text, 'html.parser')
    queryDollar = dollarQuery.find('div', class_= "currency-rates")
    dollarPriceQuery = queryDollar.getText()
    dollarPriceParsed = dollarPriceQuery[13:20]
    dollar = float(dollar)
    dollar_to_inr_rounded = float(dollarPriceParsed) * dollar
    dollar_to_inr = round(dollar_to_inr_rounded, 2)
    dollar_to_inr = '₹' + str(dollar_to_inr)
    bot.send_message(message.chat.id, 'Price in inr is ' + dollar_to_inr)

@bot.message_handler(commands=['inrtopound'])
def converter_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What is amount in inr?')
    bot.register_next_step_handler(sent_msg, converter_get3)

def converter_get3(message):
    inr = message.text
    res = requests.get('https://www.goodreturns.in/currency/british-pound-sterling-gbp-to-indian-rupee-inr-converter.html')
    poundQuery = BeautifulSoup(res.text, 'html.parser')
    queryPound = poundQuery.find('div', class_= "moneyweb-floatleft")
    poundPriceQuery = queryPound.getText()
    poundPriceParsed = poundPriceQuery[14:20]
    inr = float(inr)
    inr_to_pound_rounded = inr/float(poundPriceParsed)
    inr_to_pound = round(inr_to_pound_rounded, 2)
    inr_to_pound = '£' + str(inr_to_pound)
    bot.send_message(message.chat.id, 'Price in pound is ' + inr_to_pound)

@bot.message_handler(commands=['poundtoinr'])
def converter_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What is amount in pound?')
    bot.register_next_step_handler(sent_msg, converter_get4)

def converter_get4(message):
    pound = message.text
    res = requests.get('https://www.goodreturns.in/currency/british-pound-sterling-gbp-to-indian-rupee-inr-converter.html')
    poundQuery = BeautifulSoup(res.text, 'html.parser')
    queryPound = poundQuery.find('div', class_= "moneyweb-floatleft")
    poundPriceQuery = queryPound.getText()
    poundPriceParsed = poundPriceQuery[14:20]
    pound = float(pound)
    pound_to_inr_rounded = float(poundPriceParsed) * pound
    pound_to_inr = round(pound_to_inr_rounded, 2)
    pound_to_inr = '₹' + str(pound_to_inr)
    bot.send_message(message.chat.id, 'Price in inr is ' + pound_to_inr)

@bot.message_handler(commands=['inrtoeuro'])
def converter_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What is amount in inr?')
    bot.register_next_step_handler(sent_msg, converter_get5)

def converter_get5(message):
    inr = message.text
    res = requests.get('https://www.goodreturns.in/currency/euro-eur-to-indian-rupee-inr-converter.html')
    euroQuery = BeautifulSoup(res.text, 'html.parser')
    queryEuro= euroQuery.find('div', class_= "moneyweb-floatleft")
    queryEuro = queryEuro.getText()
    euroPriceParsed = queryEuro[14:20]
    inr = float(inr)
    inr_to_euro_rounded = inr/float(euroPriceParsed)
    inr_to_euro = round(inr_to_euro_rounded, 2)
    inr_to_euro = '€' + str(inr_to_euro)
    bot.send_message(message.chat.id, 'Price in euro is ' + inr_to_euro)

@bot.message_handler(commands=['eurotoinr'])
def converter_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What is amount in euro?')
    bot.register_next_step_handler(sent_msg, converter_get6)

def converter_get6(message):
    euro = message.text
    res = requests.get('https://www.goodreturns.in/currency/euro-eur-to-indian-rupee-inr-converter.html')
    euroQuery = BeautifulSoup(res.text, 'html.parser')
    queryEuro= euroQuery.find('div', class_= "moneyweb-floatleft")
    queryEuro = queryEuro.getText()
    euroPriceParsed = queryEuro[14:20]
    euro = float(euro)
    euro_to_inr_rounded = float(euroPriceParsed) * euro
    euro_to_inr = round(euro_to_inr_rounded, 2)
    euro_to_inr = '₹' + str(euro_to_inr )
    bot.send_message(message.chat.id, 'Price in inr is ' + euro_to_inr)


@bot.message_handler(commands=['news'])
def news_starter(message):
    sent_msg = bot.send_message(message.chat.id, 'What is the topic you want the news for? The options are World, Nation, Buisness, Technology, Entertainment, Sports, Science, Health!')
    bot.register_next_step_handler(sent_msg,news)
def news(message):
    topic = message.text
    client = gnewsclient.NewsClient(language='english', location='india', topic=topic, max_results=5)
    news_list = client.get_news()
    title1 = "Title: " +news_list[0]['title']
    title1=str(title1)
    link1 = "Link: " +  news_list[0]['link']
    link1 = str(link1)
    title2= "Title: " + news_list[1]['title']
    title2=str(title2)
    link2 = "Link: " + news_list[1]['link']
    link2 = str(link2)
    title3 = "Title: "+  news_list[2]['title']
    title3=str(title3)
    link3 = "Link: " + news_list[2]['link']
    link3 = str(link3)
    ans = f"\nNews 1 is {title1}. The News is at {link1}\n\nNews 2 is {title2}. The News is at {link2}\n\nNews 3 is {title3}. The News is at {link3}".encode('utf-8')
    bot.send_message(message.chat.id, ans)

@bot.message_handler(commands=['newsmail'])
def news_mail_starter(message):
    sent_msg = bot.send_message(message.chat.id, 'What is the topic you want the news for? The options are World, Nation, Buisness, Technology, Entertainment, Sports, Science, Health!')
    bot.register_next_step_handler(sent_msg,news_topic)

def news_topic(message):
    topic = message.text
    client = gnewsclient.NewsClient(language='english', location='india', topic=topic, max_results=5)
    news_list = client.get_news()
    title1 = "Title: " +news_list[0]['title']
    title1=str(title1)
    link1 = "Link: " +  news_list[0]['link']
    link1 = str(link1)
    title2= "Title: " + news_list[1]['title']
    title2=str(title2)
    link2 = "Link: " + news_list[1]['link']
    link2 = str(link2)
    title3 = "Title: "+  news_list[2]['title']
    title3=str(title3)
    link3 = "Link: " + news_list[2]['link']
    link3 = str(link3)
    ans = f"\nNews 1 is {title1}. The News is at {link1}\n\nNews 2 is {title2}. The News is at {link2}\n\nNews 3 is {title3}. The News is at {link3}".encode('utf-8')    
    sent_msg = bot.send_message(message.chat.id, 'What is your email id?')
    bot.register_next_step_handler(sent_msg, news_mail, ans)


def news_mail(message,ans):
    email = message.text
    bot.send_message(message.chat.id, email)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("email-id", "password")
    # message to be sent
    # message = ans
    # sending the mail
    s.sendmail("email-id", email, ans)
    # terminating the session
    s.quit()
    bot.send_message(message.chat.id, 'Mail sent!!!')

@bot.message_handler(commands=['help'])
def help(message):
    # \n/getapple to get the stock price of apple\n/gethdfc to get the stock price of HDFC\n/getamazon to get the stock Price for Amazon\n/getapple to get the stock price of Airtel
    help_str = '/cricketscore to get the score of a cricket match\n/passwordgenerator to generate a 16 letter Alphanumeric Password\n/countvowels to count vowels in a sentence\n/diceroll to roll an x number of dice\n/rockpaperscissor to play Rock, Paper and Scissor\n/calculator to use the calculator\n/weather to get weather of any city\n/streamingsite to get information of where is a movie or show available!\n/stock to get stock price of a stock!\n/inrtodollar to convert inr to dollar\n/dollartoinr to convert dollar to inr\n/inrtopound to convert inr to pound\n/poundtoinr to convert pound to inr\n/inrtoeuro to convert inr to euro\n/eurotoinr to euro pound to inr\n/news to get news\n/newsmail to get mailed news'
    bot.send_message(message.chat.id, help_str)
    

@server.route('/' + API_KEY, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200
@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='HEROKU_APP' + API_KEY)
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

bot.polling()
