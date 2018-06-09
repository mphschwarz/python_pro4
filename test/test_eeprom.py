import unittest
import time
import random

import eeprom


class TestEEPROM(unittest.TestCase):
    def test_eeprom_multi_read(self):
        """tests to see if it can get anything from eeprom"""
        eeprom_dump = []
        device = eeprom.init_serial()
        for address in range(0, 3):
            eeprom_dump.append(eeprom.request_value(address, device))
        self.assertIsNotNone(eeprom_dump)

    def test_single_echo_eeprom(self):
        """sends a single value to the mc to write to eeprom and checks if it can get the same value back"""
        device = eeprom.init_serial()
        echo_value = 1
        echo_address = 1
        t0 = time.time()
        eeprom.pass_value(echo_value, echo_address, device)
        echo_out = eeprom.request_value(echo_address, device)
        print('time elapsed for a simple echo: {:.3f}'.format(time.time() - t0))
        self.assertEqual(echo_out, echo_value)

    def test_sleeptime(self):
        """tests how small it can make the sleep time before errors occur"""
        serial_device = eeprom.init_serial()
        time.sleep(2)
        entries = 250
        for sleeptime in range(4, 80):
            sleeptime /= 500000

            inventory = [random.randint(0, 200) for _ in range(0, entries)]
            access = [random.randint(0, 200) for _ in range(0, entries)]
            expected_eeprom = (entries, 0, [val for pair in zip(inventory, access) for val in pair])

            eeprom.write_inventory(inventory, access, 0, serial_device, sleeptime=sleeptime)
            time.sleep(2)
            eeprom_dump = eeprom.read_inventory(serial_device)
            if eeprom_dump == expected_eeprom:
                print('eeprom passed at sleeptime: {}'.format(sleeptime))
                serial_device.close()
                return
            else:
                print('eeprom failed at sleeptime: {}'.format(sleeptime))
        serial_device.close()
        self.fail()

    def test_echo_eeprom(self):
        """sends 20 random integers to eeprom and checks if it gets the same values back"""
        sleeptime = 0.025
        inventory = [random.randint(0, 200) for _ in range(0, 10)]
        access = [random.randint(0, 200) for _ in range(0, 10)]
        serial_device = eeprom.init_serial()
        time.sleep(2)
        eeprom.write_inventory(inventory, access, 0, serial_device, sleeptime=sleeptime)
        time.sleep(2)
        eeprom_dump = eeprom.read_inventory(serial_device)
        self.assertEqual(eeprom_dump, (10, 0, [val for pair in zip(inventory, access) for val in pair]),
                         msg='eeprom content mismatch')

    def test_eeprom_benchmark(self):
        """successively increases number of entries, fails if there is a mismatch"""
        for entries in range(1, 11):
            entries *= 25
            inventory = [random.randint(0, 200) for _ in range(0, entries)]
            access = [random.randint(0, 200) for _ in range(0, entries)]
            device = eeprom.init_serial()
            t0 = time.time()
            eeprom.write_inventory(inventory, access, 0, device)
            t1 = time.time()
            eeprom_dump = eeprom.read_inventory(device)
            print('time elapsed for {} entries: {:.3f}'.format(entries, t1 - t0))
            self.assertEqual(eeprom_dump,
                             (len(inventory), 0, [val for pair in zip(inventory, access) for val in pair]),
                             msg='benchmark failded at {} entries'.format(entries))
