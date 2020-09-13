import os

import click
from support import helper


@click.group()
def zen():
    pass


@click.command()
@click.option('--key', prompt='what is your access key?', help='What is your access key?')
@click.option('--secret', prompt='what is your secret key?', help='What is your secret key?')
@click.option('--url', prompt='what is zen report url?', help='what is zen report url?')
def create(key, secret, url):
    return helper._create(key, secret, url)


@click.command()
@click.option('--key')
@click.option('--secret')
@click.option('--url')
def create_s(key, secret, url):
    return helper._create(key, secret, url)


@click.command()
@click.option('--key', prompt='what is your access key?', help='What is your access key?')
@click.option('--secret', prompt='what is your secret key?', help='What is your secret key?')
def update(key, secret):
    return helper._update(key, secret)


@click.command()
@click.option('--key')
@click.option('--secret')
def update_s(key, secret):
    return helper._update(key, secret)


@click.command()
@click.option('--path', default=os.getcwd(), help="folder to look into")
def publish(path):
    return helper._publish(path)


@click.command()
@click.option('--path')
def publish_s(path):
    return helper._publish(path)


zen.add_command(update)
zen.add_command(update_s)
zen.add_command(create)
zen.add_command(create_s)
zen.add_command(publish)
zen.add_command(publish_s)

if __name__ == '__main__':
    zen()
