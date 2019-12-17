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

    def test_get_bot(self):
        bot_overview = self.testConfig.bot_overview
        self.assertEqual(bot_overview, ['infinitumBot'])
