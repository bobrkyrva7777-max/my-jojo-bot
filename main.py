import telebot
import random
from flask import Flask
from threading import Thread

# Твой токен
bot = telebot.TeleBot('8378354066:AAFowcl7WeULjPr0wYfuDJnnWXPYBnjSh0s')

app = Flask('')
@app.route('/')
def home(): return "Императорский бот в сети!"
def run(): app.run(host='0.0.0.0', port=8080)

# --- ГЛОБАЛЬНЫЙ ИНТЕЛЛЕКТ ---
@bot.message_handler(func=lambda m: True)
def handler(m):
    text = m.text.lower()
    
    # Режим "ДжоДжо-ответы"
    if "как дела" in text:
        bot.reply_to(m, "Я готов вершить правосудие в этом мире, как Дио или Джотаро! А у тебя?")
    
    # Гей-тест (Тот самый)
    elif "гей тест" in text or "на сколько я гей" in text:
        p = random.randint(0, 100)
        bot.reply_to(m, f"🏳️‍🌈 Анализ стенда показал: ты гей на {p}%! 🗿")

    # Команды модерации
    if m.reply_to_message:
        target = m.reply_to_message.from_user.id
        chat = m.chat.id
        
        if text == 'ора':
            bot.ban_chat_member(chat, target)
            bot.reply_to(m, "👊 ORA ORA ORA! Изгнан навсегда.")
        elif text == 'заварудо':
            bot.restrict_chat_member(chat, target, can_send_messages=False)
            bot.reply_to(m, "⏳ ZA WARUDO! Время остановилось, ты в муте!")
        elif text == 'даймонд':
            bot.restrict_chat_member(chat, target, can_send_messages=True)
            bot.reply_to(m, "💎 CRAZY DIAMOND! Восстановлен из мертвых.")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Императорский бот запущен и готов к завоеванию...")
    bot.infinity_polling()
