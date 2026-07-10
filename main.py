import telebot
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

bot = telebot.TeleBot('8378354066:AAFowcl7WeULjPr0wYfuDJnnWXPYBnjSh0s')
rules = "📋 ПРАВИЛА: 1. Без 18+. 2. Без мата. 3. Без спама."

app = Flask('')
@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['правила', 'info'])
def send_rules(m):
    bot.reply_to(m, rules)

@bot.message_handler(func=lambda m: m.reply_to_message)
def moderation(m):
    cmd = m.text.lower().strip()
    target = m.reply_to_message.from_user.id
    chat = m.chat.id

    if cmd == 'ора':
        bot.ban_chat_member(chat, target)
        bot.reply_to(m, "👊 ORA ORA! Нарушитель забанен.")
    
    elif cmd == 'заварудо':
        until = datetime.now() + timedelta(hours=1)
        bot.restrict_chat_member(chat, target, until_date=until.timestamp(), can_send_messages=False)
        bot.reply_to(m, "⏳ ZA WARUDO! Время остановилось на 1 час.")
        
    elif cmd == 'даймонд':
        bot.restrict_chat_member(chat, target, 
                                 can_send_messages=True, can_send_audios=True, 
                                 can_send_documents=True, can_send_photos=True, 
                                 can_send_videos=True, can_send_video_notes=True, 
                                 can_send_voice_notes=True, can_send_polls=True, 
                                 can_send_other_messages=True, add_web_page_previews=True)
        bot.reply_to(m, "💎 CRAZY DIAMOND! Участник полностью восстановлен.")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Бот запущен...")
    bot.infinity_polling()
