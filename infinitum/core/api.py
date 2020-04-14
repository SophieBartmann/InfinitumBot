#! /bin/python3
from typing import Dict

from infinitum.bot import InfinitumBot


class Command:
    def __init__(self, pattern: str, channel_handle,
                 query_handle, description: str, example: str,
                 module):
        """
        Simple container class holding information needed to identify the functions to be called if a given pattern
        has been found within a message.
        """
        self.pattern = pattern
        self.channel_handle = channel_handle
        self.query_handle = query_handle
        self.description = description
        self.example = example
        self.module = module

    @staticmethod
    def create_channel_command(pattern: str, description: str, example: str, module):
        return Command(pattern, module.on_channel_msg, None, description, example, module)

    @staticmethod
    def create_query_command(pattern: str, description: str, example: str, module):
        return Command(pattern, None, module.on_query_msg, description, example, module)

    @staticmethod
    def create_msg_command(pattern: str, description: str, example: str, module):
        return Command(pattern, module.on_channel_msg, module.on_query_msg, description, example, module)


class ModulePrototype:
    def setup(self, bot: InfinitumBot, config) -> None:
        """
        Called when the bot boots. At this point each module should verify everything is set 
        up and works fine later when the action-calls are incoming
        """
        pass

    def command_map(self) -> Dict[str, Command]:
        """
        This method has to provide a dictionary mapping between commands - as regex pattern
        and a tuple of textes providing an example and an explanation ofthe usage of those commands.
        e.g.
        { r'^\.(cookie)$' : ('.cookie', 'Provides the caller with a random cookie') }0
        Important:
        The given pattern will be applied over the whole incoming message, if there is a match
        then the whole message will be given to the module; else the module will not be called.
        """
        return {}

    def is_system_module(self) -> bool:
        """
        Return true if this module needs to receive messages also non-command messages.
        Defaults to False
        """
        return False

    async def on_join(self, bot: InfinitumBot, channel: str, user: str) -> None:
        """
        Called if a user joins the given channel. This user may be bot itself.
        """
        pass

    async def on_channel_msg(self, bot: InfinitumBot, target_channel: str, sent_by: str, msg: str) -> None:
        """
        Called if either a command, created via create_channel_command or create_msg_command, is received
        or is_system_module is True.
        """
        pass

    async def on_query_msg(self, bot: InfinitumBot, sent_by: str, msg: str) -> None:
        """
        Called if either a command, created via create_query_command or create_msg_command, is received
        or is_system_modules is True.
        """
        pass

    async def on_kick(self, bot: InfinitumBot, channel: str, target: str, kicked_by: str, reason: str = None) -> None:
        """
        Called if someone on a channel the bot is in got kicked.
        """
        pass

    async def on_quit(self, bot: InfinitumBot, user: str, leave_msg: str = None) -> None:
        """
        Called if someone, maybe the bot itself, bot: InfinitumBot,  quit.
        """
        pass

    async def on_part(self, bot: InfinitumBot, channel: str, user: str, message: str = None) -> None:
        """
        Called if someone, maybe the bot itself, bot: InfinitumBot,  parts from a channel the bot is online in.
        """
        pass

    async def on_kill(self, bot: InfinitumBot, target: str, killed_by: str, reason: str = None) -> None:
        """
        Called if someone, maybe the bot itself, bot: InfinitumBot,  has been killed off the server.
        """
        pass

    async def on_nick_change(self, bot: InfinitumBot, old: str, new: str) -> None:
        """
        Called if someone, maybe the bot itself, bot: InfinitumBot,  changed nick.
        """
        pass
