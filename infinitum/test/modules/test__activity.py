import os
import sqlite3
import unittest

from infinitum.modules.activity import ActivityProvider


class ActivityProviderTest(unittest.TestCase):

    def setUp(self) -> None:
        # in case there is some database left because the last test failed.
        if os.path.exists(self.get_database_path()):
            self.remove_database()

    def get_database_path(self):
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
