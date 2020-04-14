import logging
from datetime import datetime
from sqlite3 import Cursor, Connection
from typing import Union, List, Dict

from infinitum.bot import InfinitumBot
from infinitum.core.api import ModulePrototype, Command


class Activity:
    def __init__(self, nick: str, channel: str, last_seen: datetime):
        self.nick: str = nick
        self.channel: str = channel
        self.last_seen: datetime = last_seen


class ActivityProvider:
    CREATE_TABLE_STMT = '''CREATE TABLE IF NOT EXISTS Activity (
                            nick TEXT NOT NULL UNIQUE,
                            channel TEXT NOT NULL,
                            last_seen TIMESTAMP NOT NULL)'''
    INSERT_OR_REPLACE_STMT = '''REPLACE INTO Activity
                                (nick, channel, last_seen)
                                VALUES (?, ?, ?)'''
    SELECT_STMT = '''SELECT nick, channel, last_seen
                     FROM Activity 
                     WHERE nick LIKE ? AND channel LIKE ?'''

    def __init__(self, bot):
        self.bot = bot

    def setup(self):
        logging.debug("Setting up Activity-Tables")
        connection: Connection
        with self.bot.get_db_connection() as connection:
            cursor: Cursor = connection.cursor()
            cursor.execute(ActivityProvider.CREATE_TABLE_STMT)
            connection.commit()

    def update_activity(self, activity: Activity):
        connection: Connection
        with self.bot.get_db_connection() as connection:
            cursor: Cursor = connection.cursor()
            cursor.execute(ActivityProvider.INSERT_OR_REPLACE_STMT,
                           (activity.nick, activity.channel, activity.last_seen))
            connection.commit()

    def update_activity_now(self, nick: str, channel: str):
        nick = nick.lower()
        last_seen = datetime.now()
        activity = Activity(nick, channel, last_seen)
        self.update_activity(activity)

    def get_single_activity(self, nick: str, channel: str) -> Union[Activity, None]:
        activities = self.get_multiple_activities([nick], channel)
        if len(activities) == 0:
            return None
        else:
            return activities[0]

    def get_multiple_activities(self, nicks: List[str], channel: str) -> List[Activity]:
        activities = []
        connection: Connection
        with self.bot.get_db_connection() as connection:
            cursor: Cursor = connection.cursor()
            for nick in nicks:
                nick = nick.lower()
                cursor.execute(ActivityProvider.SELECT_STMT, (nick, channel))
                row = cursor.fetchone()
                if row is not None:
                    current = Activity(row['nick'], row['channel'], row['last_seen'])
                    activities.append(current)
        return activities


class IdleChecker(ModulePrototype):
    SEEN_RE = r"^.seen [A-Za-z-_0-9]+$"
    SEEN_EXAMPLE = ".seen"
    SEEN_DESCRIPTION = ""

    def __init__(self):
        self.provider: ActivityProvider = None
        seen_cmd = Command(IdleChecker.SEEN_RE,
                           self.on_seen,
                           None,
                           IdleChecker.SEEN_DESCRIPTION,
                           IdleChecker.SEEN_EXAMPLE,
                           self)
        self._cmd_map = {IdleChecker.SEEN_RE: seen_cmd}

    def command_map(self) -> Dict[str, Command]:
        return self._cmd_map

    def setup(self, bot: InfinitumBot, config) -> None:
        super().setup(bot, config)
        logging.debug("Setting up IdleChecker module.")
        self.provider = ActivityProvider(bot)
        self.provider.setup()

    def is_system_module(self) -> bool:
        return True

    async def on_join(self, bot: InfinitumBot, channel: str, user: str) -> None:
        self.provider.update_activity_now(user, channel)

    async def on_channel_msg(self, bot: InfinitumBot, target_channel: str, sent_by: str, msg: str) -> None:
        self.provider.update_activity_now(sent_by, target_channel)

    async def on_seen(self, bot: InfinitumBot, target_channel: str, sent_by: str, msg: str) -> None:
        user_seen = msg.split(' ')[1]
        activity = self.provider.get_single_activity(user_seen, target_channel)
        if activity is None:
            await bot.message(target_channel, f"{user_seen}? Nee, kenn ich nicht.")
        else:
            str_time = activity.last_seen.strftime("%d.%m.%y um %H:%M Uhr")
            await bot.message(target_channel, f"{user_seen} war zuletzt am {str_time} aktiv.")

    def kick_all_idling(self, bot: InfinitumBot) -> bool:
        pass
