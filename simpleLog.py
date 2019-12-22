from datetime import date, datetime


def log_info(message):
    print(f'{_date()} {c.BOLD}{c.OKBLUE}[INFO]{c.ENDC}      {message}')


def log_critical(message):
    print(f'{_date()} {c.BOLD}{c.FAIL}[CRITICAL]{c.ENDC}  {message}')


def _date():
    return str(datetime.now().strftime("%a %d %b %X"))



class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'