#! /bin/python3
import click

from .bot import InfinitumBot
from .core.config import Config, dump_config
from . import setup

@click.group()
def cli():
    pass


@cli.command()
def initdb():
    click.echo("To Be Done..")


@cli.command()
@click.option('--bot', '-b', multiple=True, type=str, help="To specify which bot from the config"\
              "should be started. Multiple bots are possible. If only one is specified in the"\
              "config this parameter can be omitted")
@click.argument('config_path', type=click.Path(exists=True, readable=True, dir_okay=False,
                                          file_okay=True, allow_dash=False))
def run_bot(bot, config_path):
    click.echo(bot)
    click.echo(config_path)
    config = setup(config_path)
    dump_config(config)


if __name__ == '__main__':
    cli()
