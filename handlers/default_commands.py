from textwrap import dedent

from aiogram import Router
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from Classes.Class_db import DB_get
from keyboards.spin_keyboard import get_spin_keyboard
from util.db_into import registration


async def cmd_start(message: Message):
    user = DB_get(message.from_user.id)
    if user.status():
        await registration(message.from_user.id)
        user = DB_get(message.from_user.id)
    pot = user.pot()
    address = user.address()
    start_text = """\
    *Добро пожаловать в наше виртуальное казино!*
    У вас на счете {pot} rtm. Каждая попытка стоит 1 rtm, а за выигрышные комбинации вы получите:
    """

    rules = """\
    3 одинаковых символа (кроме семёрки) — 7 rtm
    7️⃣7️⃣▫️ — 5 rtm (квадрат = что угодно)
    7️⃣7️⃣7️⃣ — 10 rtm

    *Внимание*: бот в тестовом режиме и ваши данные могут быть сброшены в любой момент!
    *НЕ ВНОСИТЕ НА СЧЕТ БОЛЬШЕ, ЧЕМ ГОТОВЫ ПОТЕРЯТЬ!!!*

    Убрать клавиатуру — /stop
    Показать клавиатуру, если пропала — /spin
    """

    welcome_text = """\
    *Добро пожаловать в наше виртуальное казино!*
    У вас пока нет rtm на счете. Чтобы это исправить отправьте rtm на адрес `{address}`
    """
    if pot > 0:
        await message.answer(dedent(start_text).format(pot=pot))
        await message.answer(dedent(rules), reply_markup=get_spin_keyboard())
    else:
        await message.answer(dedent(welcome_text).format(address=address))
        await message.answer(dedent(rules))


async def cmd_stop(message: Message):
    await message.answer(
        "Клавиатура удалена. Начать заново: /start, вернуть клавиатуру и продолжить: /spin",
        reply_markup=ReplyKeyboardRemove()
    )


async def cmd_stat(message: Message):
    user = DB_get(message.from_user.id)
    out_add = user.out_address()
    stat_text = """\
        На счету: {pot}
        К выводу: {out}
        Адресс для вывода: 
        {out_address}
        Адрес для пополнения:
        `{address}`"""
    await message.answer(
        dedent(stat_text).format(pot=user.pot(),
                                 out=user.request_pay(),
                                 out_address=out_add if out_add is not None else '*Не задан*',
                                 address=user.address()
                                 )
                        )


def register_default_commands(router: Router):
    flags = {"throttling_key": "default"}
    router.message.register(cmd_start, Command(commands="start"), flags=flags)
    router.message.register(cmd_stop, Command(commands="stop"), flags=flags)
    router.message.register(cmd_stat, Command(commands="stat"), flags=flags)
