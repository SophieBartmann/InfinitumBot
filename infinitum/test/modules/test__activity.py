import os
import sqlite3
import unittest
from datetime import datetime
from random import randrange

from infinitum.modules.activity import ActivityProvider, Activity


class ActivityProviderTest(unittest.TestCase):

    def setUp(self) -> None:
        # in case there is some database left because the last test failed.
        if os.path.exists(self.get_database_path()):
            self.remove_database()

    @staticmethod
    def generate_activity(nick_prefix='nick', channel='channel', amount=10):
        return [Activity(nick_prefix + str(randrange(amount * 5)), channel, datetime.now()) for n in range(amount)]

    @staticmethod
    def get_database_path():
        cwd = os.getcwd()
        return os.path.join(cwd, 'test-db.sqlite')

    def get_db_connection(self):
        connection = sqlite3.connect(self.get_database_path(),
                                     detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        connection.row_factory = sqlite3.Row
        return connection

    def remove_database(self):
        os.remove(self.get_database_path())

    def tearDown(self) -> None:
        self.remove_database()

    def test_create_table(self):
        provider = ActivityProvider(self)
        provider.setup()

    def test_create_query_single_activity(self):
        provider = ActivityProvider(self)
        provider.setup()
        provider.update_activity_now("testuser", "#testchannel")
        activity = provider.get_single_activity("testuser", "#testchannel")
        self.assertIsNotNone(activity)
        self.assertEqual("testuser", activity.nick)
        self.assertEqual("#testchannel", activity.channel)

    def test_query_non_existent_activity(self):
        provider = ActivityProvider(self)
        provider.setup()
        activity = provider.get_single_activity("nonexistentuser", "#nonexistent")
        self.assertIsNone(activity)

    def test_create_query_multi_activity(self):
        provider = ActivityProvider(self)
        provider.setup()
        channel1 = ActivityProviderTest.generate_activity(channel='channel1')
        channel2 = ActivityProviderTest.generate_activity(channel='channel2')
        both = list(channel1)
        both.extend(channel2)
        for a in both:
            provider.update_activity(a)
        nicks1 = [a.nick for a in channel1]
        nicks2 = [a.nick for a in channel2]
        query1 = provider.get_multiple_activities(nicks1, 'channel1')
        query2 = provider.get_multiple_activities(nicks2, 'channel2')
        self.assert_activity_in(channel1, query1)
        self.assert_activity_in(channel2, query2)

    def assert_activity_in(self, expected, query):
        for a in query:
            self.assertTrue(a in expected)
