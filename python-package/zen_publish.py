import click

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

    shutil.make_archive(".", "zip", ".")
    upload_file['zip_file'] = open(f"{path}.zip", "rb")

    data['access_key'] = zen_data.get("key")
    data['secret_key'] = zen_data.get("secret")

    r = requests.post( f"{zen_data['url']}publish/report", files=upload_file, data=data)
    os.remove(f"{path}.zip")
    if r.status_code != 200:
        print(r.status_code)
        raise UsageError(r.text)
    else:
        config['id'] = str(r.json()["id"])
        with open("config.yml".format(base_path), "w") as f:
            yaml.dump(config, f)

    os.chdir(old_path)

    return "publish report"

#
# def _get_encryption_key():
#     base_path = os.path.expanduser("~")
#
#     with open(f"{base_path}/.zen/setting.yml", "w") as f:
#         data = yaml.safe_load(f)
#
#     secret = data["secret"]
#     return base64.decode(secret)

@click.group()
def cli():
    pass


@click.command()
@click.option('--key', prompt='what is your access key?', help='What is your access key?')
@click.option('--secret', prompt='what is your secret key?', help='What is your secret key?')
@click.option('--url', prompt='what is zen report url?', help='what is zen report url?')
def create(key, secret, url):
    return _create(key, secret, url)


@click.command()
@click.option('--key')
@click.option('--secret')
@click.option('--url')
def create_s(key, secret, url):
    return _create(key, secret, url)


@click.command()
@click.option('--key', prompt='what is your access key?', help='What is your access key?')
@click.option('--secret', prompt='what is your secret key?', help='What is your secret key?')
def update(key, secret):
    return _update(key, secret)


@click.command()
@click.option('--key')
@click.option('--secret')
def update_s(key, secret):
    return _update(key, secret)


@click.command()
@click.option('--path', default=os.getcwd(), help="folder to look into")
def publish(path):
    return _publish(path)


@click.command()
@click.option('--path')
def publish_s(path):
    return _publish(path)



cli.add_command(update)
cli.add_command(update_s)
cli.add_command(create)
cli.add_command(create_s)
cli.add_command(publish)
cli.add_command(publish_s)
# zen.add_command(get_encryption_key)

if __name__ == '__main__':
    cli()
