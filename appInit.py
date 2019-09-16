import os
import sys

import appPaths
import yaml

from distutils.dir_util import copy_tree


class AppConfig:
    app_id: int
    api_hash: str
    phone: str
    database_encryption_key: str
    tdlib_verbosity: int
    update_interval: int


def load_configuration() -> AppConfig:

    if not os.path.isfile(appPaths.config_yaml_path):
        print(f"{appPaths.config_yaml_path} does not exist")
        sys.exit(1)

    if not os.path.isdir(appPaths.tdlib_dir_path):
        print(f"{appPaths.tdlib_dir_path} does not exist")
        sys.exit(1)

    config_dict = load_config_file()
    app_config = AppConfig()
    app_config.app_id = int(config_dict['api_id'])
    app_config.api_hash = config_dict['api_hash']
    app_config.phone = config_dict['phone']
    app_config.database_encryption_key = config_dict['database_encryption_key']
    app_config.tdlib_verbosity = int(config_dict['tdlib_verbosity'])
    app_config.update_interval = int(config_dict['update_interval'])
    return app_config


def load_config_file() -> dict:
    with open(appPaths.config_yaml_path) as config_file:
        content = config_file.read()
        return yaml.load(content, Loader=yaml.BaseLoader)


def copy_tdlib_cache():
    copy_tree(appPaths.tdlib_dir_path, '/tmp/.tdlib_files/')