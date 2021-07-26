
import os
import telebot
from bs4 import BeautifulSoup
import requests
from flask import Flask,request
from googlesearch import search

API_KEY = 'API KEY'
bot = telebot.TeleBot(API_KEY)
server = Flask(__name__)


@bot.message_handler(commands=['Greet'])
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

@bot.message_handler(commands=['score'])
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

def searching(pm,team,time,format,sort):
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

@bot.message_handler(commands='diceroll')
def dice_roll_times(message):
    sent_msg = bot.send_message(message.chat.id, 'How many times do you want to roll the dice?')
    bot.register_next_step_handler(sent_msg, dice_roll)

def dice_roll(message):
    rolls = str(message.text)    
    coin = [1,2,3,4,5,6]
    answers = []
    rolls = int(rolls)
    for i in range(1,rolls + 1):
        choice = random.choice(coin)
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
    # playerchoice = playerchoice.lower()
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
    # global ans
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

def rps(message):
    playerchoice = message.text
    playerchoice = playerchoice.lower()
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


@bot.message_handler(commands=['weather'])
def weather_start(message):
    sent_msg = bot.send_message(message.chat.id, 'What place do you want the weather of?')
    bot.register_next_step_handler(sent_msg, weather)

def weather(message):
    city = message.text
    url = "https://www.google.com/search?q="+"weather"+city
    html = requests.get(url).content
 
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    bot.send_message(message.chat.id, f'Weather of {city} is {temp}')

@bot.message_handler(commands=['streamingsite'])

def streamingsite_start(message):
    sent_msg = bot.send_message(message.chat.id, 'Do you want information for a movie or tv show?')
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
    if len(sites) == 0:
        bot.send_message(message.chat.id, f'{show} is not available anywhere!')


    sites = ', '.join(sites)
    show = ' '.join(show)

    bot.send_message(message.chat.id, f'{show} is available on {sites}!')
        
def streamingsite_movie_name(message):
    sent_msg = bot.send_message(message.chat.id, 'What Movie?')
    bot.register_next_step_handler(sent_msg, streamingsite_tvshow)

def streamingsite_movie(message): 
    movie_orignal= message.text

    movie_orignal = [x.strip() for x in movie_orignal.split(' ')]
    movie = '-'.join(movie_orignal)

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
    
    if len(sites) == 0:
        bot.send_message(message.chat.id, f'{movie_orignal} is not available anywhere!')

    else:
        sites = ', '.join(sites)
        movie_orignal = ' '.join(movie_orignal)

        bot.send_message(message.chat.id, f'{movie_orignal} is available on {sites}!')


@bot.message_handler(commands=['help'])
def help(message):
    help_str = '/score to get the score of a cricket match\n/getapple to get the stock price of apple\n/gethdfc to get the stock price of HDFC\n/getamazon to get the stock Price for Amazon\n/getapple to get the stock price of Airtel\n/passwordgenerator to generate a 16 letter Alphanumeric Password\n/countvowels to count vowels in a sentence\n/diceroll to roll an x number of dice\n/rockpaperscissor to play Rock, Paper and Scissor\n/calculator to use the calculator\n/weather to get weather of any city\n/streamingsite to get information of where is a movie or show available!'
    bot.send_message(message.chat.id, help_str)

@server.route('/' + API_KEY, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200
@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='https://pure-lake-00698.herokuapp.com/' + API_KEY)
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

bot.polling()
