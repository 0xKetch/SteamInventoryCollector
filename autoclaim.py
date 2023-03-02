import time
from steampy.client import SteamClient, Asset
from steampy.utils import GameOptions
from urllib3 import disable_warnings
from sys import stderr
from loguru import logger
from pyrogram import Client, filters
import json
import os
import pickle

with open('settings.json', 'r') as f:
    main_acc = json.loads(f.read())

app = Client('telegram', api_id=main_acc['telegram_api_id'], api_hash=main_acc['telegram_api_hash'], bot_token=main_acc['telegram_bot_token'])  # main acc

games = [GameOptions.CS, ]  # GameOptions.STEAM
maFiles_path = './maFiles/'
maFiles = os.listdir(maFiles_path)
with open('accounts.txt', 'r') as f:
    accounts = {line.split()[0]: line.split()[1] for line in f}

disable_warnings()
logger.remove()
logger.add(stderr, format="<blink>{time:HH:mm:ss}</blink> | <level>{level: <4}</level> | <cyan>{line: <2}</cyan> - <light-white>{message}</light-white>", level='DEBUG')

if not os.path.exists('cookies'):
    os.mkdir('cookies')


class EmptyInventory(Exception): pass


def get_tradable_items(items, game: GameOptions = GameOptions.CS):
    tradable_items = []
    for item in items:
        if items[item]['tradable']:
            tradable_items.append(Asset(item, game))
    return tradable_items


def main(login):
    mafile_path = maFiles_path + login + '.maFile'
    password = accounts[login]

    def claim():
        try:
            client = None
            session_alive = False
            if os.path.isfile(f'cookies/{login}.pkl'):
                with open(f'cookies/{login}.pkl', 'rb') as pkl:
                    client = pickle.load(pkl)
                session_alive = client.is_session_alive()
            if not session_alive:
                client = SteamClient(main_acc['steam_api_key'])
                client.login(login, password, mafile_path)
                with open(f'cookies/{login}.pkl', 'wb') as pkl:
                    pickle.dump(client, pkl)
                time.sleep(60)
            my_items = []
            for game in games:
                my_items.extend(get_tradable_items(client.get_my_inventory(game, merge=True), game))
            if len(my_items) == 0:
                logger.info(f'{login}: пустой инвентарь')
                raise EmptyInventory
            trade_offer_id = client.make_offer_with_url(my_items, [], main_acc['trade_url'])['tradeofferid']
            main_client.accept_trade_offer(trade_offer_id)
            logger.success(f'{login}: залутал {len(my_items)} {"items" if len(my_items) > 1 else "item"}')
        except (TypeError, AttributeError) as error:
            logger.debug(f'{login}: {type(error).__name__}: {error}, повтор через 5 сек')
            time.sleep(5)
            claim()
    try:
        claim()
    except EmptyInventory:
        pass
    except Exception as e:
        if type(e).__name__ == 'KeyError' and e.__str__() == "'tradeofferid'":
            logger.warning(f'{login}: дебил у тебя инвентарь забит либо 15 дней с гуарда еще не прошло')
        else:
            logger.warning(f'{login}: {type(e).__name__}: {e}')
    time.sleep(0.5)


@app.on_message(filters.chat(main_acc['telegram_chat_id']))
def massage_handler(client, message):
    login = message.text.split()[0]
    if login in accounts:
        main(login)


if __name__ == '__main__':
    main_session_alive = False
    if os.path.isfile(f'cookies/{main_acc["login"]}.pkl'):
        with open(f'cookies/{main_acc["login"]}.pkl', 'rb') as pkl:
            main_client = pickle.load(pkl)
        main_session_alive = main_client.is_session_alive()
    if not main_session_alive:
        main_client = SteamClient(main_acc['steam_api_key'])
        main_client.login(main_acc['login'], main_acc['password'], main_acc['maFile'])
        with open(f'cookies/{main_acc["login"]}.pkl', 'wb') as pkl:
            pickle.dump(main_client, pkl)
        time.sleep(60)
    app.run()
