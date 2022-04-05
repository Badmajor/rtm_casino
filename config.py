from dataclasses import dataclass
import os

from environs import Env

env = Env()
env.read_env()


@dataclass
class TgBot:
    token: str


@dataclass
class DataBase:
    name: str
    login: str
    password: str
    server: str


@dataclass
class Webhook:
    host: str
    path: str
    url: str


@dataclass
class WebApp:
    host: str
    port: str


@dataclass
class Config:
    bot: TgBot
    database: DataBase
    webhook: Webhook
    webapp: WebApp


def load_config() -> Config:
    return Config(
        bot=TgBot(
            token=os.environ["BOT_TOKEN"]
        ),
        database=DataBase(
            name=os.environ["DB_NAME"],
            login=os.environ["DB_LOGIN"],
            password=os.environ["DB_PASSWORD"],
            server=os.environ["DB_SERVER"]
        ),
        webhook=Webhook(
            host=os.environ["WEBHOOK_HOST"],
            path=os.environ["WEBHOOK_PATH"],
            url=os.environ["WEBHOOK_URL"]
        ),
        webapp=WebApp(
            host=os.environ["WEBAPP_HOST"],
            port=os.environ["WEBAPP_PORT"]
        )
    )
