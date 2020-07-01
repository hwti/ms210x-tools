#!/usr/bin/env python3

import argparse
import hexdump

from linux.hidraw import HIDRaw
from devices import ms2109


def status(device, args):
    device.status()


def outout_data(data, output, show_addresses=False):
    if output:
        output.write(data)
        print('Saved {} bytes to {}'.format(output.tell(), output.name))
        output.close()
    else:
        if show_addresses:
            hexdump.hexdump(data)
        else:
            print(hexdump.dump(data))


def compute_address_size(args, default_size):
    if args.address is not None:
        address = args.address
        default_size = 1
    else:
        address = 0
    size = args.size if args.size is not None else default_size
    return address, size


def eeprom_dump(device, args):
    address, size = compute_address_size(args, device.eeprom_size())

    mem = bytearray()
    offset = 0
    while offset < size:
        data = device.read_eeprom_data(address + offset)
        mem += data
        offset += len(data)

    # Truncate to exact size since we read in chunks
    mem = mem[:size]
    outout_data(mem, args.output, args.address is None)


def xdata_dump(device, args):
    address, size = compute_address_size(args, 65536)

    mem = bytearray(size)
    for offset in range(size):
        mem[offset] = device.read_xdata_byte(address + offset)

    outout_data(mem, args.output, args.address is None)


def auto_int(hex_or_dec):
    """Supports parsing 0xNNNN arguments, in addition to decimal"""
    return int(hex_or_dec, 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--devname', help='Device to use (/dev/hidrawXX), instead of automatic detection')

    subparsers = parser.add_subparsers(title='subcommands')

    parser_status = subparsers.add_parser('status', help='Show information about detected device')
    parser_status.set_defaults(func=status)

    parser_eeprom_dump = subparsers.add_parser('eeprom-dump', help='Dump eeprom to stdout or file')
    parser_eeprom_dump.add_argument('-o', '--output', type=argparse.FileType('wb'), help='Write to a binary file, instead of hex on stdout')
    parser_eeprom_dump.add_argument('-a', '--address', type=auto_int, help='Start address')
    parser_eeprom_dump.add_argument('-s', '--size', type=auto_int, help='Size, defaults the whole EEPROM if no address specified, 1 else')
    parser_eeprom_dump.set_defaults(func=eeprom_dump)

    parser_eeprom_dump = subparsers.add_parser('xdata-dump', help='Dump XDATA to stdout or file')
    parser_eeprom_dump.add_argument('-o', '--output', type=argparse.FileType('wb'), help='Write to a binary file, instead of hex on stdout')
    parser_eeprom_dump.add_argument('-a', '--address', type=auto_int, help='Start address')
    parser_eeprom_dump.add_argument('-s', '--size', type=auto_int, help='Size, defaults 65536 if no address specified, 1 else')
    parser_eeprom_dump.set_defaults(func=xdata_dump)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        if args.devname:
            hidraw = HIDRaw(devname=args.devname)
        else:
            hidraw = HIDRaw(0x534D, 0x2109)
        device = ms2109.Device(hidraw)
        args.func(device, args)
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
