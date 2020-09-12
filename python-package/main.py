import click
import os
import yaml
from click import UsageError
import requests
import copy
import shutil

@click.group()
def zen():
    pass


@click.command()
@click.option('--key', prompt='what is your access key?', help='What is your access key?')
@click.option('--secret', prompt='what is your secret key?', help='What is your secret key?')
@click.option('--url', prompt='what is zen report url?', help='what is zen report url?')
def create(key, secret, url):
    base_path = os.path.expanduser("~")
    if not os.path.isdir("{0}/.zen_report".format(base_path)):
        os.mkdir("{0}/.zen_report".format(base_path))

    my_dict = {
        "key": key,
        "secret": secret,
        "url": url
    }
    with open("{0}/.zen_report/setting.yml".format(base_path), "w") as f:
        yaml.dump(my_dict, f)

@click.command()
@click.option('--key', prompt='what is your access key?', help='What is your access key?')
@click.option('--secret', prompt='what is your secret key?', help='What is your secret key?')
def update(key, secret):
    base_path = os.path.expanduser("~")
    if not os.path.isdir("{0}/.zen_report".format(base_path)):
        raise UsageError("zen report data is not present please use zen create command")
    with open("{0}/.zen_report/setting.yml".format(base_path), "r") as f:
        data = yaml.safe_load(f)
    data['key'] = key
    data['secret'] = secret

    with open("{0}/.zen_report/setting.yml".format(base_path), "w") as f:
        yaml.dump(data, f)

@click.command()
@click.option('--path', default=os.getcwd(), help="folder to look into")
def publish(path):
    if path !=  os.getcwd():
        os.chdir(path)
    base_path = os.path.expanduser("~")
    current = path
    files = os.listdir(current)
    present_config = any([True for file_ in files if 'config.yml' == file_])

    if not present_config:
        raise UsageError("config.yml file is not present")

    with open(f"{base_path}/.zen_report/setting.yml", "r") as f:
        zen_data = yaml.safe_load(f)

    if not os.path.isfile(f"{base_path}/.zen_report/setting.yml"):
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

zen.add_command(update)
zen.add_command(create)
zen.add_command(publish)

if __name__ == '__main__':
    zen()
