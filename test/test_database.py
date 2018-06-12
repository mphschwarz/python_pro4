import unittest

import database


class TestDatabase(unittest.TestCase):
    def test_regex(self):
        """checks that inventory file is ingested correctly"""
        raw_exhibitions = database.read_database('../test_database/data_inventory.txt')
        exhibitions = [('romans',
                        '    233(\n        de  roemischerhelm.mp3  roemischerhelm.tex\n        en  romanhelmet.mp3     romanhelmet.tex\n    )\n    10(\n        de  becher_rom.mp3      becher_rom.tex\n        en  cup_rome.mp3        cup_rome.tex\n    )\n'),
                       ('middle_ages',
                        '    15(\n        de  mittelalterlicher_schaedel.mp3  mittelalterlicher_schaedel.tex\n        en  skull_medieval.mp3              skull_medieval.tex\n    )\n    11(\n        de  morgenstern.mp3         morgenstern.tex\n        en  primitive_weapon.mp3    primitive_weapon.tex\n    )\n')]
        self.assertEqual(exhibitions, database.exhibition_regex.findall(raw_exhibitions))
        objects = \
            [('233',
              'de  roemischerhelm.mp3  roemischerhelm.tex\n        en  romanhelmet.mp3     romanhelmet.tex\n    '),
             ('10',
              'de  becher_rom.mp3      becher_rom.tex\n        en  cup_rome.mp3        cup_rome.tex\n    ')]
        self.assertEqual(objects, database.object_regex.findall(exhibitions[0][1]))
        languages = [('de', 'roemischerhelm.mp3', 'roemischerhelm.tex'),
                     ('en', 'romanhelmet.mp3', 'romanhelmet.tex')]
        self.assertEqual(languages, database.language_regex.findall(objects[0][1]))

    def test_parse_database(self):
        """checks that the correct dictionary tree is generated"""
        inventory = \
            {
                'romans': {
                    '233': {
                        'de': ['roemischerhelm.mp3', 'roemischerhelm.tex'],
                        'en': ['romanhelmet.mp3', 'romanhelmet.tex']
                    },
                    '10': {
                        'de': ['becher_rom.mp3', 'becher_rom.tex'],
                        'en': ['cup_rome.mp3', 'cup_rome.tex']
                    },

                },
                'middle_ages': {
                    '15': {
                        'de': ['mittelalterlicher_schaedel.mp3', 'mittelalterlicher_schaedel.tex'],
                        'en': ['skull_medieval.mp3', 'skull_medieval.tex']
                    },
                    '11': {
                        'de': ['morgenstern.mp3', 'morgenstern.tex'],
                        'en': ['primitive_weapon.mp3', 'primitive_weapon.tex']
                    }
                }
            }
        self.assertEqual(inventory,
                         database.parse_inventory(database.read_database('../test_database/data_inventory.txt')))

    def test_package_maker(self):
        """checks if dictionary tree contains correct values form test inventory file"""
        compiled_inventory = ['233', '10']
        compiled_package = ['romanhelmet.mp3', 'cup_rome.mp3']
        self.assertEqual((compiled_inventory, compiled_package), database.compile_inventory_package(
                ['romans'],
                ['en'],
                database.parse_inventory(database.read_database('../test_database/data_inventory.txt'))
        ))
        compiled_inventory = ['233', '10']
        compiled_package = ['roemischerhelm.mp3', 'romanhelmet.mp3', 'becher_rom.mp3', 'cup_rome.mp3']
        self.assertEqual((compiled_inventory, compiled_package), database.compile_inventory_package(
                ['romans'],
                ['de', 'en'],
                database.parse_inventory(database.read_database('../test_database/data_inventory.txt'))
        ))
        compiled_inventory = ['233', '10', '15', '11']
        compiled_package = ['roemischerhelm.mp3', 'romanhelmet.mp3',
                            'becher_rom.mp3', 'cup_rome.mp3',
                            'mittelalterlicher_schaedel.mp3', 'skull_medieval.mp3',
                            'morgenstern.mp3', 'primitive_weapon.mp3']
        self.assertEqual((compiled_inventory, compiled_package), database.compile_inventory_package(
                ['romans', 'middle_ages'],
                ['de', 'en'],
                database.parse_inventory(database.read_database('../test_database/data_inventory.txt'))))
        self.assertEqual((compiled_inventory, compiled_package), database.compile_inventory_package(
                ['romans', 'middle_ages'],
                ['de', 'en'],
                database.parse_inventory(database.read_database('../test_database/data_inventory.txt'))))
        self.assertEqual((compiled_inventory, compiled_package), database.compile_inventory_package(
                database.read_preset('../test_database/test_preset.txt')[1],
                database.read_preset('../test_database/test_preset.txt')[0],
                database.parse_inventory(database.read_database('../test_database/data_inventory.txt'))))

    def test_compiled_eeprom(self):
        """tests if eeprom ticket contains correct values"""
        total_inventory = database.parse_inventory(database.read_database('../test_database/data_inventory.txt'))
        language = 'de'
        payed_exhibitions = ['romans']
        expected_eeprom = (0, [233, 10, 15, 11], [2, 2, 0, 0])
        compiled_inventory, compiled_package = database.compile_inventory_package(['romans', 'middle_ages'],
                                                                                  ['de', 'en'],
                                                                                  total_inventory)
        compiled_test_eeprom = database.compile_eeprom(payed_exhibitions, 'de', compiled_inventory, total_inventory)
        self.assertEqual(expected_eeprom, compiled_test_eeprom)

    def test_compiled_package(self):
        total_inventory = database.parse_inventory(database.read_database('../test_database/data_inventory.txt'))
        preset = database.read_preset('../test_database/test_preset.txt')
        compiled_inventory, compiled_package = database.compile_inventory_package(preset[1], preset[0], total_inventory)
        database.compile_package(compiled_package, '../test_database', '../test_database/test_package',
                                 audio_format='.ad4')
