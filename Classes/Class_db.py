import pymysql

from config import load_config


class DB_get:
    def __init__(self, user_id):
        config = load_config()
        db = config.database
        connect = pymysql.connect(
            host=db.server,
            user=db.login,
            password=db.password,
            database=db.name,
            cursorclass=pymysql.cursors.DictCursor)
        with connect.cursor() as cursor:
            command = \
                "SELECT `pot`, `out_pot`, `request_pay`, `address`, `received`, `out_address` FROM `users` WHERE " \
                "`user_id`=%s "
            cursor.execute(command, user_id)
            self.data = cursor.fetchone()
        connect.close()

    def pot(self):
        return self.data.get('pot')

    def out_pot(self):
        return self.data.get('out_pot')

    def request_pay(self):
        return self.data.get('request_pay')

    def address(self):
        return self.data.get('address')

    def rec(self):
        return self.data.get('received')

    def out_address(self):
        return self.data.get('out_address')

    def status(self):
        return self.data is None
