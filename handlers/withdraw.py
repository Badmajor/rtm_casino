from aiogram import Router
from aiogram.dispatcher.filters import Command
from aiogram.methods import SendMessage
from aiogram.types import Message

from Classes.Class_db import DB_get
from util.db_into import new_pot, new_request_pay, new_out_address


async def cmd_withdraw(message: Message):
    user_id = message.from_user.id
    user = DB_get(user_id)
    pot = user.pot()
    request_pay = user.request_pay()
    address = user.out_address()
    if not address:
        await message.answer('Не указан адресс для выода\n'
                             'используйте команду: /address')
        return
    try:
        withdraw = int(message.text.split()[1])
    except (IndexError, TypeError, ValueError):
        await message.answer('Введите сумму вывода после команды\n'
                             'Пример: /withdraw 1000')
        return
    if withdraw <= pot:
        request_pay += withdraw
        pot -= withdraw
        await new_pot(pot, user_id)
        await new_request_pay(request_pay, user_id)
        msg = await message.answer(f'Вывод {withdraw} на адресс: {address}\n'
                                   f'Принят в обработку. ')
        print(msg)
    else:
        await message.answer(f'Запрошеная сумма превышает ваш банк:{pot} rtm')


async def cmd_address(message: Message):
    try:
        out_address = message.text.split()[1]
    except (IndexError, TypeError, ValueError):
        await message.answer('Введите адрес после команды\n'
                             'Пример: /address RUpnrSxd4vmZqpcsMEsQyxpXLKfA5NB1J9')
        return
    await new_out_address(out_address, message.from_user.id)
    await message.answer(f'Новый адрес для вывода зарегистрирован:\n'
                         f'{out_address}'
                         f'его можно изменить командой /address + новый адрес')


def register_withdraw_commands(router: Router):
    flags = {"throttling_key": "default"}
    router.message.register(cmd_withdraw, Command(commands="withdraw"), flags=flags)
    router.message.register(cmd_address, Command(commands="address"), flags=flags)
