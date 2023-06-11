#!/usr/bin/env python3
import binascii

input_str = input("Enter a string: ")
shellcode = ""

for ch in input_str:
    shellcode += "\\x" + binascii.hexlify(ch.encode()).decode()

print(shellcode)
