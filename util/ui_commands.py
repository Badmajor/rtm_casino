from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    commands = [
            BotCommand(command="start", description="Перезапустить казино"),
            BotCommand(command="spin", description="Сделать бросок"),
            BotCommand(command="stop", description="Убрать клавиатуру"),
            BotCommand(command="stat", description="Показать статистику"),
            BotCommand(command="withdraw", description="Запросить вывод"),
            BotCommand(command="address", description="Указать адрес для вывода")
        ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
