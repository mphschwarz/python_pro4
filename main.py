import serial
import time
import click
import re

import eeprom
import database

exhibition_regex = re.compile('(\w+)')


@click.command()
@click.argument('inventory_file')
@click.argument('preset_file')
@click.option('--exhibitions', prompt=True, help='exhibitions that the visitor has payed for')
@click.option('--language', prompt=True, help='language selected by visitior')
def make_ticket(inventory_file, preset_file, exhibitions, language):
    exhibitions = exhibition_regex.findall(exhibitions)
    load_eeprom(inventory_file, preset_file, exhibitions, language)


def load_eeprom(inventory_file, preset_file, exhibitions, language):
    presets = database.read_preset(preset_file)
    complete_inventory = database.parse_inventory(database.read_database(inventory_file))
    compiled_inventory, compiled_package = database.compile_inventory_package(presets[1],
                                                                              presets[0],
                                                                              complete_inventory)
    eeprom_conents = database.compile_eeprom(exhibitions, language, compiled_inventory, complete_inventory)
    device = eeprom.init_serial()
    eeprom.write_inventory(eeprom_conents[1], eeprom_conents[2], eeprom_conents[0], device)
    pass


def load_sd(inventory_file, preset_file, sd_path):
    os.system('mount /dev/{} .'.format(sd_path))

    pass
