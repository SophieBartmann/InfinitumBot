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


    def __init__(self):
        self.cookies = []
        self.drinks = []
        self.food = []
        self._config = None
        self._command_map = { Waitress.COOKIES_REGEX: (Waitress.COOKIES_EXAMPLE, Waitress.COOKIES_HELP) }

    def setup(self, bot: InfinitumBot, config: Dict[str, Any]) -> None:
        self._config = config
        self.cookies = utils.read_list(config[COOKIES_PATH])
        logging.debug(f"Successfully loaded {len(self.cookies)} cookies")
        #self.food = utils.read_list(config[FOOD_PATH])
        #self.drinks = utils.read_list(config[DRINKS_PATH])

    def command_map(self) -> Dict[str, str]:
        return self._command_map

    async def on_channel_msg(self, bot: InfinitumBot, target: str, send_by: str, msg: str) -> None:
        if re.fullmatch(Waitress.COOKIES_REGEX, msg):
            await bot.me_action(f"schenkt {send_by} einen {random.choice(self.cookies)}.", target)


