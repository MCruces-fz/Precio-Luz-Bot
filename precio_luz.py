import requests
import json
import pandas as pd
import telebot
# from python_whatsapp_bot import Whatsapp

BOT_TOKEN = '6665531181:AAF_ScnEJ5-iy5vHGYnTw-ggCBCdoR3QcQk'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Hello world')

def get_daily_prices():
    response = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB")
    
    # request
    json_response = response.json()
    string_response = json.dumps(json_response, indent=2)
    
    # to dataframe
    df = pd.DataFrame.from_dict(json_response, orient="index")
    df = df.drop(columns=['is-cheap', 'market'])
    df = df.rename(columns={'is-under-avg': 'cunde'})

    # date and time
    df["str-date-time"] = df.apply(lambda row: f"{row.date} {row.hour.split('-')[0]}", axis=1)
    df = df.drop(columns=['date', 'hour'])
    df["date-time"] = pd.to_datetime(df["str-date-time"], format='%d-%m-%Y %H')
    df["date"] = df["date-time"].dt.strftime("%Y-%m-%d")
    df["time"] = df["date-time"].dt.strftime("%Hh")
    date = df["date"].iloc[0]
    df = df.drop(columns=['str-date-time', 'date-time', 'date'])

    # price
    df['cost'] = df.apply(lambda row: f"{row.price}{row.units}", axis=1)
    df = df.drop(columns=['price', 'units'])

    df = df[['time', 'cost', 'cunde']]

    return {"date":date, "df":df}

@bot.message_handler(commands=['precio', 'luz'])
def prices_handler(message):
    prices_dict = get_daily_prices()
    df = prices_dict['df'].reset_index(drop=True)
    date = prices_dict['date']

    bot.send_message(message.chat.id, f"Fecha: {date}")

    # md_table = df.to_markdown(index=False)
    # text = f"```\n{md_table}\n```"
    # bot.send_message(message.chat.id, text, parse_mode="Markdown")

    # text = f"<pre>\n{md_table}\n</pre>"
    # bot.send_message(message.chat.id, text, parse_mode="HTML")

    # html_table = df.to_html(index_names=False)
    # bot.send_message(message.chat.id, html_table, parse_mode="HTML")

    bot.send_message(message.chat.id, f"<pre>{df}</pre>", parse_mode="html", reply_to_message_id=message.message_id)    

# print(get_daily_prices())

bot.infinity_polling()
