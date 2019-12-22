import appInit as AppInit
import simpleLog as Logger

from telegram.client import Telegram
from datetime import date, datetime

import time


def delete_api_message(chat_id: int, message_id: int, telegram: Telegram):
    delete_message_data = {
        '@type': 'deleteMessages',
        'chat_id': chat_id,
        'message_ids': [message_id]
    }
    res = telegram._send_data(delete_message_data)


def edit_api_message(chat_id: int, message_id: int, telegram: Telegram):
    edit_message_data = {
        '@type': 'editMessageText',
        'chat_id': chat_id,
        'message_id': message_id,
        'input_message_content': {
            '@type': 'inputMessageText',
            'text': {'@type': 'formattedText', 'text': f'api_test_{datetime.now()}'},
        },
    }
    res = telegram._send_data(edit_message_data)
    res.wait()


def send_api_test_message(telegram: Telegram, chat_id: int):
    Logger.log_info("Send api message")
    api_message = f'api_test_{datetime.now()}'
    telegram.send_message(chat_id, api_message).wait()


def get_chat_history_data(message_id, chat_id):
    return {
        '@type': 'getChatHistory',
        'chat_id': chat_id,
        'from_message_id': message_id,
        'offset': 0,
        'limit': 1
    }


def do_shit(telegram: Telegram):
    # chats = telegram.get_chats(offset_order=2**63 - 1)

    me = telegram.get_me()
    me.wait()

    Logger.log_info("Getting saved messages chat id")
    saved_messages_chat_id: int = me.update['id']
    if type(saved_messages_chat_id) is not int or saved_messages_chat_id is "":
        Logger.log_critical("Saved messages chat id is empty")
        return False

    messages_list = []
    last_message_id = 0
    left = 10

    while left > 0:
        data = get_chat_history_data(last_message_id, saved_messages_chat_id)
        messages_response = telegram._send_data(data=data)
        messages_response.wait()

        if len(messages_response.update['messages']) is 0:
            break

        last_message_dict = messages_response.update['messages'][0]
        messages_list.append(last_message_dict)
        last_message_id = last_message_dict['id']
        left = left - 1
        # print(last_message_dict)

    Logger.log_info("Got messages list. List length: " + str(len(messages_list)))

    api_test_message_dict = None
    for message_dict_data in messages_list:
        if message_dict_data['content']['@type'] != 'messageText':
            continue
        message_text: str = message_dict_data['content']['text']['text']
        if message_text.startswith('api_test'):
            api_test_message_dict = message_dict_data
            break
    if api_test_message_dict is None:
        send_api_test_message(telegram, saved_messages_chat_id)
    else:
        delete_api_message(saved_messages_chat_id, api_test_message_dict['id'], telegram)
        send_api_test_message(telegram, saved_messages_chat_id)

    return True


def init_telegram():
    t = Telegram(
        api_id=app_config.app_id,
        api_hash=app_config.api_hash,
        phone=app_config.phone,
        database_encryption_key=app_config.database_encryption_key,
        tdlib_verbosity=app_config.tdlib_verbosity
    )

    t.login()
    chats = t.get_chats()
    chats.wait()

    return t


def main_loop():
    try:
        while True:
            telegram = init_telegram()
            while do_shit(telegram):
                time.sleep(app_config.update_interval)
    except Exception as e:
        Logger.log_critical("Something when wrong. Exception message:")
        Logger.log_critical(e)
        main_loop()


if __name__ == '__main__':
    app_config = AppInit.load_configuration()
    AppInit.copy_tdlib_cache()

    main_loop()



