#!/usr/bin/env python
import click
from subprocess import run

@click.group()
def commands():
    pass

@click.group()
def db():
    pass

@click.group()
def api():
    pass

@click.command()
@click.option('-m', '--message', help='revision message')
def generate(message):
    if not message:
        message = input('Enter message: ')
    run(['alembic', 'revision', '--autogenerate', '-m', message])

@click.command()
@click.option('--sql', is_flag=True, help='show sql')
def upgrade(sql):
    command = ['alembic', 'upgrade', 'head']
    if sql:
        command.append('--sql')
    run(command)

db.add_command(generate)
db.add_command(upgrade)
commands.add_command(db)

@click.command()
def test():
    run(['sam', 'build', '--use-container'])
    run(['sam', 'local', 'invoke', 'EmailFunction', '-e', 'events/send_email.json'])

@click.command()
@click.option('--dbengine', help='Production DB engine')
def deploy(dbengine):
    if not dbengine:
        dbengine = input('Enter database (engine://user:password@url/dbname): ')
    run(['sam', 'deploy', '--parameter-overrides', f'DB_ENGINE={dbengine}'])


api.add_command(test)
api.add_command(deploy)
commands.add_command(api)

if __name__ == '__main__':
    commands()
