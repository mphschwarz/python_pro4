import serial
import time

def init_serial(dev_name=None, boud=115200, timeout=0.1):
    if not dev_name:
        try:
            device = serial.Serial('/dev/ttyACM0', boud, timeout=timeout)
        except serial.serialutil.SerialException:
            device = serial.Serial('/dev/ttyACM1', boud, timeout=timeout)
    else:
        device = serial.Serial(dev_name, boud, timeout=timeout)
    time.sleep(2)
    device.flush()
    return device

def pass_value(value, address, device, sleeptime=0.01):
    outstring = 'p{0:0>3}{1:0>3};'.format(address, value)
    device.write(bytes(outstring, 'utf-8'))
    while device.readline().decode('utf-8') != 'r\n':
        pass


def request_value(address, device, sleeptime=0.01):
    outstring = 'q{:>3};'.format(address)
    device.write(bytes(outstring, 'utf-8'))
    time.sleep(sleeptime)
    temp = device.readline().decode('utf-8')
    while temp == '' or temp == '\n':
        # time.sleep(sleeptime)
        temp = device.readline().decode('utf-8')
    return int(temp)


def write_inventory(inventory, access, language_code, device, sleeptime=0.04):
    pass_value(len(inventory), 0, device, sleeptime=sleeptime)
    pass_value(language_code, 1, device, sleeptime=sleeptime)
    for index, item in enumerate(inventory):
        pass_value(inventory[index], 2 * index + 2, device, sleeptime=sleeptime)
        pass_value(access[index], 2 * index + 3, device, sleeptime=sleeptime)


def read_inventory(device, sleeptime=0.01):
    entries = request_value(0, device)
    language = request_value(1, device)
    inventory = []
    for entry in range(2, 2 * entries + 2):
        inventory.append(request_value(entry, device, sleeptime=sleeptime))
    return entries, language, inventory

def extract_likes(device, sleeptime=0.01):
    likes = []
    nr_likes = request_value(0, device)
    for entry in range(0, nr_likes):
        likes.append(request_value(entry * 2 + 3, device))
    for index, like in enumerate(likes):
        if likes[index] == 2 or likes[index] == 0:
            likes[index] = False
        else:
            likes[index] = True
    return likes
