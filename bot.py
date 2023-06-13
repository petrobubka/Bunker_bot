import random
import asyncio
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import urlparse, parse_qs

from aiogram import Bot, Dispatcher, executor
from aiogram import types
import abilities
import histories
import pandas as pd
import os.path
import string
import csv
import re

logging.basicConfig(level=logging.INFO)

bot = Bot('')


storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
csv_file = 'bot_members.csv'
csv_file_for_text = 'room_text.csv'
columns = ['Full Name', 'Chat ID']
columns_for_text = ['Chat ID', 'Text']

if not os.path.isfile(csv_file):
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file, index=False)

if not os.path.isfile(csv_file_for_text):
    df = pd.DataFrame(columns=columns_for_text)
    df.to_csv(csv_file_for_text, index=False)
@dp.message_handler(commands="sta1rt")
async def start(message: types.Message):
    print(message.get_args())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "Cтворити кімнату",
        "Приєднатися до кімнати",
    ]
    keyboard.add(*buttons)

    await bot.send_message(
        message.chat.id,
        "Вітаємо, {0.first_name}!\nСтвори або долучись до ігрової кімнати, аби почати гру\n ".format(message.from_user),
        parse_mode='html',
        reply_markup=keyboard
    )

@dp.message_handler(text='Приєднатися до кімнати')
async def room(message):
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        room_ids = set(row['Room ID'] for row in csv_reader)

    # Create inline buttons for each unique Room ID
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    for room_id in room_ids:
        inline_keyboard.add(types.InlineKeyboardButton(room_id, callback_data=f"join_room_{room_id}"))

    await bot.send_message(
        message.chat.id,
        "Оберіть кімнату для приєднання:",
        reply_markup=inline_keyboard
    )

@dp.callback_query_handler(lambda query: query.data.startswith('join_room_'))
async def join_room_callback(query: types.CallbackQuery):
    room_id = query.data.split('_')[2]  # Extract the room ID from the callback data
    user_chat_id = query.message.chat.id


    df = pd.read_csv(csv_file)
    df.loc[df['Chat ID'] == user_chat_id, 'Room ID'] = room_id
    df.to_csv(csv_file, index=False)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "👤Персона",
        "🌋Історія",
        "🛖Бункер",
        "📖Правила",
        "⚙️"
    ]
    keyboard.add(*buttons)

    await bot.send_message(
        query.message.chat.id,
        f"You have joined room {room_id}.",
        reply_markup=keyboard
    )



@dp.message_handler(text='Cтворити кімнату')
async def room(message):
    df = pd.read_csv(csv_file)
    user_chat_id = message.chat.id
    user_full_name = message.from_user.full_name

    random_room = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    if user_chat_id in df['Chat ID'].values:
        df.loc[df['Chat ID'] == user_chat_id, 'Full Name'] = user_full_name
    else:
        new_row = pd.DataFrame([[user_full_name, user_chat_id]], columns=columns)
        df = pd.concat([df, new_row], ignore_index=True)

    df.loc[df['Chat ID'] == user_chat_id, 'Room ID'] = random_room
    df.to_csv(csv_file, index=False)
    await bot.send_message(message.chat.id, random_room)
    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "👤Персона",
        "🌋Історія",
        "🛖Бункер",
        "📖Правила",
        "⚙️"
    ]
    keyboard1.add(*buttons)
    await bot.send_message(
        message.chat.id,
        "Вітаємо, {0.first_name}!\nСкоро розпочнеться гра. Сподіваємось у тебе "
        "вийде потрапити в бункер\n Номер твоєї ігрової кімнати: ❇️{1}❇️ ".format(message.from_user, random_room),
        parse_mode='html',
        reply_markup=keyboard1
    )

@dp.message_handler(text='⚙️')
async def room(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "Cтворити кімнату",
        "Приєднатися до кімнати",
    ]
    keyboard.add(*buttons)

    await bot.send_message(
        message.chat.id,
        "Вітаємо, {0.first_name}!\nСтвори або долучись до ігрової кімнати, аби почати гру\n ".format(message.from_user),
        parse_mode='html',
        reply_markup=keyboard
    )

@dp.message_handler(commands=['send_link'])
async def send_link_message(message: types.Message):
    # Create the link
    link_text = "Click here"
    link_url = "https://t.me/Bunker_beta_bot?start=share6"
    link = f"[{link_text}]({link_url})"

    # Create the message with the link
    text_message = f"Please {link} for more information."

    # Send the message
    await message.answer(text_message, parse_mode=types.ParseMode.MARKDOWN)

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
@dp.throttled(lambda message, loop, *args, **kwargs: loop.create_task(bot.send_message(message.from_user.id, "❌ Ви можете створити персонажа один раз на 10 хвилин")),rate=10*60)
async def person(message):
    df = pd.read_csv(csv_file)

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
    global stat
    global ages
    random_sex = str("Стать: ") + str(random.choice(abilities.sex))
    random_age = str("Вік: ") + str(age) + str(" р.")
    random_profession = str("Професія: ") + str(random.choice(abilities.profesion))
    random_childability = str("Здатність мати дітей: ") + str(*random.choices(abilities.childability, weights=childweights))
    random_childdesire = str("Бажання мати дітей: ") + str(*random.choices(abilities.childfree, weights=(3, 1)))
    random_health = str("Здоров'я: ") + str(*random.choices(abilities.health, weights=abilities.healthweights))
    random_disability = str("Інвалідність: ") + str(*random.choices(abilities.disability, weights=abilities.disabilityweights))
    random_phobia = str("Фобія: ") + str(random.choice(abilities.phobia))
    random_hobby = str("Гобі: ") + str(random.choice(abilities.hobby))
    random_education = str("Друга освіта: ") + str(*random.choices(abilities.education, weights=abilities.educationweights))
    random_inventory = str("Багаж: ") + str(random.choice(abilities.inventory))
    random_nature = str("Характер: ") + str(random.choice(abilities.nature))
    random_religion = str("Релігія: ") + str(*random.choices(abilities.religion, weights=abilities.religionweights))
    random_addinfo = str("Дод. інфо: ") + str(random.choice(abilities.addinfo))
    random_mom = str("Мати: ") + str(random.choice(abilities.profesion))
    random_dad = str("Батько: ") + str(random.choice(abilities.profesion))
    random_action1 = str("🃏Карта дії №1:\n ") + str(random.choice(abilities.actioncard))
    random_action2 = str("🃏Карта дії №2:\n ") + str(random.choice(abilities.actioncard))
    a = "👫⏳👷🫃👼🦠👨‍🦽🕷🎨🎓🎒🗣🕍📝👵👨‍🦳"
    await bot.send_message(message.chat.id, "[👫](https://t.me/Bunker_beta_bot?start=share3)" + random_sex, parse_mode=types.ParseMode.MARKDOWN)
    await bot.send_message(message.chat.id, random_age)
    await bot.send_message(message.chat.id, random_profession)
    await bot.send_message(message.chat.id, random_childability)
    await bot.send_message(message.chat.id, random_childdesire)
    await bot.send_message(message.chat.id, random_health)
    await bot.send_message(message.chat.id,random_disability)
    await bot.send_message(message.chat.id, random_phobia)
    await bot.send_message(message.chat.id, random_hobby)
    await bot.send_message(message.chat.id, random_education)
    await bot.send_message(message.chat.id, random_inventory)
    await bot.send_message(message.chat.id, random_nature)
    await bot.send_message(message.chat.id, random_religion)
    await bot.send_message(message.chat.id, random_addinfo)
    await bot.send_message(message.chat.id, random_mom)
    await bot.send_message(message.chat.id, random_dad)
    await bot.send_message(message.chat.id, random_action1)
    await bot.send_message(message.chat.id, random_action2)


    # Update the DataFrame with the 'stat' and 'ages' variables
    user_chat_id = message.chat.id
    user_full_name = message.from_user.full_name

    room_broadcast_text = f"Характеристики гравця {message.from_user.full_name}"

    df1 = pd.read_csv(csv_file_for_text)
    if user_chat_id in df1['Chat ID'].values:
        df1.loc[df['Chat ID'] == user_chat_id, 'Text'] = room_broadcast_text
    else:
        new_row = pd.DataFrame([[user_chat_id, room_broadcast_text]], columns=columns_for_text)
        df1 = pd.concat([df1, new_row], ignore_index=True)
    room_broadcast_text = ""
    texts = df1['Text']
    for text in texts:
        room_broadcast_text += text + "\n\n"
    specific_room_id = df.loc[df['Chat ID'] == user_chat_id]['Room ID'].iloc[0]

    global upload_room_message
    upload_room_message = []
    for index, member in df.iterrows():
        room_id = member['Room ID']
        chat_id = member['Chat ID']
        if room_id == specific_room_id:
            upload_room_message.append(await bot.send_message(chat_id, room_broadcast_text))
    df1.to_csv(csv_file_for_text, index=False)


    df.loc[df['Chat ID'] == user_chat_id, 'Sex'] = random_sex
    df.loc[df['Chat ID'] == user_chat_id, 'Age'] = random_age
    df.loc[df['Chat ID'] == user_chat_id, 'Profession'] = random_profession
    df.loc[df['Chat ID'] == user_chat_id, 'Child Ability'] = random_childability
    df.loc[df['Chat ID'] == user_chat_id, 'Child Desire'] = random_childdesire
    df.loc[df['Chat ID'] == user_chat_id, 'Health'] = random_health
    df.loc[df['Chat ID'] == user_chat_id, 'Disability'] = random_disability
    df.loc[df['Chat ID'] == user_chat_id, 'Phobia'] = random_phobia
    df.loc[df['Chat ID'] == user_chat_id, 'Hobby'] = random_hobby
    df.loc[df['Chat ID'] == user_chat_id, 'Education'] = random_education
    df.loc[df['Chat ID'] == user_chat_id, 'Inventory'] = random_inventory
    df.loc[df['Chat ID'] == user_chat_id, 'Nature'] = random_nature
    df.loc[df['Chat ID'] == user_chat_id, 'Religion'] = random_religion
    df.loc[df['Chat ID'] == user_chat_id, 'Additional Info'] = random_addinfo
    df.loc[df['Chat ID'] == user_chat_id, 'Mother'] = random_mom
    df.loc[df['Chat ID'] == user_chat_id, 'Father'] = random_dad
    df.loc[df['Chat ID'] == user_chat_id, 'Action 1'] = random_action1
    df.loc[df['Chat ID'] == user_chat_id, 'Action 2'] = random_action2

    df.to_csv(csv_file, index=False)
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


@dp.message_handler(commands="broadcast")
async def broadcast(message: types.Message):
    bot_members_file = 'bot_members.csv'
    df_members = pd.read_csv(bot_members_file)
    if message.from_user.id == 275068212:  # Replace YOUR_ADMIN_USER_ID with the actual user ID of the admin
        text = message.text[10:]  # Extract the text after "/broadcast "
        if text:

            for index, member in df_members.iterrows():
                chat_id = member['Chat ID']
                await bot.send_message(chat_id, text)
        else:
            await message.reply("Please provide a message to broadcast.")


@dp.message_handler(commands="start")
async def echo_message(message: types.Message):

    numbers = re.findall(r'\d+', message.get_args())
    arg = 0
    for number in numbers:
        arg = number
    arg = int(arg)
    if message.get_args() == f"share{arg}":
        await message.delete()
        user_chat_id = message.chat.id
        df = pd.read_csv(csv_file_for_text)
        room_broadcast_text = df.loc[df['Chat ID'] == user_chat_id]['Text'].iloc[0]
        print(message.text)
        with open('bot_members.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                print(row[1])
                if row[1] == str(message.from_user.id):
                    room_broadcast_text += "\n"
                    room_broadcast_text += row[arg]
                    df.loc[df['Chat ID'] == user_chat_id, 'Text'] = room_broadcast_text
                    df.to_csv(csv_file_for_text, index=False)
                    texts = df['Text']
                    room_broadcast_text = ""
                    for text in texts:
                        room_broadcast_text += text + "\n\n"
                    for i in upload_room_message:
                            await i.edit_text(text=room_broadcast_text)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            "Cтворити кімнату",
            "Приєднатися до кімнати",
        ]
        keyboard.add(*buttons)

        await bot.send_message(
            message.chat.id,
            "Вітаємо, {0.first_name}!\nСтвори або долучись до ігрової кімнати, аби почати гру\n ".format(
                message.from_user),
            parse_mode='html',
            reply_markup=keyboard
        )


        # You can perform further actions here if the condition is met
    # else:
    #     await bot.send_message(message.from_user.id, str("Схоже щось пішло не так...\nНатисни сюди — \"/start\""))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
