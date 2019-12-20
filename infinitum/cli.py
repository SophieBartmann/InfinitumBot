#! /bin/python3
import click
import logging

from .bot import InfinitumBot
from .core.config import Config, sdump_config
from . import setup
from typing import List


def create_bot(botname: str, config: Config):
    logging.debug(f"Creating bot named '{botname}'..")
    bot_config = config.get_bot(botname)
    logging.debug(f"Config to be used:\n{sdump_config(bot_config)}")
    if not bot_config:
        logging.error("Could not create bot config")
        return None
    bot = InfinitumBot(bot_config)
    logging.debug("..Done")
    return bot


def start_bots(bots: List[InfinitumBot]):
    if len(bots) > 1:
        click.echo("Yet only a single bot can be run.")
        return
    if len(bots) == 0:
        click.echo("Please set up bots first.")
        return
    bots[0].run()


@click.group()
def cli():
    pass


@cli.command()
def initdb():
    click.echo("To Be Done..")


@cli.command()
@click.option('--botname', '-b', multiple=True, type=str, help="To specify which bot from the config"\
              "should be started. Multiple bots are possible. If only one is specified in the"\
              "config this parameter can be omitted")
@click.argument('config_path', type=click.Path(exists=True, readable=True, dir_okay=False,
                                          file_okay=True, allow_dash=False))
def run_bot(botname, config_path):
    click.echo(botname)
    click.echo(config_path)
    config = setup(config_path)
    bot_list = []
    if len(botname) > 0:
        if len(botname) > 1:
            click.echo("Running multiple bots at once is yet not supported.")
            return
        bot = create_bot(botname[0], config)
        if not bot:
            click.echo("Could not find config for bot '{botname[0]}'.")
            return
        bot_list.append(bot)
    elif len(config.bot_overview) > 1:
        click.echo("The config specifies more than one bot. Please use --botname to choose which"\
                   "to run.")
        return
    elif len(config.bot_overview) == 0:
        click.echo("The config does not specify a bot. Please fix your config.")
    else:
        name = config.bot_overview.pop()
        bot = create_bot(name, config)
        if not bot:
            click.echo(f"Could not create bot '{name}'. Please check the logs")
            return
        bot_list.append(bot)

    start_bots(bot_list)


if __name__ == '__main__':
    cli()
