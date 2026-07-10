import telebot
import random
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

bot = telebot.TeleBot('8378354066:AAFowcl7WeULjPr0wYfuDJnnWXPYBnjSh0s')

# База данных
db = {"rules": "📋 ПРАВИЛА: 1. Без 18+. 2. Без мата. 3. Без спама.", "rep": {}}

app = Flask('')
@app.route('/')
def home(): return "Бот работает!"

def run(): app.run(host='0.0.0.0', port=8080)

# --- ИРИС-КОМАНДЫ ---
@bot.message_handler(commands=['правила', 'info', 'инфо'])
def send_rules(m): bot.reply_to(m, db["rules"])

@bot.message_handler(commands=['статистика', 'stats'])
def stats(m): bot.reply_to(m, "📊 Бот работает в штатном режиме. Стенд готов к бою!")

# --- ДЖОДЖО-РЕЙТИНГ ---
@bot.message_handler(func=lambda m: "на сколько я гей" in m.text.lower() or "гей тест" in m.text.lower())
def gay_test(m):
    p = random.randint(0, 100)
    res = f"🏳️‍🌈 Уровень ДжоДжо-гейства пользователя {m.from_user.first_name}: {p}%."
    if p > 80: res += "\n🌟 Ты — Дио Брандо! Легенда!"
    elif p > 40: res += "\n🗿 Ты обычный ДжоДжо-фаг."
    else: res += "\n👊 Ты чист как Джонатан Джостар!"
    bot.reply_to(m, res)

# --- МОДЕРАЦИЯ (ИРИС + ДЖОДЖО) ---
@bot.message_handler(func=lambda m: m.reply_to_message)
def moderation(m):
    cmd = m.text.lower().strip()
    target = m.reply_to_message.from_user.id
    chat = m.chat.id
    
    # Репутация
    if cmd in ['+', 'спасибо', 'лайк']:
        db["rep"][target] = db["rep"].get(target, 0) + 1
        bot.reply_to(m, f"📈 Репутация пользователя {m.reply_to_message.from_user.first_name} повышена! (Всего: {db['rep'][target]})")
        return

    # Наказания
    if cmd in ['ора', '!бан', 'бан']:
        bot.ban_chat_member(chat, target)
        bot.reply_to(m, "👊 ORA ORA! Нарушитель изгнан из чата!")
    
    elif cmd in ['заварудо', '!мут', 'мут']:
        until = datetime.now() + timedelta(hours=1)
        bot.restrict_chat_member(chat, target, until_date=until.timestamp(), can_send_messages=False)
        bot.reply_to(m, "⏳ ZA WARUDO! Время остановлено для нарушителя!")
        
    elif cmd in ['даймонд', '!размут', 'размут', 'возврат']:
        bot.restrict_chat_member(chat, target, can_send_messages=True)
        bot.reply_to(m, "💎 CRAZY DIAMOND! Нарушитель исцелен!")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()