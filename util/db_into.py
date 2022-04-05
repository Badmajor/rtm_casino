import pymysql

from config import load_config

config = load_config()
db = config.database
connect = pymysql.connect(
        host=db.server,
        user=db.login,
        password=db.password,
        database=db.name,
        cursorclass=pymysql.cursors.DictCursor)


async def get_address() -> str:
    connect.close()
    connect.connect()
    with connect.cursor() as cursor:
        command = "SELECT COUNT(*) FROM `users`"
        cursor.execute(command)
        count_u = cursor.fetchone().get('COUNT(*)')
        command = "SELECT `address` FROM `addresses` WHERE `id`=%s "
        cursor.execute(command, count_u + 1)
        address = cursor.fetchone()
        return address.get('address')


async def new_pot(pot: int, user_id: int):
    connect.close()
    connect.connect()
    with connect.cursor() as cursor:
        command = "UPDATE `users` SET `pot`=%s WHERE `user_id`=%s"
        cursor.execute(command, [pot, user_id])
        connect.commit()


async def new_request_pay(request_pay: int, user_id: int):
    connect.close()
    connect.connect()
    with connect.cursor() as cursor:
        command = "UPDATE `users` SET `request_pay`=%s WHERE `user_id`=%s"
        cursor.execute(command, [request_pay, user_id])
        connect.commit()


async def new_out_address(out_address: str, user_id: int):
    connect.close()
    connect.connect()
    with connect.cursor() as cursor:
        command = "UPDATE `users` SET `out_address`=%s WHERE `user_id`=%s"
        cursor.execute(command, [out_address, user_id])
        connect.commit()


async def registration(user_id: int):
    address = await get_address()
    connect.close()
    connect.connect()
    with connect.cursor() as cursor:
        command = "INSERT INTO `users`(`user_id`, `pot`, `out_pot`, `request_pay`, `address`, `received`) " \
                  "VALUE (%s, %s, %s, %s, %s, %s)"
        cursor.execute(command, (user_id, 0, 0, 0, address, 0))
        connect.commit()


async def new_rec(rec: int, user_id: int):
    connect.close()
    connect.connect()
    with connect.cursor() as cursor:
        command = "UPDATE `users` SET `received`=%s WHERE `user_id`=%s"
        cursor.execute(command, [rec, user_id])
        connect.commit()


"""def add_address():
    """"""Добавляет список адресов в БД""""""
    with connect.cursor() as cursor:
        for ad in list_address:
            command = "INSERT INTO `addresses`(`address`) VALUE (%s)"
            cursor.execute(command, ad)
            connect.commit()"""
