import os
import pytz
import datetime
from config import TIME_ZONE
from termcolor import colored


def get_now_datetime_str():
    now = datetime.datetime.now(pytz.timezone(TIME_ZONE))
    return now.strftime('%Y-%m-%d__%H-%M-%S')


def remove_temp_files(file_name):
    try:
        os.remove(file_name)
        print(colored("\U0001F44D File deleted!", "green"))
    except FileNotFoundError:
        pass
