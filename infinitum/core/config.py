#! /bin/python3
import json
import logging
from typing import List, Dict, Any, Union, Set

import hcl

DEBUG = 'debug'
LOG_FILE = 'log_file'
BOT = 'Bot'
NICK = 'nick'
USERNAME = 'username'
REALNAME = 'realname'
ADMINS = 'admins'
CHANNEL = 'Channel'
ENTRY_MSG = 'entry_message'
LEAVE_MSG = 'leave_message'
SERVER = 'server'
PORT = 'port'
TLS = 'tls'
TLS_VERIFY = 'tls_verify'
MODULES = 'modules'
MODULE = 'Module'


class ModuleConfig:
    def __init__(self, config: Dict[str, Any] = None):
        pass


class ChannelConfig:
    def __init__(self, name: str, config: Dict[str, Any], parent):
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
        self._module_cache = dict()
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
        return create_set_from_list_or_dict(self.config.get(CHANNEL, {}))

    def get_channel(self, channel_name: str) -> Union[ChannelConfig, None]:
        if channel_name not in self.channel_overview:
            logging.debug(f"Channel '{channel_name}' has been queried, but could not find it in" \
                          "the config")
            return None
        if channel_name not in self._channel_cache.keys():
            logging.debug(f"Channel '{channel_name}' yet not within the cache, therefore creating it")
            if type(self.config[CHANNEL]) is type([]):
                for c in self.config[CHANNEL]:
                    channel_dict = c.get(channel_name, None)
                    if channel_dict is not None:
                        break  # we've found the channel needed
            else:
                channel_dict = self.config[CHANNEL].get(channel_name, None)
            if channel_dict is not None:
                self._channel_cache[channel_name] = ChannelConfig(channel_name, channel_dict, self)
        if channel_name in self._channel_cache.keys():
            logging.debug(f"Cache hit for channel '{channel_name}'")
        else:
            logging.warning(f"No config for channel '{channel_name}' could be found")
        return self._channel_cache.get(channel_name, None)

    @property
    def module_overview(self) -> Set[str]:
        return create_set_from_list_or_dict(self.config.get(MODULE, {}))

    def get_module(self, modulename: str) -> Union[Dict[str, Any], None]:
        if modulename not in self.module_overview:
            logging.warn(f"Module '{modulename}' has been queried but no config could be found.")
            return None
        if modulename not in self._module_cache.keys():
            modules = self.config.get(MODULE, {})
            module_dict = None
            if isinstance(modules, type([])):
                for m in modules:
                    module_dict = m.get(modulename, None)
                    if module_dict is not None:
                        break
            else:
                module_dict = modules.get(modulename, None)
            if module_dict is not None:
                self._module_cache[modulename] = module_dict
        if modulename in self._module_cache.keys():
            logging.debug(f"Cache hit for module '{modulename}'.")
        else:
            logging.warning(f"No config for Module '{modulename}' could be found.")
        return self._module_cache.get(modulename, None)


class Config:
    def __init__(self, path: str = None):
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
    def bot_overview(self) -> Set[str]:
        """
        returns: A set containing the names of all defined bots. To get the bot-config object
        itself use #get_bot
        """
        return create_set_from_list_or_dict(self.config.get(BOT, {}))

    def get_bot(self, bot: str) -> Union[BotConfig, None]:
        if bot not in self.bot_overview:
            return None
        if bot not in self._bot_cache.keys():
            self._bot_cache[bot] = BotConfig(bot, self.config[BOT][bot], self)
        return self._bot_cache[bot]


def create_set_from_list_or_dict(list_or_dict: Union[List, Dict]) -> Set[str]:
    """
    Takes either a dict or a list containing dicts and returns a set containing (toplevel) keys
    within the dict or the dicts within the list.
    This is needed since something like this:
    
    foo "bar"{
        /* stuff */
    }
    
    will be transformed to:

    { foo: bar: {/* stuff */ } }
    
    but:
    
    foo "bar" {
        /* stuff */
    }
    foo "nope" {
        /* another stuff */
    }
    
    will be transformed to:
    
    { foo: [
        bar : { /* stuff */ },
        nope: { /* another stuff */ }
        ]
    }

    If you now want the keys (bar and nope) you have to handle it differently depending wether there
    is more than one element or not.

    This is the case when using multiple bot definitions within one config file, as well as multiple
    channels within one bot and multiple module definitions.
    """
    if type(list_or_dict) is type([]):
        oset = set()
        for element in list_or_dict:
            for key in element.keys():
                oset.add(key)
        return oset
    else:
        return set(list_or_dict.keys())


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
