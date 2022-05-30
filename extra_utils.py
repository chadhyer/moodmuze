from re import search
import logging


def get_key_value_pair(file_path):
    dictionary = {}
    with open(file_path) as file:
        for line in file:
            if search('=', line) and not search('^#', line):
                dictionary[line.split('=')[0]] = line.split('=')[1].strip()
    return dictionary


def read_file(file_path):
  with open('./README.md', 'r') as file:
    print(file.read())


def log_message(level, message):
    if level == 1:
        logging.debug(message)
    elif level == 2:
        logging.info(message)
    elif level == 3:
        logging.warn(message)
    elif level == 4:
        logging.error(message)
    elif level == 5:
        logging.critical(message)

