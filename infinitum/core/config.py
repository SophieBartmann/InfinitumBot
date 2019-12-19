#! /bin/python3
import hcl
import logging
import json

from typing import List, Dict, Any, Union, Set


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
SERVER = 'server'
PORT = 'port'
TLS = 'tls'
TLS_VERIFY = 'tls_verify'


class ModuleConfig:
    def __init__(self, config: Dict[str, Any]=None):
        pass
    

class ChannelConfig:
    def __init__(self, name: str, parent, config: Dict[str, Any]=None):
        self.config = config
        self._name = name
        self._parent = parent

    @property
    def module_list(self) -> List[str]:
        return self.config.get(MODULES, [])

    @property
    def channel_name(self) -> str:
        return self._name

    @property
    def entry_message(self) -> str:
        return self.config.get(ENTRY_MSG, '')

    @entry_message.setter
    def entry_message(self, value: str) -> None:
        self.config[ENTRY_MSG] = value

    @property
    def leave_message(self) -> str:
        return self.config.get(LEAVE_MSG, '')

    @leave_message.setter
    def leave_message(self, value: str) -> None:
        self.config[LEAVE_MSG] = value

    @property
    def admins(self) -> List[str]:
        return self.config.get(ADMINS, [])

    @admins.setter
    def admins(self, value: List[str]) -> None:
        self.config[ADMINS] = value


class BotConfig:
    def __init__(self, nick: str, config: Dict[str, Any], parent):
        self.config = config
        self._parent = parent
        self._channel_cache = dict()
        self._nick = nick


    @property
    def nick(self) -> str:
        return self._nick

    @nick.setter
    def nick(self, value: str) -> None:
        pass

    @property
    def bot_admins(self) -> List[str]:
        return self.config.get(ADMINS, [])

    @bot_admins.setter
    def bot_admins(self, value: List[str]) -> None:
        self.config[ADMINS] = value

    @property
    def server(self) -> Union[str, None]:
        return self.config.get(SERVER, None)

    @server.setter
    def server(self, value: str) -> None:
        self.config[SERVER] = value

    @property
    def port(self) -> int:
        return self.config.get(PORT, -1)

    @port.setter
    def port(self, value: int) -> None:
        self.config[PORT] = value

    @property
    def tls(self) -> bool:
        return self.config.get(TLS, True)

    @tls.setter
    def tls(self, value: bool) -> None:
        self.config[TLS] = value

    @property
    def tls_verify(self) -> bool:
        return self.config.get(TLS_VERIFY, True)

    @tls_verify.setter
    def tls_verify(self, value: bool) -> None:
        self.config[TLS_VERIFY] = value

    @property
    def channel_overview(self) -> Set[str]:
        """
        returns: A list containing the names the Bot has been configured to. To get the
        channel-config object itself use #get_channel
        """
        channel_list = self.config.get(CHANNEL, {})
        if type(channel_list) is type([]):
            channel_set = set()
            for c in channel_list:
                for name in c.keys():
                    channel_set.add(name)
            return channel_set
        else: # type must be dict
            return set(channel_list.keys())

    def get_channel(self, channel: str) -> Union[ChannelConfig, None]:
        if channel not in self.channel_overview:
            return None
        if channel not in self._channel_cache.keys():
            self._channel_cache[channel] = ChannelConfig(channel, self.config[CHANNEL][channel],
                                                         self)
        return self.channel_cache[channel]


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
    def bot_overview(self) -> Set[str]:
        """
        returns: A list containing the names of all defined bots. To get the bot-config object
        itself use #get_bot
        """
        bot_list = self.config.get(BOT, {})
        if type(bot_list) is type([]):
            bot_set = set()
            for b in bot_set:
                for name in b.keys():
                    bot_set.add(name)
            return bot_set
        else:
            return set(bot_list.keys())

    def get_bot(self, bot: str) -> Union[BotConfig, None]:
        if bot not in self.bot_overview:
            return None
        if bot not in self._bot_cache.keys():
            self._bot_cache[bot] = BotConfig(bot, self.config[BOT][bot], self)
        return self._bot_cache[bot]
    

def sdump_config(config):
    """
    Returns a dump of the dictionary behind the given config. Therefore the config-object must 
    contain a config field.
    """
    return json.dumps(config.config, indent=1)


def dump_config(config):
    """
    Calls sdump_config and prints it to the stdout
    """
    print(sdump_config(config))
