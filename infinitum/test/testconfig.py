#! /bin/python3
import unittest
import os
from infinitum.core.config import Config

class SimpleConfigTest(unittest.TestCase):
    def setUp(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_directory, 'test-config.hcl')
        self.testConfig = Config(path=config_path)

    def test_get_global_admins(self):
        global_admins = self.testConfig.global_admins
        self.assertEqual(global_admins, ['global_admin'])

    def test_set_global_admin(self):
        self.testConfig.global_admins.append("another_admin")
        global_admins = self.testConfig.global_admins
        self.assertEqual(global_admins, ['global_admin', 'another_admin'])

    def test_get_debug(self):
        debug = self.testConfig.debug
        self.assertEqual(debug, True)

    def test_get_bot_overview(self):
        bot_overview = self.testConfig.bot_overview
        self.assertEqual(bot_overview, {'infinitumBot'})

    def test_get_bot_config(self):
        bot_config = self.testConfig.get_bot('infinitumBot')
        self.assertIsNotNone(bot_config)

    def test_get_bot_admins(self):
        bot_config = self.testConfig.get_bot('infinitumBot')
        bot_admins = bot_config.bot_admins
        self.assertEqual(bot_admins, ['bot_admin'])

    def test_get_bot_channel(self):
        bot_config = self.testConfig.get_bot('infinitumBot')
        channel = bot_config.channel_overview
        self.assertEqual(channel, {'#infinitumbot', '#infinitum2'})
