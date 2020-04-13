#! /bin/python3

import logging
import random
import re
from typing import Dict, Any

from infinitum import utils
from infinitum.bot import InfinitumBot
from infinitum.core.api import ModulePrototype, Command

COOKIES_PATH = "cookies"
DRINKS_PATH = "drinks"
FOOD_PATH = "food"


class Waitress(ModulePrototype):
    COOKIES_REGEX = r'^.*\.cookie.*$'
    COOKIES_EXAMPLE = '.cookie'
    COOKIES_HELP = 'Gibt dem Nutzer einen zufälligen Keks.'

    DRINK_REGEX = r'^.*\.drink.*$'
    DRINK_EXAMPLE = '.drink'
    DRINK_HELP = 'Gibt dem Nutzer einen zufälligen Drink'

    FOOD_REGEX = r'^.*\.food.*$'
    FOOD_EXAMPLE = '.food'
    FOOD_HELP = 'Gibt dem Nutzer zufälliges Essem'

    def __init__(self):
        self.cookies = []
        self.drinks = []
        self.food = []
        self._config = None
        cookies_cmd = Command.create_msg_command(Waitress.COOKIES_REGEX, Waitress.COOKIES_HELP,
                                                 Waitress.COOKIES_EXAMPLE, self)
        food_cmd = Command.create_msg_command(Waitress.FOOD_REGEX, Waitress.FOOD_HELP, Waitress.FOOD_EXAMPLE,
                                              self)
        drink_cmd = Command.create_msg_command(Waitress.DRINK_REGEX, Waitress.DRINK_HELP, Waitress.DRINK_EXAMPLE,
                                               self)
        self._command_map = {Waitress.COOKIES_REGEX: cookies_cmd,
                             Waitress.FOOD_REGEX: food_cmd,
                             Waitress.DRINK_REGEX: drink_cmd}

    def setup(self, bot: InfinitumBot, config: Dict[str, Any]) -> None:
        self._config = config
        self.cookies = utils.read_list(config[COOKIES_PATH])
        logging.debug(f"Successfully loaded {len(self.cookies)} cookies")
        self.drinks = utils.read_list(config[DRINKS_PATH])
        logging.debug(f"Successfully loaded {len(self.drinks)} drinks")
        self.food = utils.read_list((config[FOOD_PATH]))
        logging.debug(f"Successfully loaded {len(self.food)} dinners")

    def command_map(self) -> Dict[str, Command]:
        return self._command_map

    async def on_channel_msg(self, bot: InfinitumBot, target: str, send_by: str, msg: str) -> None:
        await self._on_msg(bot, target, send_by, msg)

    async def on_query_msg(self, bot: InfinitumBot, send_by: str, msg: str) -> None:
        await self._on_msg(bot, send_by, send_by, msg)

    async def _on_msg(self, bot: InfinitumBot, target: str, send_by: str, msg: str) -> None:
        if re.fullmatch(Waitress.COOKIES_REGEX, msg):
            await bot.me_action(f"schenkt {send_by} einen {random.choice(self.cookies)}.", target)
        if re.fullmatch(Waitress.DRINK_REGEX, msg):
            await bot.me_action(f"schenkt {send_by} {random.choice(self.drinks)} ein.", target)
        if re.fullmatch(Waitress.FOOD_REGEX, msg):
            await bot.me_action(f"tischt {send_by} {random.choice(self.food)} auf.", target)
