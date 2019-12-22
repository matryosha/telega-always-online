from datetime import date, datetime


def log_info(message):
    print(_date() + " [INFO]      " + message)


def log_critical(message):
    print(_date() + " [CRITICAL]  " + message)


def _date():
    return str(datetime.now().strftime("%a %d %b %X"))
