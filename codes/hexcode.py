#!/usr/bin/env python3
import binascii

input_str = input("Enter a string: ")
hex_code = binascii.hexlify(input_str.encode())

print(hex_code)
