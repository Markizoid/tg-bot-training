import asyncio
import logging
from config_reader import config
from aiogram import Bot, Dispatcher, types
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram import md, F
from datetime import datetime
from aiogram.filters import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from random import randint
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest


class NumberCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int]

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


'''--------------------- INLINE-КНОПКИ -------------------------------'''

@dp.message(Command('food'))
async def button_creation(message: types.Message):
    # тут мы типа создали заготовки для кнопок, их надписи
    kb = [[
        types.KeyboardButton(text="С пюрешкой"),
        types.KeyboardButton(text="Без пюрешки")
    ]]
    # кнопки которые отвечают
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите способ подачи',
        one_time_keyboard=True,
    )
    await message.answer('Как подавать каклетки?', reply_markup=keyboard)


@dp.message(Text('С пюрешкой'))
async def with_puree(message: types.Message):
    await message.reply('Отличный выбор\! Сделаем с пюрешкой')

@dp.message(Text('Без пюрешки'))
async def with_puree(message: types.Message):
    await message.reply(f'{md.bold("Просто коклетка?")} Ну лан че\.\.\.')

@dp.message(Command('keyboard'))
async def reply_keyboard(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        'Выберите число:',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(Command('my_id'))
async def send_id(message: types.Message):
    await message.reply(f"Твой id : {md.quote(md.bold(message.from_user.id))}")


@dp.message(Command('buttons'))
async def special_buttons(message: types.Message):
    builder_ = ReplyKeyboardBuilder()

    builder_.row(
        types.KeyboardButton(text="Запросить геолокацию", request_location=True),
        types.KeyboardButton(text="Запросить контакт", request_contact=True),
    )
    builder_.row(
        types.KeyboardButton(text="Выбрать преимиум-пользователя",
                             request_user=types.KeyboardButtonRequestUser(
                                 request_id=1,
                                 user_is_premium=True,
                                ),
                             ),
        )
    builder_.row(
        types.KeyboardButton(text="Выбрать супергруппу с форумами",
                             request_chat=types.KeyboardButtonRequestChat(
                                 request_id=2,
                                 chat_is_channel=False,
                                 chat_is_forum=True,
                                ),
                             ),
        )
    await message.answer(
        'Выберите действие:',
        reply_markup=builder_.as_markup(resize_keyboard=True),
    )


@dp.message(Command('inline_url'))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder_ = InlineKeyboardBuilder()
    builder_.row(types.InlineKeyboardButton(
        text="Guthib", url='https://github.com'),
    )
    builder_.row(types.InlineKeyboardButton(
        text="Оф. канал Telegram",
        url='tg://resolve?domain=telegram'),
    )
    user_id=197122807
    # запрашиваем инфу о чате с пользователем
    chat_info = await bot.get_chat(user_id)
    # если он разрешает переход к чату, то выводим кнопку
    if not chat_info.has_private_forwards:
        builder_.row(types.InlineKeyboardButton(
            text="НУ ТИПА Админ",
            url=f"tg://user?id={user_id}"
        ))

    await message.answer(
        'Выберите ссылку',
        reply_markup=builder_.as_markup(),
    )

'''--------------------- CALLBACK-КНОПКИ -------------------------------'''
@dp.message(Command('random'))
async def cmd_random(message: types.Message):
    builder_ = InlineKeyboardBuilder()
    builder_.add(types.InlineKeyboardButton(
        text="Нажми меня!",
        callback_data='randomiser',
    ))
    await message.reply(
        'Нажмите на кнопку, чтобы бот отправил число от 1 до 10',
        reply_markup=builder_.as_markup(),
    )

@dp.callback_query(Text('randomiser'))
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer(
        text="Спасибо, что воспользовались рандомайзером!",
        show_alert=True,
    )


def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(
        f"Укажите число: {new_value}",
        reply_markup=get_keyboard()
    )


@dp.message(Command("numbers"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())


'''--------------ФАБРИКА КОЛБЭКОВ-----------------'''

user_data = {}

def get_keyboard_fab():
    builder_ = InlineKeyboardBuilder()
    builder_.button(
        text="-2", callback_data=NumberCallbackFactory(action="change", value=-2)
    )
    builder_.button(
        text="-1", callback_data=NumberCallbackFactory(action="change", value=-1)
    )
    builder_.button(
        text="+1", callback_data=NumberCallbackFactory(action="change", value=1)
    )
    builder_.button(
        text="+2", callback_data=NumberCallbackFactory(action="change", value=2)
    )
    builder_.button(
        text="Подтвердить", callback_data=NumberCallbackFactory(action="finish")
    )
    builder_.adjust(4)
    return builder_.as_markup()


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Укажите число: {new_value}",
            reply_markup=get_keyboard_fab()
        )


@dp.message(Command("numbers_fab"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())


@dp.callback_query(NumberCallbackFactory.filter())
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: NumberCallbackFactory,
        ):
    # текущее значение
    user_value = user_data.get(callback.from_user.id, 0)

    if callback_data.action == "incr":
        user_data[callback.from_user.id] = user_value + callback_data.value
        await update_num_text_fab(callback.message, user_value + callback_data)
    else:
        await callback.message.edit_text(f"Итого: {user_value}")
    await callback.answer()

# создали хендлер для любого текста в принципе (поэтому в конце)
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
