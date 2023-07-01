import time
from steampy.client import SteamClient, Asset
from steampy.utils import GameOptions
from steampy.exceptions import InvalidCredentials
from urllib3 import disable_warnings
from sys import stderr
from loguru import logger
import json
import os
import pickle

maFiles_path = './maFiles/'
maFiles = os.listdir(maFiles_path)
with open('settings.json', 'r') as f:
    main_acc = json.loads(f.read())
with open('accounts.txt', 'r') as f:
    accounts = {line.split()[0]: line.split()[1] for line in f}

disable_warnings()
logger.remove()
logger.add(stderr, format="<blink>{time:HH:mm:ss}</blink> | <level>{level: <4}</level> | <cyan>{line: <2}</cyan> - <light-white>{message}</light-white>", level='DEBUG')

def get_login_from_mafile(mafile_path):
    with open(mafile_path, 'r') as mafile:
        return json.loads(mafile.read())['account_name']


def main():
    for maFile in maFiles:
        mafile_path = maFiles_path + maFile
        login = get_login_from_mafile(mafile_path)
        if login not in accounts:
            continue
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
                    time.sleep(45)
                rec_queue = client.get_recommendations_queue()
                if rec_queue.status_code != 200:
                    logger.warning(f'{login}: аккаунт еблан')
                    return
                rec_queue = rec_queue.json()['queue']
                for app_id in rec_queue:
                    status = client.watch_recommendation(app_id)
                    if status != 1:
                        logger.warning(status)
                        break
                    else:
                        # logger.info(f'{login}: просмотрена {rec_queue.index(app_id) + 1} рекомендация')
                        time.sleep(0.2)
                else:
                    logger.success(f'{login}: done')
            except (TypeError, AttributeError, InvalidCredentials) as error:
                logger.debug(f'{login}: {type(error).__name__}: {error}, повтор через 15 сек')
                time.sleep(15)
                claim()
        try:
            claim()
        except Exception as e:
            logger.warning(f'{login}: {type(e).__name__}: {e}')
        time.sleep(1)


if __name__ == '__main__':
    main()