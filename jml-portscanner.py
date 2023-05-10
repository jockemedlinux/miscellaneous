#!/usr/bin/env python3
#@jockemedlinux 2023-05-04#

import socket,argparse,sys,time
def banner():
	print("""
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |J|M|L|-|p|o|r|t|s|c|a|n|n|e|r|
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		""")
parser = argparse.ArgumentParser(prog="Simple portsscanner", description="It scans specified host for open portss.", epilog="")
parser.add_argument('-H', type=str, default="localhost", help="Host to scan.", required=True)
parser.add_argument('-P', type=int, default="65535", help="ports to scan", required=True)
args = parser.parse_args()
def portscanner(host, port):
	found_open_ports = False
	try:
		for ports in range(1, args.P+1):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			conn = s.connect_ex((str(host), ports))
			if conn == 0:
				print(f"[+] Port {ports} is open")
				found_open_ports = True
				s.close()
			else:
				s.close()
		if found_open_ports == False:
			print("[-] No open ports found")
	except KeyboardInterrupt:
		print("\n User interrupted. Exiting..")
	except socket.gaierror:
		print("\n Somethings wrong with the connection..")
	except:
		print("\n Some other stupid error")
if __name__ == "__main__":
	banner()
	portscanner(args.H, args.P)