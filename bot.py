import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram import md, F
from datetime import datetime

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


# создали хендлер для любого текста в принципе
# получается, что message.text возвращает текст, хранимый в отправляемом сообщении
@dp.message(F.text)
async def time_sender(message: types.Message):
    time_now = datetime.now().strftime('%Y\-%m\-%d %H:%M')
    added_text = md.underline(f'Отправлено в {time_now}')
    await message.answer(f'{message.text}\n\n{md.bold(added_text)}')


# Запуск процесса поллинга новых апдейтов
async def main():
    # зарегали тут хэндлер cmd_test2 по команде /test2
    dp.message.register(cmd_test2, Command('test2'))

    await dp.start_polling(bot, mylist=[1, 2, 3])


if __name__ == "__main__":
    asyncio.run(main())
