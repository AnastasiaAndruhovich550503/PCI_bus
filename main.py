#!/usr/bin/env python

import os


pci_decoded_ids = list()
list_of_dirs = list()
devices_list = list()


def file_open():
    # get info from file with ids decoding
    pci_ids = open('/usr/share/hwdata/pci.ids', 'r')
    global pci_decoded_ids
    pci_decoded_ids = pci_ids.readlines()
    pci_ids.close()


def get_dir_listing():
    global list_of_dirs
    list_of_dirs = list()
    for dirname, dirnames, filenames in os.walk("/sys/bus/pci/devices"):
        # get path to all subdirectories
        for subdirname in dirnames:
            list_of_dirs.append(os.path.join(dirname, subdirname))


def get_ids():
    # get list of (vendor_id, device_id)
    get_dir_listing()
    global devices_list
    devices_list = list()
    for dir in list_of_dirs:
        vendor_id = open(dir + "/vendor", 'r')
        device_id = open(dir + "/device", 'r')
        devices_list.append((vendor_id.read()[:-1], device_id.read()[:-1]))
        vendor_id.close()
        device_id.close()


def my_lspci():
    get_ids()
    file_open()
    string_list = list()
    string_indexes = list()
    # find decoded vendor name
    for device_element in devices_list:
        vendor_element_string = str(device_element[0])
        vendor_element_string = vendor_element_string[2:]
        string_index = -1
        for list_element in pci_decoded_ids:
            string = str(list_element)
            res = -1
            string_index += 1
            if string[0] != '\t':
                res = string.find(vendor_element_string)
            if res != - 1:
                string_list.append(string[6:-1])
                string_indexes.append(string_index + 1)
                break

    # find decoded device name
    i = 0
    for device_element in devices_list:
        device_element_string = str(device_element[1])
        device_element_string = device_element_string[2:]
        res = - 1
        index = string_indexes[i]

        # search in strings after vendor name
        while res != 0:
            string = pci_decoded_ids[index]
            if string[0] == '\t' and string[1] != 't':
                string = string[1:]
                res = string.find(device_element_string)
            if res == 0:
                print(str(i + 1) + ". " + string_list[i] + string[4:-1])
                break
            index += 1

        i += 1


if __name__ == '__main__':
    my_lspci()
