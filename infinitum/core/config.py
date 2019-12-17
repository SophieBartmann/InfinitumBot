#! /bin/python3
import hcl

from typing import List, Dict, Any, Union

DEBUG = 'debug'
LOG_FILE = 'log_file'
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
    def __init__(self, path: str=None):
        self.path = path
        self.config = dict()
        if path:
            self.load(path)

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
    def channel_list(self) -> List[str]:
        return self.config.get(CHANNEL, {}).keys()

    def get_channel(self, channel: str) -> Union[ChannelConfig, None]:
        if channel not in self.channel_list:
            return None
        return ChannelConfig(self.config[channel])
