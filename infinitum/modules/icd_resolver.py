#! /bin/python3

import csv
import re
from typing import Dict, Any

from infinitum.bot import InfinitumBot
from infinitum.core.api import ModulePrototype, Command

ICD_PATH = "icd_codes"


class ICDResolver(ModulePrototype):
    ICD_REGEX = r'^.*\b\w\d{2}\.?\d?\b.*$'
    ICD_EXAMPLE = 'F84.5'
    ICD_HELP = 'Gibt die zugehörige Krankheit zu einem ICD Code aus.'

    def __init__(self):
        self._config = None
        resolver_cmd = Command.create_full_command(ICDResolver.ICD_REGEX, ICDResolver.ICD_HELP,
                                                   ICDResolver.ICD_EXAMPLE, self)
        self._command_map = {ICDResolver.ICD_REGEX: resolver_cmd}

    def setup(self, bot: InfinitumBot, config: Dict[str, Any]) -> None:
        self._config = config

    def command_map(self) -> Dict[str, Command]:
        return self._command_map

    async def on_channel_msg(self, bot: InfinitumBot, target: str, send_by: str, msg: str) -> None:
        await self._on_msg(bot, target, send_by, msg)

    async def on_query_msg(self, bot: InfinitumBot, send_by: str, msg: str) -> None:
        await self._on_msg(bot, send_by, send_by, msg)

    async def _on_msg(self, bot: InfinitumBot, target: str, send_by: str, msg: str) -> None:
        regex = r'\b(\w\d{2}\.?\d?)\b'
        codes = re.findall(regex, msg)
        for code in codes:
            code = code.capitalize()
            text = self.get_icd(code)
            if text == 0:
                if code.find('.') != -1:
                    code += '-'
                else:
                    code += '.-'
            text = self.get_icd(code)
            if text != 0:
                await bot.message(target, text)

    def get_icd(self, code):
        icd10_codes = open(self._config[ICD_PATH], 'r', encoding='utf8')
        icd10 = csv.reader(icd10_codes, delimiter=';', quotechar='"')
        for row in icd10:
            if row[0] == code:
                return code + ' - ' + row[1]
