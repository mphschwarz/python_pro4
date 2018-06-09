import click
import shutil
import re
import os
import getpass
import time

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

@click.command()
@click.argument('package_path')
def make_sd(package_path):
    sd_path = '/run/media/{}/8E5E-7CBB'.format(getpass.getuser())
    device = eeprom.init_serial()
    device.write(bytes('m      ;', 'utf-8'))
    time.sleep(0.1)
    load_sd(package_path, sd_path)

@click.command()
@click.argument('inventory_file')
@click.argument('preset_file')
@click.argument('package_path')
@click.option('--format', default='.ad4')
def make_package(inventory_file, preset_file, package_path, format):
    """generates a audio package from audio file found in current directory\n
    :param inventory_file: file specifying which audio files belong to which exhibiton and language\n
    :param preset_file: file specifying which exhibitions are to be written to sd\n
    :param package_path: folder to which all files in package are copied
    :param format: audio file format"""
    if not os.path.isdir(package_path):
        os.makedirs(package_path)
    total_inventory = database.parse_inventory(database.read_database(inventory_file))
    preset = database.read_preset(preset_file)
    compiled_inventory, compiled_package = database.compile_inventory_package(preset[1], preset[0], total_inventory)
    database.compile_package(compiled_package, '.', package_path, audio_format=format)

def load_eeprom(inventory_file, preset_file, exhibitions, language):
    """writes a ticket to eeprom
    :param inventory_file: file specifying which audio files belong to which exhibiton and language
    :param preset_file: file specifying which exhibitions are to be written to sd
    :param exhibitions: paid exhibitions
    :param language: language chosen by visitor"""
    presets = database.read_preset(preset_file)
    complete_inventory = database.parse_inventory(database.read_database(inventory_file))
    compiled_inventory, compiled_package = database.compile_inventory_package(presets[1],
                                                                              presets[0],
                                                                              complete_inventory)
    eeprom_conents = database.compile_eeprom(exhibitions, language, compiled_inventory, complete_inventory)
    device = eeprom.init_serial()
    eeprom.write_inventory(eeprom_conents[1], eeprom_conents[2], eeprom_conents[0], device)

def load_sd(package_path, sd_path):
    """clears sd card and loads new package
    :param package_path: directory containing the audio package
    :param sd_path: directory where the sd card is mounted
    :returns True if successful, False if not"""
    old_files = os.listdir(sd_path)
    for file in old_files:
        os.remove('{}/{}'.format(sd_path, file))

    source_files = os.listdir(package_path)
    for file in source_files:
        try:
            shutil.copy('{}/{}'.format(package_path, file), '{}/{}'.format(sd_path, file))
        except shutil.Error:
            click.echo('failed to copy {}/{} to {}/{}'.format(package_path, file, sd_path, file))
            return False
    return True
