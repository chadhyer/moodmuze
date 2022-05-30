from pathlib import Path
from os import getenv
import logging

#### Define logging
LOG_LEVEL = 1
LOG_FILE = Path('general.log')
if str(LOG_LEVEL).upper() == 'DEBUG' or LOG_LEVEL == 1:
    log_level = 'DEBUG'
elif str(LOG_LEVEL).upper() == 'INFO' or LOG_LEVEL == 2:
    log_level = 'INFO'
elif str(LOG_LEVEL).upper() == 'WARN' or LOG_LEVEL == 3:
    log_level = 'WARN'
elif str(LOG_LEVEL).upper() == 'ERROR' or LOG_LEVEL == 4:
    log_level = 'ERROR'
elif str(LOG_LEVEL).upper() == 'CRITICAL' or LOG_LEVEL == 5:
    log_level = 'CRITICAL'
logging.basicConfig(filename=LOG_FILE, level=log_level)

BRIDGE_IP = '10.0.0.10'

PROXY = {
  'http': 'socks5://127.0.0.1:8888',
  'https': 'socks5://127.0.0.1:8888',
}

AUTH_KEY = getenv('BRIDGE_KEY', 'testkey')
AUTH_TOKEN = 'http://' + BRIDGE_IP + '/api/' + AUTH_KEY

ENCODING = 'utf-8'
