from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, 
    Dispatcher, 
    CallbackContext, 
    Filters, 
    MessageHandler, 
    CommandHandler, 
    CallbackQueryHandler)
import os
import json

TOKEN=os.environ['TOKEN']

updater = Updater(TOKEN)
dp = updater.dispatcher

def start(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = str(update.message.chat.id)
    try:
        with open('data.json','r') as f:
            data=json.loads(f.read())
        like = data[chat_id]['like']
        dislike = data[chat_id]['dislike']
    except:
        data={chat_id:{'like':0,'dislike':0}}
        with open('data.json','w') as f:
            json.dump(data,fp=f, indent=4)
    bot.sendMessage(chat_id=chat_id, text="Send me a Photo")

def photo(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = str(update.message.chat.id)
    photo = update.message.photo[-1]["file_id"]
    with open('data.json','r') as f:
        data=json.loads(f.read())
    like = data[chat_id]['like']
    dislike = data[chat_id]['dislike']

    button1 = InlineKeyboardButton(text = f"👍 {like}", callback_data="like")
    button2 = InlineKeyboardButton(text = f"👎 {dislike}", callback_data="dislike")

    keyboard = InlineKeyboardMarkup([[button1, button2]])
    bot.sendPhoto(chat_id=chat_id, photo=photo, reply_markup=keyboard)

def like_and_dislike(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id=update.message.chat.id
    bot = context.bot
    print(query.data)
    with open('data.json','r') as f:
        data=json.loads(f.read())    
    like = data[f'{chat_id}']['like']
    dislike = data[f'{chat_id}']['dislike']
    if query.data=='like':
        like+=1
    if query.data=='dislike':
        dislike+=1
    print(like)
    print(dislike)
    data[f'{chat_id}']['like'] = like
    data[f'{chat_id}']['dislike'] = dislike
    with open('data.json','w') as f:
        json.dump(data,fp=f, indent=4)
    button1 = InlineKeyboardButton(text = f"👍 {like}", callback_data="like")
    button2 = InlineKeyboardButton(text = f"👎 {dislike}", callback_data="dislike")

    keyboard = InlineKeyboardMarkup([[button1, button2]])
    update.callback_query.message.edit_reply_markup(chat_id=chat_id, reply_markup=keyboard)

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.photo, photo))
dp.add_handler(CallbackQueryHandler(like_and_dislike))
updater.start_polling()
updater.idle()