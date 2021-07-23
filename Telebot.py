
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

@bot.message_handler(commands=['help'])

def help(message):
    help_str = '/score to get the score of a cricket match\n/getapple to get the stock price of apple\n/gethdfc to get the stock price of HDFC\n/getamazon to get the stock Price for Amazon\n/getapple to get the stock price of Airtel'
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






# https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2

# git init
# git add .
# git commit -m "first commit"
# heroku git:remote -a pure-lake-00698
# git push heroku master
