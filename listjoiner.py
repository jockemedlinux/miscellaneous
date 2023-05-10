#!/usr/bin/env python3
#Listjoiner.py : @jockemedlinux 2022-08-09#
import argparse
parser = argparse.ArgumentParser('Listjoiner.py')
parser.add_argument("inputfile1", help="Insert list1")
parser.add_argument("inputfile2", help="Insert list2")
parser.add_argument("outputfile", help="Output filename")
args = parser.parse_args()

list1 = []
list2 = []

with open(args.inputfile1) as usernames:
	for x in usernames:
		list1.append(x)
with open(args.inputfile2) as passwords:
	for x in passwords:
		list2.append(x)
with open(args.outputfile, "w") as newfile:
	for x, y in zip(list1, list2):
		newfile.write(x.replace('\n', ":") + y)
