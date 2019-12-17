#! /bin/python3
import hcl
import logging
from typing import List, Dict, Any, Union

DEBUG = 'debug'
LOG_FILE = 'log_file'
BOT = 'Bot'
NICK = 'nick'
USERNAME = 'username'
REALNAME = 'realname'
ADMINS = 'admins'
CHANNEL = 'channel'
ENTRY_MSG = 'entry_message'
LEAVE_MSG = 'leave_message'
MODULES = 'modules'


class ModuleConfig:
    def __init__(self, config: Dict[str, Any]=None):
        pass
    

class ChannelConfig:
    def __init__(self, name: str, config: Dict[str, Any]=None):
        self._config = config
        self._name = name

    @property
    def module_list(self) -> List[str]:
        return self._config.get(MODULES, [])

    @property
    def channel_name(self) -> str:
        return self._name

    @property
    def entry_message(self) -> str:
        return self._config.get(ENTRY_MSG, '')

    @entry_message.setter
    def entry_message(self, value: str) -> None:
        self._config[ENTRY_MSG] = value

    @property
    def leave_message(self) -> str:
        return self._config.get(LEAVE_MSG, '')

    @leave_message.setter
    def leave_message(self, value: str) -> None:
        self._config[LEAVE_MSG] = value

    @property
    def admins(self) -> List[str]:
        return self._config.get(ADMINS, [])

    @admins.setter
    def admins(self, value: List[str]) -> None:
        self._config[ADMINS] = value


class BotConfig:
    def __init__(self, config: Dict[str, Any]):
        self.path = path
        self.config = config
        self._channel_cache = dict()


    @property
    def nick(self) -> str:
        return self.config.get(NICK, "InfinitumBot")

    @nick.setter
    def nick(self, value: str) -> None:
        self.config[NICK] = value

    @property
    def bot_admins(self) -> List[str]:
        return self.config.get(ADMINS, [])

    @bot_admins.setter
    def bot_admins(self, value: List[str]) -> None:
        self.config[ADMINS] = value

    @property
    def channel_overview(self) -> List[str]:
        """
        returns: A list containing the names the Bot has been configured to. To get the
        channel-config object itself use #get_channel
        """
        return list(self.config.get(CHANNEL, {}))

    def get_channel(self, channel: str) -> Union[ChannelConfig, None]:
        if channel not in self.channel_list:
            return None
        if channel not in self._channel_cache.keys():
            self._channel_cache[channel] = ChannelConfig(self.config[channel])
        return self_channel_cache[channel]


class Config:
    def __init__(self, path: str=None):
        self.path = path
        self.config = dict()
        if path:
            self.load(path)
        self._bot_cache = dict()

    def load(self, path: str) -> None:
        with open(path, 'r') as fp:
            self.config = hcl.load(fp)
    
    @property
    def debug(self) -> None:
        return self.config.get(DEBUG, False)

    @debug.setter
    def debug(self, value: bool) -> bool:
        self.config[DEBUG] = value

    @property
    def global_admins(self) -> List[str]:
        return self.config.get(ADMINS, [])

    @global_admins.setter
    def global_admins(self, value: List[str]) -> None:
        self.config[ADMINS] = value

    @property
    def bot_overview(self) -> List[str]:
        """
        returns: A list containing the names of all defined bots. To get the bot-config object
        itself use #get_bot
        """
        return list(self.config.get(BOT, {}))

