#! /bin/python
import logging
import pydle

from .core.config import BotConfig


class InfinitumBot(pydle.Client):

    def __init__(self, config: BotConfig):
        super().__init__(config.nick)
        self._config = config

    def get_config(self):
        return self._config

    def run(self):
        if not self._config:  # TBD! or not self._config.is_valid():
            logging.critical("Tried run a bot without a valid config!")
            raise RuntimeError('No valid config is given')
        server = self._config.server
        port = self._config.port
        tls = self._config.tls
        tls_verify = self._config.tls_verify
        logging.info(f"Connecting {self._config.nick} to {server} at port {port} using TLS={tls}"\
                     f"and tls_verfiy={tls_verify}")
        super().run(hostname=server, port=port, tls=tls, tls_verify=False)

    def is_known_user(self, nickname: str) -> bool:
        for channel, info in self.channels.items():
            users = info['users']
            if nickname in users.keys():
                logging.debug(f"Found user {nickname} in channel {channel}")
                return True
        return False

    async def on_connect(self):
        for channel in self._config.channel_overview:
            await self.join(channel)
            await self.message(channel, "huhu sagt der uhu")

