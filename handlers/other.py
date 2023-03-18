from creating_bot import bot, dp
from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram import md, F
from aiogram.filters import Text
from datetime import datetime

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
async def without_puree(message: types.Message):
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


def handler_register_other(dp: Dispatcher):
    dp.message.register(button_creation, Command('food'))
    dp.message.register(with_puree, Text(''))