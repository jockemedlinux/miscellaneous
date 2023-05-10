#!/usr/bin/env python3
#@jockemedlinux 2022-07-13#
import requests, json, re, sys

mac_address = input("Enter (atleast) first 6 characters of the MAC: ")
url = "https://api.maclookup.app/v2/macs/"

r = requests.get(url + mac_address)
response = r.json()
json_data = re.findall(r'company.*|country.*', json.dumps(response, indent=2))

if json_data:
	print(json_data)
else:
	print("\nCould not find any info. Check your address..")
