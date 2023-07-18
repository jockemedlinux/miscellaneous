#!/usr/bin/env python3

def hex_to_little_endian(hex_string):
        little_endian_hex = bytearray.fromhex(hex_string)[::-1]
        hex_str = ''.join([f'\\x{byte:02X}' if any(c.isupper() for c in hex_string) else f'\\x{byte:02x}' for byte in little_endian_hex])
        return hex_str

offset = input("What is thy input?:\t").replace('0x', '')

if len(offset) <= 8:
    print("\n" + "'" +hex_to_little_endian(offset) + "'")
else:
    print("\n" + hex_to_little_endian(offset) + '\x00\x00\x00\x00\x00')
