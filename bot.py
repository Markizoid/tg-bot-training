import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram import md, F
from datetime import datetime
from aiogram.filters import Text

from config_reader import config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="MarkdownV2")
# Диспетчер
dp = Dispatcher()


# mylist = [1,2,3]


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


# Хэндлер на команду /test1
@dp.message(Command("reply"))
async def cmd_reply(message: types.Message):
    await message.reply("I can reply on your message!!")


# Хэндлер на команду /test2
# Без декоратора, т.к. регистрируется ниже в функции main()
async def cmd_test2(message: types.Message):
    await message.reply("Test 2")


@dp.message(Command("answer"))
async def cmd_answer(message: types.Message):
    await message.answer("And I can just simply writing messages!")


# стандартная задача функции ответа кубиком
@dp.message(Command("dice_reply"))
async def cmd_dice(message: types.Message):
    await message.reply_dice(emoji=DiceEmoji.DICE)


# передача аргументов
@dp.message(Command("add_to_list"))
async def cmd_add_to_list(message: types.Message, mylist: list[int]):
    mylist.append(7)
    await message.answer(f"Добавлено число 7")


@dp.message(Command("show_list"))
async def cmd_show_list(message: types.Message, mylist: list[int]):
    await message.answer(f"Ваш список: {mylist}")


# ПЕРЕДАЧА СООБЩЕНИЯ В КАКОЙ-НИБУДЬ ДРУГОЙ ЧАТ С id
# @dp.message(Command("dice"))
# async def cmd_dice(message: types.Message, bot:Bot):
#     await bot.send_dice(-тут_должен_быть_id,  emoji=DiceEmoji.DICE)

@dp.message(Command('text'))
async def text_sender(message: types.Message):
    await message.answer('Hello, *world*\!')


@dp.message(Command('name'))
async def name_sender(message: types.Message, command: CommandObject):
    if command.args:
        await message.reply(f'good to read from you, {md.bold(md.quote(command.args))}\!')
    else:
        await message.reply(f'need to know your name, buddy\! type after command /name')


@dp.message(Command('food'))
async def button_creation(message: types.Message):
    # тут мы типа создали заготовки для кнопок, их надписи
    kb = [[
        types.KeyboardButton(text="С пюрешкой"),
        types.KeyboardButton(text="Без пюрешки")
    ]]
    # кнопки которые отвечают
    keyboard = types.ReplyKeyboardRemove(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите способ подачи',
        one_time_keyboard=True
    )
    await message.answer('Как подавать каклетки?', reply_markup=keyboard)

@dp.message(Text('С пюрешкой'))
async def with_puree(message: types.Message):
    await message.reply('Отличный выбор\! Сделаем с пюрешкой')

@dp.message(Text('Без пюрешки'))
async def with_puree(message: types.Message):
    await message.reply(f'{md.bold("Просто коклетка?")} Ну лан че\.\.\.')

# создали хендлер для любого текста в принципе
# получается, что message.text возвращает текст, хранимый в отправляемом сообщении
@dp.message(F.text)
async def time_sender(message: types.Message):
    time_now = datetime.now().strftime('%Y\-%m\-%d %H:%M')
    added_text = md.underline(f'Отправлено в {time_now}')

    if message.text.startswith('когда'):
        await message.answer(f'{message.text[5:]}\n\n{md.bold(added_text)}')
    else:

        data = {
            'email': 'None',
            'code': 'None',  # только code блять
            'url': 'None'
        }
        entities = message.entities
        if entities:  # это я сам дописал
            for item in entities:
                if item.type in data.keys():
                    data[item.type] = item.extract_from(message.text)

            await message.reply(
                "Here's what I found:\n\n"
                f"URL: {md.quote(data['url'])}\n"
                f"Password: {md.quote(data['code'])}\n"
                f"Email: {md.quote(data['email'])}\n"
            )






# эта штука для приветственного сообщения новопришедших в канал
# @dp.message(F.new_chat_members)
# async def somebody_added(message: types.Message):
#     for user in message.new_chat_members:
#         # проперти full_name берёт сразу имя И фамилию
#         await message.reply(f"Привет, {user.full_name}")


# Запуск процесса поллинга новых апдейтов
async def main():
    # зарегали тут хэндлер cmd_test2 по команде /test2
    dp.message.register(cmd_test2, Command('test2'))

    await dp.start_polling(bot, mylist=[1, 2, 3])


if __name__ == "__main__":
    asyncio.run(main())
