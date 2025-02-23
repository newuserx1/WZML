from logging import FileHandler, StreamHandler, INFO, basicConfig, error as log_error, info as log_info
from os import path as ospath, environ, remove as osremove
from subprocess import run as srun, call as scall
from pkg_resources import working_set
from requests import get as rget
from dotenv import load_dotenv
from pymongo import MongoClient

if ospath.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[FileHandler('log.txt'), StreamHandler()],
                    level=INFO)

load_dotenv('config.env', override=True)

try:
    if bool(environ.get('_____REMOVE_THIS_LINE_____')):
        log_error('The README.md file there to be read! Exiting now!')
        exit()
except:
    pass

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = int(BOT_TOKEN.split(':', 1)[0])

DATABASE_URL = environ.get('DATABASE_URL', '')
if len(DATABASE_URL) == 0:
    DATABASE_URL = None

if DATABASE_URL is not None:
    conn = MongoClient(DATABASE_URL)
    db = conn.mltb
    if config_dict := db.settings.config.find_one({'_id': bot_id}):  #retrun config dict (all env vars)
        environ['UPSTREAM_REPO'] = config_dict['UPSTREAM_REPO']
        environ['UPSTREAM_BRANCH'] = config_dict['UPSTREAM_BRANCH']
        environ['UPDATE_PACKAGES'] = config_dict.get('UPDATE_PACKAGES', 'False')
    conn.close()

UPDATE_PACKAGES = environ.get('UPDATE_PACKAGES', 'False')
if UPDATE_PACKAGES.lower() == 'true':
    packages = [dist.project_name for dist in working_set]
    scall("pip install " + ' '.join(packages), shell=True)

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', 'https://github.com/newuserx1/WZML')
if len(UPSTREAM_REPO) == 0:
   UPSTREAM_REPO = None

UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', 'master')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'master'


