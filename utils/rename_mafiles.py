from urllib3 import disable_warnings
from sys import stderr
from loguru import logger
import json
import os

maFiles_path = '../maFiles/'
maFiles = os.listdir(maFiles_path)

disable_warnings()
logger.remove()
logger.add(stderr, format="<blink>{time:HH:mm:ss}</blink> | <level>{level: <4}</level> | <cyan>{line: <2}</cyan> - <light-white>{message}</light-white>", level='DEBUG')


class EmptyInventory(Exception): pass


def get_login_from_mafile(mafile_path):
    with open(mafile_path, 'r') as mafile:
        return json.loads(mafile.read())['account_name']


for maFile in maFiles:
    try:
        login = get_login_from_mafile(maFiles_path + maFile)
        os.rename(maFiles_path + maFile, maFiles_path + login + '.maFile')
        logger.success(f'{maFile} was renamed to {login + ".maFile"}')
    except Exception as e:
        logger.error(f'{maFile}: {type(e).__name__}: {e}')
