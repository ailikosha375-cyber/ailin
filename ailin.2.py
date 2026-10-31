
import json
import os
import telebot

# Вставь сюда токен своего бота от BotFather
TOKEN = "8839086068:AAEcWO155Arz8uwWpKaVB_rxDlKHb3VxrmU"

bot = telebot.TeleBot(TOKEN)

# Словарь пользователей
users = {}


# Загрузка данных из JSON
def load_data():
    global users

    if os.path.exists("user.json"):
        try:
            with open("user.json", "r", encoding="utf-8") as file:
                users = json.load(file)
        except (json.JSONDecodeError, OSError):
            users = {}
    else:
        users = {}


# Сохранение данных в JSON
def save_data():
    with open("user.json", "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


# Загружаем данные при старте
load_data()


# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.first_name,
            "username": message.from_user.username or "",
            "age": None
        }
        save_data()

    bot.send_message(
        message.chat.id,
        "Привет! Я бот с сохранением профиля.\n\n"
        "Команды:\n"
        "/profile — посмотреть профиль\n"
        "/setname Имя — изменить имя\n"
        "/setage Возраст — указать возраст"
    )


# Просмотр профиля
@bot.message_handler(commands=["profile"])
def profile(message):
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.first_name,
            "username": message.from_user.username or "",
            "age": None
        }
        save_data()

    user = users[user_id]

    age = user.get("age")
    if age is None:
        age = "12"

    bot.send_message(
        message.chat.id,
        f"👤 Твой профиль\n\n"
        f"Имя: {user['name']}\n"
        f"Возраст: {age}\n"
        f"Username: @{user.get('username') or 'не указан'}"
    )


# Изменение имени
@bot.message_handler(commands=["setname"])
def set_name(message):
    user_id = str(message.from_user.id)
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        bot.send_message(message.chat.id, "Напиши имя так: /setname Алексей")
        return

    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.first_name,
            "username": message.from_user.username or "",
            "age": None
        }

    users[user_id]["name"] = parts[1].strip()
    save_data()

    bot.send_message(message.chat.id, "✅ Имя сохранено!")


# Изменение возраста
@bot.message_handler(commands=["setage"])
def set_age(message):
    user_id = str(message.from_user.id)
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        bot.send_message(message.chat.id, "Напиши возраст так: /setage 20")
        return

    try:
        age = int(parts[1])
        if not 1 <= age <= 120:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "setage 12.")
        return

    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.first_name,
            "username": message.from_user.username or "alikosha",
            "age": 12
        }

    users[user_id]["age"] = age
    save_data()

    bot.send_message(message.chat.id, "✅ Возраст сохранён!")


# Запуск бота
print("Бот запущен!")
bot.infinity_polling()