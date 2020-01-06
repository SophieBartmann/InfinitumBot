#! /bin/python3

from typing import Dict, Any

from infinitum.core.api import ModulePrototype
from infinitum.bot import InfinitumBot

import html
import re
import urllib
from urllib import request
from infinitum import utils

class URL_resolver(ModulePrototype):
    
    URL_REGEX = r'^.*(?P<url>https?://[^\s]+).*$'
    URL_EXAMPLE = 'https://ich-bin-ein-Beispiel.org'
    URL_HELP = 'Gibt den Titel einer URL aus'

    def __init__(self):
        self._config = None
        self._command_map = {URL_resolver.URL_REGEX:(URL_resolver.URL_EXAMPLE, URL_resolver.URL_HELP)}

    def setup(self, bot: InfinitumBot, config: Dict[str, Any]) -> None:
        self._config = config

    def command_map(self) -> Dict[str, str]:
        return self._command_map

    async def on_channel_msg(self, bot: InfinitumBot, target: str, send_by: str, msg: str) -> None:
        await self._on_msg(bot, target, send_by, msg)

    async def on_query_msg(self, bot: InfinitumBot, send_by: str, msg: str) -> None:
        await self._on_msg(bot, send_by, send_by, msg)

    async def _on_msg(self, bot: InfinitumBot, target: str, send_by: str, msg: str) -> None:
        regex = "(?P<url>https?://[^\s]+)"
        url = re.search(regex, msg)
        if url is not None:
            url = url.group()
            print(url)
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
                url = url
                req = urllib.request.Request(url, None, headers)
                resource = urllib.request.urlopen(req)
                title = self.getTitle(resource)
                title = title[:350]
                await bot.message(target, title)
            except Exception as exc:
                print(exc)
                pass

    def getTitle(self, resource: str):
        encoding = resource.headers.get_content_charset()
        if not encoding:
            encoding = 'utf-8'
        content = resource.read().decode(encoding, errors='replace')
        title_re = re.compile("<title>(.+?)</title>")
        title = title_re.search(content).group(1)
        title = html.unescape(title)
        title = utils.replace_html(title)
        return title



