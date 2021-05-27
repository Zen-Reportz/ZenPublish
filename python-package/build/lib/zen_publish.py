import click
import webbrowser
import copy
import os
import shutil
import requests
import oyaml as yaml
from click import UsageError
import time

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


def _publish(path, fresh, browser):
    old_path = os.getcwd()
    if path != old_path:
        os.chdir(path)
    base_path = os.path.expanduser("~")

    if not os.path.isfile(f"{base_path}/.zen/setting.yml"):
        raise UsageError("zen report data is not present please use zen create command")
    
    current = path
    files = os.listdir(current)
    present_config = any([True for file_ in files if 'config.yml' == file_])

    if not present_config:
        raise UsageError("config.yml file is not present")

    setting_path = base_path + "/.zen/setting.yml"
    
    with open(setting_path, "r") as myfile:
        zen_data = yaml.safe_load(myfile)


    upload_file = {}
    for file_ in files:
        if file_ == 'config.yml':
            with open("config.yml", "r") as f:
                data = yaml.safe_load(f)
            break_list = ['title', 'type', 'language']
            for b in break_list:
                if b not in data.keys():
                    raise UsageError(f"{b.capitalize()} is not provided in config")
            if fresh:
                data.pop('id', None)
                with open("config.yml".format(base_path), "w") as f:
                    yaml.dump(data, f)
            config = copy.deepcopy(data)
    type = config.get('type')

    shutil.make_archive(".", "zip", ".")
    upload_file['zip_file'] = open(f"{path}.zip", "rb")

    data['access_key'] = zen_data.get("key")
    data['secret_key'] = zen_data.get("secret")
    publish_url = zen_data['url']
    if publish_url[-1] != "/":
        publish_url = publish_url + "/"
    print(f"publishing document at {zen_data['url']}publish/report/")
    r = requests.post( f"{zen_data['url']}publish/report/", files=upload_file, data=data)
    os.remove(f"{path}.zip")
    if r.status_code != 200:
        if r.status_code == 402:
            print("You have used all reports, need to updagrade Zen Reportz")
        raise UsageError(r.text)
    else:
        response = r.json()["data"]
        time.sleep(10)
        report_id = str(response["id"])
        config['id'] = report_id
        with open("config.yml".format(base_path), "w") as f:
            yaml.dump(config, f)

        if len(response["workers"])> 0 :
            workerNames = ', '.join(response["workers"])
            print(f"following worker(s) are not present, please talk your admin {workerNames}")

        if len(response["worker_groups"])> 0 :
            worker_group = ', '.join(response["worker_groups"])
            print(f"following worker group(s) are not present, please talk your admin {worker_group}")

        url_to_open = publish_url + f'report-application/{report_id}?type={type}&open=true'

        if browser:
            webbrowser.open(url_to_open)

        os.chdir(old_path)

    return "publish report"

def _get_workers():
   
    base_path = os.path.expanduser("~")

    if not os.path.isfile(f"{base_path}/.zen/setting.yml"):
        raise UsageError("zen report data is not present please use zen create command")
    
    with open(f"{base_path}/.zen/setting.yml", "r") as f:
        zen_data = yaml.safe_load(f)

    data = {}
    data['access_key'] = zen_data.get("key")
    data['secret_key'] = zen_data.get("secret")
    r = requests.post( f"{zen_data['url']}api/external/get_worker/", data=data)
    if r.status_code != 200:
        raise UsageError(r.text)
    else:
        response = r.json()

        if response["data"] is None :
            print("no worker name present")
            return 0

        workerNames = ', '.join( d["name"] for d in response["data"])
        print(f" workers are {workerNames}")
        return 0


def _get_worker_groups():
   
    base_path = os.path.expanduser("~")

    if not os.path.isfile(f"{base_path}/.zen/setting.yml"):
        raise UsageError("zen report data is not present please use zen create command")
    
    with open(f"{base_path}/.zen/setting.yml", "r") as f:
        zen_data = yaml.safe_load(f)

    data = {}
    data['access_key'] = zen_data.get("key")
    data['secret_key'] = zen_data.get("secret")
    r = requests.post( f"{zen_data['url']}api/external/get_worker_group/", data=data)
    if r.status_code != 200:
        raise UsageError(r.text)
    else:
        response = r.json()
        if response["data"] is None :
            print("no worker group name present")

            return 0
        workerGroupNames = ', '.join( d["name"] for d in response["data"])
        print(f" worker group are {workerGroupNames}")
        return 0


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
@click.option('--key', prompt='what is your access key?', help='What is your access key?')
@click.option('--secret', prompt='what is your secret key?', help='What is your secret key?')
def update(key, secret):
    return _update(key, secret)

@click.command()
@click.option('--path', default=os.getcwd(), help="folder to look into")
@click.option('--fresh', '-f', is_flag=True,  help="run as fresh report")
@click.option('--browser','-b', is_flag=True, help="Want to open window")
def publish(path, fresh, browser):
    return _publish(path, fresh, browser)

@click.command()
def get_workers():
    return _get_workers()

@click.command()
def get_worker_group():
    return _get_worker_groups()



cli.add_command(update)
cli.add_command(create)
cli.add_command(publish)
cli.add_command(get_workers)
cli.add_command(get_worker_group)

# zen.add_command(get_encryption_key)

if __name__ == '__main__':
    cli()
