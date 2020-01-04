#! /bin/python3

import re
import random
import logging

from typing import Dict, Any

from infinitum.core.api import ModulePrototype
from infinitum.bot import InfinitumBot
from infinitum import utils

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


    def __init__(self):
        self.cookies = []
        self.drinks = []
        self.food = []
        self._config = None
        self._command_map = {Waitress.COOKIES_REGEX: (Waitress.COOKIES_EXAMPLE, Waitress.COOKIES_HELP),
                             Waitress.DRINK_REGEX:(Waitress.DRINK_EXAMPLE, Waitress.DRINK_HELP)}

    def setup(self, bot: InfinitumBot, config: Dict[str, Any]) -> None:
        self._config = config
        self.cookies = utils.read_list(config[COOKIES_PATH])
        logging.debug(f"Successfully loaded {len(self.cookies)} cookies")
        self.drinks = utils.read_list(config[DRINKS_PATH])
        logging.debug(f"Successfully loaded {len(self.drinks)} drinks")
        #self.food = utils.read_list(config[FOOD_PATH])

    def command_map(self) -> Dict[str, str]:
        return self._command_map

    async def on_channel_msg(self, bot: InfinitumBot, target: str, send_by: str, msg: str) -> None:
        await self._on_msg(bot, target, send_by, msg)

    async def on_query_msg(self, bot: InfinitumBot, send_by: str, msg: str) -> None:
        await self._on_msg(bot, send_by, send_by, msg)

    async def _on_msg(self, bot: InfinitumBot, target: str, send_by: str, msg: str) -> None:
        if re.fullmatch(Waitress.COOKIES_REGEX, msg):
            await bot.me_action(f"schenkt {send_by} einen {random.choice(self.cookies)}.", target)
        if re.fullmatch(Waitress.DRINK_REGEX, msg):
            await bot.me_action(f"schenkt {send_by} {random.choice(self.drinks)} ein", target)



