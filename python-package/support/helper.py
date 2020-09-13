import copy
import os
import shutil

import requests
import yaml
from click import UsageError


def _create(key, secret, url):
    base_path = os.path.expanduser("~")
    if not os.path.isdir(f"{base_path}/.zen"):
        os.mkdir(f"{base_path}/.zen")

    my_dict = {
        "key": key,
        "secret": secret,
        "url": url
    }
    with open(f"{base_path}/.zen/setting.yml", "w") as f:
        yaml.dump(my_dict, f)

    return "created value"


def _update(key, secret):
    base_path = os.path.expanduser("~")
    if not os.path.isdir(f"{base_path}/.zen"):
        raise UsageError("zen report data is not present please use zen create command")
    with open(f"{base_path}/.zen/setting.yml", "r") as f:
        data = yaml.safe_load(f)
    data['key'] = key
    data['secret'] = secret

    with open(f"{base_path}/.zen/setting.yml", "w") as f:
        yaml.dump(data, f)

    return "updated value"


def _publish(path):
    old_path = os.getcwd()
    if path != old_path:
        os.chdir(path)
    base_path = os.path.expanduser("~")
    current = path
    files = os.listdir(current)
    present_config = any([True for file_ in files if 'config.yml' == file_])

    if not present_config:
        raise UsageError("config.yml file is not present")

    with open(f"{base_path}/.zen/setting.yml", "r") as f:
        zen_data = yaml.safe_load(f)

    if not os.path.isfile(f"{base_path}/.zen/setting.yml"):
        raise UsageError("zen report data is not present please use zen create command")

    upload_file = {}
    for file_ in files:
        if file_ == 'config.yml':
            with open("config.yml".format(base_path), "r") as f:
                data = yaml.safe_load(f)
            break_list = ['title', 'type', 'language']
            for b in break_list:
                if b not in data.keys():
                    raise UsageError(f"{b.capitalize()} is not provided in config")
            config = copy.deepcopy(data)

    shutil.make_archive("..", "zip", ".")
    upload_file['zip_file'] = open(f"{path}.zip", "rb")

    data['access_key'] = zen_data.get("key")
    data['secret_key'] = zen_data.get("secret")
    r = requests.post(f"{zen_data['url']}/api/publish/", files=upload_file, data=data)
    if r.status_code != 200:
        print(r.status_code)
        raise UsageError(r.text)
    else:
        config['id'] = str(r.json()["id"])
        with open("config.yml".format(base_path), "w") as f:
            yaml.dump(config, f)
    os.chdir(old_path)

    return "publish report"
