from creating_bot import dp
from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import CommandObject
from aiogram import md, F


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


# эта штука для приветственного сообщения новопришедших в канал
# @dp.message(F.new_chat_members)
# async def somebody_added(message: types.Message):
#     for user in message.new_chat_members:
#         # проперти full_name берёт сразу имя И фамилию
#         await message.reply(f"Привет, {user.full_name}")

def handler_register_client(dp: Dispatcher):
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_reply, Command('reply'))
    dp.message.register()