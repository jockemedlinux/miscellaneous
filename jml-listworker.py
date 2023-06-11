#!/usr/bin/env python3
#Listworker.py : @jockemedlinux 2022-07-13#
import itertools, argparse
parser = argparse.ArgumentParser('Listworker.py')
parser.add_argument("inputfile1", help="First input filename")
parser.add_argument("inputfile2", help="Second input filename")
parser.add_argument("outputfile", help="Output filename")
parser.add_argument("seperator", type=str, help="Choose your seperator")
args = parser.parse_args()
open(args.outputfile, "a").close()
with open(args.inputfile1, "r") as file1, open(args.inputfile2, "r") as file2, open(args.outputfile, "w") as output:
	for x, y in itertools.product(file1, file2):
		newfile = f'{x.strip()}{args.seperator}{y.strip()}\n'
		#print(newfile.strip())
		output.writelines(newfile)
