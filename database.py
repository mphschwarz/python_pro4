import re
import os
import shutil

exhibition_regex = re.compile(r'exhibition\s([\w,_]+)\{\n([^}]+)')
object_regex = re.compile(r'(\d+)\(\s*([^\)]+)\)')
language_regex = re.compile(r'(\w{2})\s+(\w+\.\w+)\s+(\w+\.\w+)')

preset_regex = re.compile(r'(\w+),?\s?')

language_key = {'de': 0, 'en': 1}

def read_database(db_file):
    file = open(db_file, 'r')
    out_string = file.read()
    file.close()
    return out_string

def read_preset(preset_file):
    file = open(preset_file, 'r')
    preset_string = file.readlines()
    file.close()
    preset_string[0] = preset_string[0].split(': ')[1]
    preset_string[1] = preset_string[1].split(': ')[1]
    return preset_regex.findall(preset_string[0]), preset_regex.findall(preset_string[1])


def parse_inventory(database):
    """reads database file and compiles entries into a dict"""
    exhibitions = exhibition_regex.findall(database)
    inventory = {}
    for exhibition in exhibitions:
        inventory.update({exhibition[0]: {}})
        objs = object_regex.findall(exhibition[1])
        for obj in objs:
            inventory[exhibition[0]].update({obj[0]: {}})
            langs = language_regex.findall(obj[1])
            for lang in langs:
                inventory[exhibition[0]][obj[0]].update({lang[0]: [lang[1], lang[2]]})

    return inventory

def compile_inventory_package(exhibitions, languages, inventory):
    """compiles a list of beacon ids and audio files"""
    compiled_inventory = []
    compiled_package = []
    for exhibition in exhibitions:
        for obj in inventory[exhibition].keys():
            compiled_inventory.append(obj)
            for language in languages:
                compiled_package.append(inventory[exhibition][obj][language][0])
    return compiled_inventory, compiled_package

def compile_eeprom(exhibitions, language, compiled_invetory, inventory):
    """generates list of beacon ids and corresponding access/like bytes for eeprom"""
    payed_objects = []
    for exhibition in exhibitions:
        for beacon_id in inventory[exhibition].keys():
            payed_objects.append(beacon_id)
    compiled_eeprom = [len(compiled_invetory), language_key[language]]
    ids = []
    access = []
    for beacon_id in compiled_invetory:
        # compiled_eeprom.append(int(beacon_id))
        ids.append(int(beacon_id))
        if beacon_id in payed_objects:
            access.append(2)
            # compiled_eeprom.append(2)
        else:
            access.append(0)
            # compiled_eeprom.append(0)
    # return compiled_eeprom
    return language_key[language], ids, access

def compile_package(compiled_package, audio_path, package_path, audio_format='.mp3'):
    """copies all audio files in compiled_package into a separate folder with wtv compliant names"""
    for index, audiofile in enumerate(compiled_package):
        shutil.copy('{}/{}'.format(audio_path, audiofile),
                    '{0:}/{1:0>4}{2:}'.format(package_path, index, audio_format))

