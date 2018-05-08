import unittest

import main
import database
import eeprom

class TestEEPROM(unittest.TestCase):
    def test_main_eeprom(self):
        inventory_file = '../test_database/data_inventory.txt'
        preset_file = '../test_database/test_preset.txt'
        exhibitions = ['romans', 'middle_ages']
        language = 'de'

        main.load_eeprom(inventory_file, preset_file, exhibitions, language)
        eeprom_conents = eeprom.read_inventory(eeprom.init_serial())
        self.assertEqual(eeprom_conents, (4, 0, [233, 2, 10, 2, 15, 2, 11, 2]))

        exhibitions = ['middle_ages']
        main.load_eeprom(inventory_file, preset_file, exhibitions, language)
        eeprom_conents = eeprom.read_inventory(eeprom.init_serial())
        self.assertEqual(eeprom_conents, (4, 0, [233, 0, 10, 0, 15, 2, 11, 2]))

        exhibitions = ['romans']
        main.load_eeprom(inventory_file, preset_file, exhibitions, language)
        eeprom_conents = eeprom.read_inventory(eeprom.init_serial())
        self.assertEqual(eeprom_conents, (4, 0, [233, 2, 10, 2, 15, 0, 11, 0]))

    def test_visitor_cycle(self):
        """writes inventory to eeprom and reads likes, expects them to all be unliked"""
        inventory_file = '../test_database/data_inventory.txt'
        preset_file = '../test_database/test_preset.txt'
        exhibitions = ['romans', 'middle_ages']
        language = 'de'

        main.load_eeprom(inventory_file, preset_file, exhibitions, language)
        device = eeprom.init_serial()
        likes = eeprom.extract_likes(device)
        self.assertEqual(likes, [False, False, False, False])
