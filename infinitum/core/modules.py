#! /bin/python3

import enum

from typing import Dict


class ModulePrototype:
    def setup(self, config) -> None:
        """
        Called when the bot boots. At this point each module should verify everything is set 
        up and works fine later when the action-calls are incoming
        """
        pass

    def command_map(self) -> Dict[str, str]:
        """
        This method has to provide a dictionary mapping between commands - as regex pattern
        and a tuple of textes providing an example and an explanation ofthe usage of those commands.
        e.g.
        { r'^\.(cookie)$' : ('.cookie', 'Provides the caller with a random cookie') }
        Important:
        The given pattern will be applied over the whole incoming message, if there is a match
        then the whole message will be given to the module; else the module will not be called.
        """
        pass

    async def on_join(self, channel: str, user: str) -> None:
        """
        Called if a user joins the given channel. This user may be bot itself.
        """
        pass

    async def on_channel_msg(self, target_channel: str, sent_by: str, msg: str) -> None:
        """
        Called if a message has been sent to a channel the bot is joined to.
        """
        pass

    async def on_query_msg(self, sent_by: str, msg: str) -> None:
        """
        Called if the bot receives a private messsage.
        """
        pass

    async def on_kick(self, channel: str, target: str, kicked_by: str, reason: str=None) -> None:
        """
        Called if someone on a channel the bot is in got kicked.
        """
        pass

    async def on_quit(self, user: str, leave_msg: str=None) -> None:
        """
        Called if someone, maybe the bot itself, quit.
        """
        pass

    async def on_part(self, channel: str, user: str, message str=None) -> None:
        """
        Called if someone, maybe the bot itself, parts from a channel the bot is online in.
        """
        pass

    async def on_kill(self, target: str, killed_by: str, reason: str=None) -> None:
        """
        Called if someone, maybe the bot itself, has been killed off the server.
        """
        pass

    async def on_nick_change(self, old: str, new: str) -> None:
        """
        Called if someone, maybe the bot itself, changed nick.
        """
        pass
 
