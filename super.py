import time
import telebot;
from telebot import types
import requests
import schedule
bot = telebot.TeleBot('1659868824:AAFJuytsqCoIkj9Jib0JneJFHuohFcZ-3oA');
regions = ["ua","it","ru","fr","us"]
qqq = [
   {
      "region":"ua",
      "confirmed":2216654,
      "recovered":2101722,
      "deaths":51333
   },
   {
      "region":"it",
      "confirmed":12134286,
      "recovered":3918657,
      "deaths":754169
   },
   {
      "region":"ru",
      "confirmed":10633869,
      "recovered":8810973,
      "deaths":195255
   },
   {
      "region":"fr",
      "confirmed":5917397,
      "recovered":5425261,
      "deaths":110062
   },
   {
      "region":"us",
      "confirmed":34227306,
      "recovered":28177659,
      "deaths":612702
   }
]
table = []
def infoall() :
    for region in regions:
        time.sleep(2)
        url = "https://covid-19-data.p.rapidapi.com/country/code"
        querystring = {"code":region}
        headers = {
                'x-rapidapi-key': "3465f74c86msh86c8c25da433fa1p1664bdjsn77dfe841a474",
                'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
                }
        response = requests.request("GET", url, headers=headers, params=querystring)
        pass_times = response.json()
        table_details = {"region": None, "confirmed": None, "recovered": None, "deaths": None}
        for i in pass_times:
            table_details['region'] = region
            table_details['confirmed'] = i['confirmed']
            table_details['recovered'] = i['recovered']
            table_details['deaths'] = i['deaths']
            table.append(table_details)
infoall()
print(qqq)
def test():
    for i in qqq:
        print("aaa",i['region'])
# test()
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "хочу узнать данные":
        bot.send_message(message.from_user.id, "Держи: ")
        keyboard = types.InlineKeyboardMarkup();
        key_ua = types.InlineKeyboardButton(text='Украина', callback_data='ua');
        keyboard.add(key_ua);
        key_fr = types.InlineKeyboardButton(text='Франция', callback_data='fr');
        keyboard.add(key_fr);
        key_ru = types.InlineKeyboardButton(text='Россия', callback_data='ru');
        keyboard.add(key_ru);
        key_it = types.InlineKeyboardButton(text='Италия', callback_data='it');
        keyboard.add(key_it);
        key_us = types.InlineKeyboardButton(text='США', callback_data='us');
        keyboard.add(key_us);
        question = 'Какая страна тебя интересует?';
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши 'привет'")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    for i in qqq:
        if i['region'] == call.data:
            bot.send_message(call.message.chat.id, f' {i["region"]} => Заболело: {i["confirmed"]},выздоровело: {i["recovered"]},умерло: {i["deaths"]}  ')
bot.polling(none_stop=True, interval=0)
schedule.every().day.at("10:00").do(infoall)
while True:
    schedule.run_pending()
    time.sleep(1)