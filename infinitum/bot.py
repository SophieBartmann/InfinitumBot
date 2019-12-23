#! /bin/python
import logging
import pydle
import re

from importlib import import_module

from .core.config import BotConfig


class InfinitumBot(pydle.Client):

    def __init__(self, config: BotConfig):
        super().__init__(config.nick)
        self._config = config
        self._modules = dict()
        self._setup()

    def _setup(self) -> None:
        for fq_module_name in self._config.module_overview:
            module_config = self._config.get_module(fq_module_name)
            import_path, module_class = fq_module_name.rsplit('.', 1)
            module = import_module('.' + import_path, package='infinitum.modules')
            clazz = getattr(module, module_class)
            module_instance = clazz()
            module_instance.setup(self, module_config)
            self._modules[fq_module_name] = module_instance
            

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
    
    async def is_admin(self, nickname: str, channel: str) -> bool:
        is_admin = False
        channel_admins = self._config.get_channel(channel).admins
        # An admin must set within the config AND must be identified to nickserv
        if nickname in self._config.bot_admins or nickname in channel_admins:
            is_admin = is_identified(nickname)
        return is_admin

    async def is_identified(self, nickname: str) -> bool:
        whois_info = await self.whois(nickname)
        return whois_info['identified']

    async def me_action(self, msg: str, target: str) -> None:
        await self.message(target, '\001ACTION ' + msg)

    async def on_connect(self):
        for channel in self._config.channel_overview:
            await self.join(channel)
            entry_msg = self._config.get_channel(channel).entry_message
            await self.message(channel, entry_msg)

    async def on_channel_message(self, target: str, send_by: str, msg: str) -> None:
        logging.debug("received channel message")
        # We don't want to react on our own messages
        if send_by == self._config.nick:
            return
        channel_modules = self._config.get_channel(target).module_list
        logging.debug(f"In channel '{target}' are the following {len(channel_modules)} modules active: {channel_modules}")
        logging.debug(f"matching {msg} against..")
        for fq_module in channel_modules:
            module = self._modules[fq_module]
            cmd_map = module.command_map()
            logging.debug(f".. module '{fq_module}'")
            for cmd_re in cmd_map.keys():
                logging.debug(f"...with regex '{cmd_re}'")
                if re.fullmatch(cmd_re, msg):
                    logging.debug(f"Message in channel '{target}' send by '{send_by}' matches"\
                                  f"'{fq_module}'")
                    await module.on_channel_msg(self, target, send_by, msg)



