#! /bin/python3
import os
import unittest

from infinitum.core.config import Config


class SimpleConfigTest(unittest.TestCase):
    def setUp(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_directory, 'test-config.hcl')
        self.test_config = Config(path=config_path)

    def test_get_debug(self):
        debug = self.test_config.debug
        self.assertEqual(debug, True)

    def test_get_bot_overview(self):
        bot_overview = self.test_config.bot_overview
        self.assertEqual(bot_overview, {'infinitumBot'})

    def test_get_bot_config(self):
        bot_config = self.test_config.get_bot('infinitumBot')
        self.assertIsNotNone(bot_config)

    def test_get_bot_admins(self):
        bot_config = self.test_config.get_bot('infinitumBot')
        bot_admins = bot_config.bot_admins
        self.assertEqual(bot_admins, ['bot_admin'])

    def test_get_bot_channel(self):
        bot_config = self.test_config.get_bot('infinitumBot')
        channel = bot_config.channel_overview
        self.assertEqual(channel, {'#infinitumbot', '#infinitum2'})

    def test_get_channel_config(self):
        bot_config = self.test_config.get_bot('infinitumBot')
        channel = bot_config.get_channel('#infinitumbot')
        self.assertIsNotNone(channel)

    def test_get_module_overview(self):
        bot_config = self.test_config.get_bot('infinitumBot')
        modules = bot_config.module_overview
        self.assertEqual(modules, {'food.Waitress', 'fun.Peace'})
