import requests

from Classes.Class_db import DB_get
from util.db_into import new_pot, new_rec


async def check_balance(user_id: int):
    user = DB_get(user_id)
    old_rec = user.rec()
    pot = user.pot()
    balance_data = requests.get(f'https://explorer.raptoreum.com/api/getaddressbalance?address={user.address()}')
    rec = balance_data.json()[user.address()]['received'] // 100000000
    if old_rec != rec:
        pot += rec - old_rec
        await new_pot(pot, user_id)
        await new_rec(rec, user_id)
        print(f'депозит обработан{pot}')
