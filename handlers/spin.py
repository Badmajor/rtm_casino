from asyncio import sleep
from textwrap import dedent

from aiogram import Router
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message

from Classes.Class_db import DB_get
from data.const import STICKER_FAIL, SPIN_TEXT, THROTTLE_TIME_SPIN, SPIN_TEXT_5, SPIN_TEXT_10
from keyboards.spin_keyboard import get_spin_keyboard
from util.balance import check_balance
from util.db_into import new_pot, registration
from util.dice_check import get_combo_data


async def cmd_spin(message: Message):
    user_id = message.from_user.id
    await check_balance(user_id)
    user = DB_get(user_id)
    user_score = user.pot()
    user_address = user.address()
    if user_score is None:
        await registration(user_id)
        user = DB_get(user_id)
        user_score = user.pot()

    if user_score < 1:
        await message.answer_sticker(sticker=STICKER_FAIL)
        await message.answer(
            "Ваш баланс равен нулю. Вы можете смириться с судьбой и продолжить жить своей жизнью, "
            f"а можете пополнить баланс, адрес вашего кошелька для пополнения: `{user_address}`"
        )
        return

    answer_text_template = """\
        Ваша комбинация: 
        {combo_text}.
        {win_or_lose_text} Ваш счёт: {new_score} rtm.
        """

    # Отправка дайса пользователю
    msg = await message.answer_dice(emoji="🎰", reply_markup=get_spin_keyboard())

    # Получение информации о дайсе
    score_change, combo_text = get_combo_data(msg.dice.value)
    score_change = score_change[0]
    if score_change < 1:
        win_or_lose_text = "К сожалению, вы не выиграли."
    else:
        win_or_lose_text = f"Вы выиграли {score_change} очков!"

    # Обновление счёта
    new_score = user_score + score_change
    await new_pot(new_score, user_id)

    await sleep(THROTTLE_TIME_SPIN)
    await msg.reply(
        dedent(answer_text_template).format(
            combo_text=combo_text,
            dice_value=msg.dice.value,
            win_or_lose_text=win_or_lose_text,
            new_score=new_score
        )
    )


async def cmd_spin_5(message: Message):
    user_id = message.from_user.id
    await check_balance(user_id)
    user = DB_get(user_id)
    user_score = user.pot()
    user_address = user.address()
    if user_score is None:
        await registration(user_id)
        user = DB_get(user_id)
        user_score = user.pot()

    if user_score < 5:
        await message.answer_sticker(sticker=STICKER_FAIL)
        await message.answer(
            "Ваш баланс меньше ставки. Вы можете выбрать размер ставки, "
            f"а можете пополнить баланс, адрес вашего кошелька для пополнения: `{user_address}`"
        )
        return

    answer_text_template = """\
        Ваша комбинация: 
        {combo_text}.
        {win_or_lose_text} Ваш счёт: {new_score} rtm.
        """

    # Отправка дайса пользователю
    msg = await message.answer_dice(emoji="🎰", reply_markup=get_spin_keyboard())

    # Получение информации о дайсе
    score_change, combo_text = get_combo_data(msg.dice.value)
    score_change = score_change[1]
    if score_change < 1:
        win_or_lose_text = "К сожалению, вы не выиграли."
    else:
        win_or_lose_text = f"Вы выиграли {score_change} очков!"

    # Обновление счёта
    new_score = user_score + score_change
    await new_pot(new_score, user_id)

    await sleep(THROTTLE_TIME_SPIN)
    await msg.reply(
        dedent(answer_text_template).format(
            combo_text=combo_text,
            dice_value=msg.dice.value,
            win_or_lose_text=win_or_lose_text,
            new_score=new_score
        )
    )


async def cmd_spin_10(message: Message):
    user_id = message.from_user.id
    await check_balance(user_id)
    user = DB_get(user_id)
    user_score = user.pot()
    user_address = user.address()
    if user_score is None:
        await registration(user_id)
        user = DB_get(user_id)
        user_score = user.pot()

    if user_score < 10:
        await message.answer_sticker(sticker=STICKER_FAIL)
        await message.answer(
            "Ваш баланс меньше ставки. Вы можете выбрать размер ставки, "
            f"а можете пополнить баланс, адрес вашего кошелька для пополнения: `{user_address}`"
        )
        return

    answer_text_template = """\
        Ваша комбинация: 
        {combo_text}.
        {win_or_lose_text} Ваш счёт: {new_score} rtm.
        """

    # Отправка дайса пользователю
    msg = await message.answer_dice(emoji="🎰", reply_markup=get_spin_keyboard())

    # Получение информации о дайсе
    score_change, combo_text = get_combo_data(msg.dice.value)
    score_change = score_change[2]
    if score_change < 1:
        win_or_lose_text = "К сожалению, вы не выиграли."
    else:
        win_or_lose_text = f"Вы выиграли {score_change} очков!"

    # Обновление счёта
    new_score = user_score + score_change
    await new_pot(new_score, user_id)

    await sleep(THROTTLE_TIME_SPIN)
    await msg.reply(
        dedent(answer_text_template).format(
            combo_text=combo_text,
            dice_value=msg.dice.value,
            win_or_lose_text=win_or_lose_text,
            new_score=new_score
        )
    )


def register_spin_command(router: Router):
    flags = {"throttling_key": "spin"}
    router.message.register(cmd_spin, Command(commands="spin"), flags=flags)
    router.message.register(cmd_spin, Text(text=SPIN_TEXT), flags=flags)
    router.message.register(cmd_spin_5, Text(text=SPIN_TEXT_5), flags=flags)
    router.message.register(cmd_spin_10, Text(text=SPIN_TEXT_10), flags=flags)
