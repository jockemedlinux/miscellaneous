#!/usr/bin/env python3

from base64 import b64encode
import sys

string = input("Enter command: ")
print(b64encode(string.encode('UTF-16LE')))