import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from magic_filter import F

from config import Config, load_config
from handlers.default_commands import register_default_commands
from handlers.spin import register_spin_command
from handlers.withdraw import register_withdraw_commands
from middlewares.throttling import ThrottlingMiddleware
from util.ui_commands import set_bot_commands


async def main():
    config: Config = load_config()
    bot = Bot(config.bot.token, parse_mode="Markdown")

    default_router = Router()

    default_router.message.filter(F.chat.type == "private")

    register_default_commands(default_router)
    register_spin_command(default_router)
    register_withdraw_commands(default_router)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(default_router)

    # Регистрация мидлвари для троттлинга
    dp.message.middleware(ThrottlingMiddleware())

    # Установка команд в интерфейсе
    await set_bot_commands(bot)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
