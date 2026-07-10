import telebot
import random
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# --- КОНФИГУРАЦИЯ ---
TELEGRAM_TOKEN = '8378354066:AAFowcl7WeULjPr0wYfuDJnnWXPYBnjSh0s'
# Получи ключ здесь: https://aistudio.google.com/
GOOGLE_API_KEY = "805219e9090b9a27b6a5f019182cc8340e4ad8377d24208db2492947dcd55b3c" # <--- ВСТАВИТЬ КЛЮЧ СЮДА

# --- ИНИЦИАЛИЗАЦИЯ ---
# Настройка ИИ
if GOOGLE_API_KEY == "ВСТАВЬ СЮДА СВОЙ КЛЮЧ (API KEY)":
    print("ВНИМАНИЕ: Не задан API KEY для ИИ! Бот будет работать без умных ответов.")
    ai_active = False
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    ai_active = True

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Веб-сервер (чтобы бот не засыпал на Render)
app = Flask('')
@app.route('/')
def home(): return "ИИ-Император в сети!"
def run(): app.run(host='0.0.0.0', port=8080)

# --- ЛОГИКА БОТА ---

@bot.message_handler(commands=['start'])
def send_welcome(m):
    bot.reply_to(m, "ZA WARUDO! Я готов к работе. @mention меня в группе, чтобы я ответил как ИИ, или используй команды модерации.")

# Команды модерации (только в ответ на сообщение)
@bot.message_handler(func=lambda m: m.reply_to_message)
def moderation(m):
    cmd = m.text.lower().strip()
    target = m.reply_to_message.from_user.id
    target_name = m.reply_to_message.from_user.first_name
    chat = m.chat.id

    if cmd == 'ора':
        try:
            bot.ban_chat_member(chat, target)
            bot.reply_to(m, f"👊 ORA ORA ORA! {target_name} изгнан навсегда.")
        except Exception as e:
            bot.reply_to(m, f"Не удалось наказать (возможно, админ): {e}")
            
    elif cmd == 'заварудо':
        try:
            bot.restrict_chat_member(chat, target, until_date=time.time()+3600, can_send_messages=False)
            bot.reply_to(m, f"⏳ ZA WARUDO! Время остановилось для {target_name} на 1 час.")
        except Exception as e:
            bot.reply_to(m, f"Не удалось остановить время: {e}")
        
    elif cmd == 'даймонд':
        try:
            bot.restrict_chat_member(chat, target, can_send_messages=True)
            bot.reply_to(m, f"💎 CRAZY DIAMOND! {target_name} восстановлен.")
        except Exception as e:
            bot.reply_to(m, f"Не удалось исправить: {e}")

# Гей-тест (работает везде)
@bot.message_handler(func=lambda m: "гей тест" in m.text.lower().strip() or "на сколько я гей" in m.text.lower().strip())
def gay_test(m):
    p = random.randint(0, 100)
    res = f"🏳️‍🌈 Анализ стенда показал: {m.from_user.first_name}, ты гей на {p}%! 🗿"
    if p > 75: res += "\nТы воплощение Дио Брандо!"
    elif p > 35: res += "\nТы обычный пользователь Stand."
    else: res += "\nТы чист как Джонатан Джостар."
    bot.reply_to(m, res)

# Умный ИИ-ответ (только в личке или при упоминании бота @username)
@bot.message_handler(func=lambda m: True)
def ai_responder(m):
    is_private = m.chat.type == 'private'
    is_mentioned = m.text and bot.user.username and f"@{bot.user.username}" in m.text
    
    if ai_active and (is_private or is_mentioned):
        try:
            # Удаляем упоминание бота из текста запроса, чтобы ИИ не видел "@my_bot"
            clean_text = m.text.replace(f"@{bot.user.username}", "").strip()
            if not clean_text: return # Если просто @bot без текста, игнорируем
            
            # Отправляем запрос к Gemini
            response = model.generate_content(f"Ты персонаж из аниме JoJo's Bizarre Adventure. Ответь на вопрос пользователя в стиле ДжоДжо: {clean_text}")
            
            # Отправляем ответ бота
            bot.reply_to(m, response.text)
            
        except Exception as e:
            print(f"Ошибка ИИ: {e}")
            bot.reply_to(m, "Мой стенд перегрелся, я не могу сейчас ответить... Попробуй позже.")
    elif not ai_active and (is_private or is_mentioned):
        bot.reply_to(m, "ИИ-модуль не активирован. Введите API Key в код.")

# --- ЗАПУСК ---
if __name__ == "__main__":
    # Запускаем Flask-сервер в отдельном потоке
    t = Thread(target=run)
    t.start()
    print("Императорский ИИ-бот запущен и готов...")
    bot.infinity_polling()