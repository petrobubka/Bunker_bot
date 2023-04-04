import random
import asyncio
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor
from aiogram import types
import abilities
import histories

logging.basicConfig(level=logging.INFO)

bot = Bot('')


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["👤Персона", "🌋Історія", "🛖Бункер", "📖Правила"]
    keyboard.add(*buttons)
    await bot.send_message(message.chat.id, "Вітаємо, {0.first_name}!\nСкоро розпочнеться гра. Сподіваємось у тебе "
                                            "вийде потрапити в бункер ".format(message.from_user), parse_mode='html',
                           reply_markup=keyboard)
@dp.message_handler(text='🛖Бункер')
async def bunker(message):
    locate = ["Анкара, Туреччина", "Москва, Росія", "Лондон, Британія ", "Київ, Україна", "Жмеринка, Україна",
              "Тегусігальпа, Гондурас", "Вашингтон, США", "Абу-Дабі, ОАЕ", "Баку, Азербайджан",
              "Брюсель, Бельгія",
              "Бухарест, Румунія", "Делі, Індія", "Мінськ, Білорусія", "Самбір, Україна", "Париж, Франція",
              "Берлін, Німеччина", "Варшава, Польща"]

    vorog = ["Далеко", "1 км", "5 км", "10 км", "20 км", "50 км", "100 км", "500 м", "Невідомо"]
    v = "Бункер №" + str(random.randint(0, 999)) + "\n" + "Місцезнаходження: " + str(random.choice(locate))\
        + "\n" + "Розмір: " + str(random.randint(30, 800)) + "m²" + "\n" + "Їжі достатньо на: " \
        + str(random.randint(1, 52)) + " міс." + "\n" + "До ворожого бункера: " + str(random.choice(vorog)  \
        + "\n" + "Час який треба пробути в бункері: " + str(random.randint(36, 600)) + " міс.")
    await bot.send_message(message.chat.id, v)
@dp.message_handler(text='👤Персона')
@dp.throttled(lambda msg, loop, *args, **kwargs: loop.create_task(bot.send_message(msg.from_user.id, "❌ Ви можете створити персонажа один раз на 10 хвилин")),rate=10*60)
async def person(message):
    loading = ["👫Обираємо стать", "🗄Готуємо професію", "💊Лікуємо здоров'я", "🧳Набираємо багаж", "📝Навчаємо освіти", "🃏Роздаємо картки дії"]
    upload_message = await bot.send_message(chat_id=message.chat.id, text="🫀Cтворюємо персонажа")
    await asyncio.sleep(1)
    for i in loading:
        await upload_message.edit_text(text=f"{i}")
        await asyncio.sleep(0.5)
    await asyncio.sleep(0.5)
    await bot.delete_message(chat_id=message.chat.id, message_id=upload_message.message_id)
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
    await bot.send_message(message.chat.id, str("Стать: ") + str(random.choice(abilities.sex)))
    await bot.send_message(message.chat.id, str("Вік: ") + str(age) + str(" р."))
    await bot.send_message(message.chat.id, str("Професія: ") + str(random.choice(abilities.profesion)))
    await bot.send_message(message.chat.id, str("Здатність мати дітей: ") + str(*random.choices(abilities.childability, weights=childweights)))
    await bot.send_message(message.chat.id,
                     str("Бажання мати дітей: ") + str(*random.choices(abilities.childfree, weights=(3, 1))))
    await bot.send_message(message.chat.id,
                     str("Здоров'я: ") + str(*random.choices(abilities.health, weights=abilities.healthweights)))
    await bot.send_message(message.chat.id, str("Інвалідність: ") + str(
        *random.choices(abilities.disability, weights=abilities.disabilityweights)))
    await bot.send_message(message.chat.id, str("Фобія: ") + str(random.choice(abilities.phobia)))
    await bot.send_message(message.chat.id, str("Гобі: ") + str(random.choice(abilities.hobby)))
    await bot.send_message(message.chat.id, str("Друга освіта: ") + str(
        *random.choices(abilities.education, weights=abilities.educationweights)))
    await bot.send_message(message.chat.id, str("Багаж: ") + str(random.choice(abilities.inventory)))
    await bot.send_message(message.chat.id, str("Харктер: ") + str(random.choice(abilities.nature)))
    await bot.send_message(message.chat.id,
                     str("Релігія: ") + str(*random.choices(abilities.religion, weights=abilities.religionweights)))
    await bot.send_message(message.chat.id, str("Дод. інфо: ") + str(random.choice(abilities.addinfo)))
    await bot.send_message(message.chat.id, str("Мати: ") + str(random.choice(abilities.profesion)))
    await bot.send_message(message.chat.id, str("Батько: ") + str(random.choice(abilities.profesion)))
    await bot.send_message(message.chat.id, str("🃏Карта дії №1:\n ") + str(random.choice(abilities.actioncard)))
    await bot.send_message(message.chat.id, str("🃏Карта дії №2:\n ") + str(random.choice(abilities.actioncard)))
@dp.message_handler(text='🌋Історія')
async def story(message):
    stories = [histories.story1, histories.story2, histories.story3, histories.story4,
    histories.story5, histories.story6, histories.story7, histories.story8]
    await bot.send_message(message.chat.id, str(random.choice(stories)))
@dp.message_handler(text='📖Правила')
async def story(message):
    rules = """Правила\n           
• Кожен гравець створює свого персонажа за допомогою ключового слова "Персона" \n\
• Колективним рішенням обирається людина, яка перед початком гри зачитає \
інформацію, яку отримає через кодові слова: "Історія" та "Бункер". \n\
• Людина, яка оголошувала цю інформацію починає коло та обирає його напрям. \n\
• Гравці по черзі повинні відкривати по 2 пункти на вибір свого персонажа кожного кола(Окрім \
першого кола, під час нього усі відкривають свою стать, професію та одну х-ку на вибір) \
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
    await bot.send_message(message.chat.id, str(rules))
@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, str("""Схоже щось пішло не так...\n\
Натисни сюди — "/start"""))
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
