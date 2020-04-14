#! /bin/python
import logging
import re
import sqlite3
from importlib import import_module
from sqlite3 import Connection
from threading import Timer

import pydle

from .core.config import BotConfig


class InfinitumBot(pydle.Client):

    def __init__(self, config: BotConfig):
        super().__init__(config.nick)
        self._config = config
        self._modules = dict()
        self._timer_map = dict()
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

    def get_db_connection(self) -> Connection:
        # To be able to use type converters e.g. for date and timestamp:
        # see https://docs.python.org/3/library/sqlite3.html#default-adapters-and-converters
        connection = sqlite3.connect(self._config.database,
                                     detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # Set the row_factory for the ease of row-element access:
        # see: https://docs.python.org/3.8/library/sqlite3.html#accessing-columns-by-name-instead-of-by-index
        connection.row_factory = sqlite3.Row
        return connection

    def run(self):
        if not self._config:  # TBD! or not self._config.is_valid():
            logging.critical("Tried run a bot without a valid config!")
            raise RuntimeError('No valid config is given')
        server = self._config.server
        port = self._config.port
        tls = self._config.tls
        tls_verify = self._config.tls_verify
        logging.info(f"Connecting {self._config.nick} to {server} at port {port} using TLS={tls}" \
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
            is_admin = self.is_identified(nickname)
        return is_admin

    async def is_identified(self, nickname: str) -> bool:
        whois_info = await self.whois(nickname)
        return whois_info['identified']

    async def me_action(self, msg: str, target: str) -> None:
        await self.message(target, '\x01ACTION ' + msg)

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
        logging.debug(
            f"In channel '{target}' are the following {len(channel_modules)} modules active: {channel_modules}")
        logging.debug(f"matching {msg} against..")
        for command, module in self._iter_matching_commands(channel_modules, msg):
            await command.channel_handle(self, target, send_by, msg)
        for module in self._iter_system_modules(channel_modules):
            await module.on_channel_msg(self, target, send_by, msg)

    def _iter_matching_commands(self, modules_to_match, msg: str):
        for fq_module in modules_to_match:
            module = self._modules[fq_module]
            cmd_map = module.command_map()
            logging.debug(f".. module '{fq_module}'")
            if cmd_map is not None:
                for cmd_re, cmd in cmd_map.items():
                    logging.debug(f"...with regex '{cmd_re}'")
                    if re.fullmatch(cmd_re, msg):
                        logging.debug(f"Message '{msg}' matches '{cmd_re}' of module '{fq_module}'")
                        yield cmd, fq_module

    def _iter_channels_by_nick(self, nick: str):
        logging.debug(f"Iterating over channels with user '{nick}' in")
        for ch_name, ch_data in self.channels.items():
            for user_nick in ch_data['users']:
                if nick == user_nick:
                    logging.debug(f"Found user '{nick}' in channel '{ch_name}'")
                    yield ch_name

    def _iter_system_modules(self, modules_to_match):
        logging.debug(f"Iterating over system modules")
        for fq_module in modules_to_match:
            module = self._modules[fq_module]
            if module.is_system_module():
                logging.debug(f".. {fq_module} is a system module")
                yield module

    async def on_private_message(self, target: str, send_by: str, msg: str):
        logging.debug("received private message")
        if send_by == self._config.nick:
            return
        channels_with_user = [ch for ch in self._iter_channels_by_nick(send_by)]
        logging.debug(f"User '{send_by}' is in {len(channels_with_user)} channels active: {channels_with_user}")
        modules_with_user = set()
        for channel in channels_with_user:
            module_list = self._config.get_channel(channel).module_list
            modules_with_user = modules_with_user.union(module_list)
        for command, module in self._iter_matching_commands(modules_with_user, msg):
            await command.query_handle(self, send_by, msg)
        for module in self._iter_system_modules(modules_with_user):
            await module.on_query_msg(self, send_by, msg)

    def register_timer(self, fun, interval):
        self._timer_map[fun] = Timer(interval, self.timer_callback, fun, interval)
        self._timer_map[fun].start()

    def timer_callback(self, fun, interval):
        restart = fun(self)
        if restart:
            self.register_timer(fun, interval)

    def cancel_timer(self, fun):
        self._timer_map[fun].cancel()
        del self._timer_map[fun]
