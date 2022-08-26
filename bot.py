import random
import telebot
import requests
import abilities
import histories
from telebot import types

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13" \
                                                      "-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT "

bot = telebot.TeleBot('1473850435:AAEOSlGS0fsyn2fzCtlEOGh3mvlGck0ktno')


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("👤Персона")
    item2 = types.KeyboardButton("🌋Історія")
    item3 = types.KeyboardButton("🛖Бункер")
    item4 = types.KeyboardButton("📖Правила")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id,
                     "Вітаємо, {0.first_name}!\nСкоро розпочнеться гра. Сподіваємось у тебе вийде потрапити в бункер ".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '👤Персона':
            age = random.randint(16, 95)
            childweights = (0, 0)
            if age < 30:
                childweights = (8, 1)
            elif age < 35:
                childweights = (5, 1)
            elif age < 40:
                childweights = (2, 1)
            elif age < 50:
                childweights = (1, 1)
            elif age < 60:
                childweights = (1, 3)
            elif age < 70:
                childweights = (1, 5)
            elif age < 100:
                childweights = (1, 8)
            bot.send_message(message.chat.id, str("Стать: ") + str(random.choice(abilities.sex)))
            bot.send_message(message.chat.id, str("Вік: ") + str(age) + str(" р."))
            bot.send_message(message.chat.id, str("Професія: ") + str(random.choice(abilities.profesion)))
            bot.send_message(message.chat.id, str("Здатність мати дітей: ") + str(
                *random.choices(abilities.childability, weights=childweights)))
            bot.send_message(message.chat.id,
                             str("Бажання мати дітей: ") + str(*random.choices(abilities.childfree, weights=(3, 1))))
            bot.send_message(message.chat.id,
                             str("Здоров'я: ") + str(*random.choices(abilities.health, weights=abilities.healthweights)))
            bot.send_message(message.chat.id, str("Інвалідність: ") + str(
                *random.choices(abilities.disability, weights=abilities.disabilityweights)))
            bot.send_message(message.chat.id, str("Фобія: ") + str(random.choice(abilities.phobia)))
            bot.send_message(message.chat.id, str("Гобі: ") + str(random.choice(abilities.hobby)))
            bot.send_message(message.chat.id, str("Друга освіта: ") + str(
                *random.choices(abilities.education, weights=abilities.educationweights)))
            bot.send_message(message.chat.id, str("Багаж: ") + str(random.choice(abilities.inventory)))
            bot.send_message(message.chat.id, str("Харктер: ") + str(random.choice(abilities.nature)))
            bot.send_message(message.chat.id,
                             str("Релігія: ") + str(*random.choices(abilities.religion, weights=abilities.religionweights)))
            bot.send_message(message.chat.id, str("Дод. інфо: ") + str(random.choice(abilities.addinfo)))
            bot.send_message(message.chat.id, str("Мати: ") + str(random.choice(abilities.profesion)))
            bot.send_message(message.chat.id, str("Батько: ") + str(random.choice(abilities.profesion)))
            bot.send_message(message.chat.id, str("🃏Карта дії №1: ") + str(random.choice(abilities.actioncard)))
            bot.send_message(message.chat.id, str("🃏Карта дії №2: ") + str(random.choice(abilities.actioncard)))

        elif message.text == '🛖Бункер':
            locate = ["Анкара, Туреччина", "Москва, Росія", "Лондон, Британія ", "Київ, Україна", "Жмеринка, Україна",
                      "Тегусігальпа, Гондурас", "Вашингтон, США", "Абу-Дабі, ОАЕ", "Баку, Азербайджан",
                      "Брюсель, Бельгія",
                      "Бухарест, Румунія", "Делі, Індія", "Мінськ, Білорусія", "Самбір, Україна", "Париж, Франція",
                      "Берлін, Німеччина", "Варшава, Польща"]

            vorog = ["Далеко", "1 км", "5 км", "10 км", "20 км", "50 км", "100 км", "500 м", "Невідомо"]
            vorogloc = str(random.choice(vorog))
            vorog1 = "До ворожого бункера: "
            v = "Бункер №" + str(random.randint(0, 999)) + "\n" + "Місцезнаходження: " + str(random.choice(locate)) \
                + "\n" + "Розмір: " + str(random.randint(30, 800)) + "m²" + "\n" + "Їжі достатньо на: " \
                + str(random.randint(1, 52)) + " міс." + "\n" + "До ворожого бункера: " + str(random.choice(vorog) \
                                                                                              + "\n" + "Час який треба пробути в бункері: " + str(
                random.randint(36, 600)) + " міс.")
            bot.send_message(message.chat.id, v)
        elif message.text == '🌋Історія':
            stories = [histories.story1, histories.story2, histories.story3, histories.story4,
                       histories.story5, histories.story6, histories.story7, histories.story8]
            bot.send_message(message.chat.id, str(random.choice(stories)))
        elif message.text == '📖Правила':
            rules = """Правила\n           
• Кожен гравець створює свого персонажа за допомогою ключового слова "Персона" \n\
• Колективним рішенням обирається людина, яка перед початком гри зачитає \
інформацію, яку отримає через кодові слова: "Історія" та "Бункер". \n\
• Людина, яка оголошувала цю інформацію починає коло та обирає його напрям. \n\
• Гравці по черзі повинні відкривати по 2 пункти на вибір свого персонажа кожного кола(Окрім \
першого кола, під час нього усі відкривають свою професію, стать, та ще 1 пункт на вибір кожого гравця) \
на це їм \
відведено по 2 хвилини, за цей час вони повинні довести свою важливість для бункера \
відносно тих характеристик, які вони відкрили щойно або раніше. \n\
• У кінці кола гравці голосують за людину, яку буде вигнано з кола. \n\
• Карти дій характеристиками не є і можуть бути застосовані в будь-який час гри(за виключенням моменту \
коли гравець, що використовує карту вигнаний з кола чи мертвий :) \n\
• Ваша задача - протриматись у грі якомога довше \n\
• Гра завершується, коли у колі залишається певна кількість людей, скільки саме - вирішувати вам \n\
Щасти тобі потрапити в бункер \n\
                """
            bot.send_message(message.chat.id, str(rules))
        else:
            list_of_commands = """Схоже щось пішло не так...\n\
Натисни сюди — "/start" \n\

                """
            bot.send_message(message.chat.id, str(list_of_commands))


# RUN
bot.polling(none_stop=True)
