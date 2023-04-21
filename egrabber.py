#!/usr/bin/env python3
#egrabber.py : @jockemedlinux 2022-08-05 :EASY EMAIL-GRABBER#
#Version v1.2: Parsing possible usernames                   #
#############################################################
import requests, argparse, re, itertools
try:    
    parser = argparse.ArgumentParser('egrabber.py')
    parser.add_argument("URL", help="Input the URL")
    args = parser.parse_args()
    targeturl = requests.get(args.URL, headers={"user-agent": "e-grabber v1.2"})
    econtent = re.findall(r'[A-Za-z0-9\.-]+[@][A-Za-z0-9\.-]+[.]{,5}', targeturl.text)
    ucontent = re.findall(r'[A-Za-z0-9.-]+@', targeturl.text)
#####EMAIL SECTION#####
    email_list = []
    for emails in econtent:
        if emails not in email_list:
            email_list.append(emails)
    if email_list:
        print("-" * 65)
        print(f"Emails found on this page:\t {args.URL}")
        print("-" * 65)
        for emails in email_list:
            print(emails)
        with open('emails.txt', 'w') as userfile:
            for x in itertools.product(email_list):
                for y in x:
                    userfile.writelines(y +"\n")
    else:
        print("-" * 65)
        print(f"Could not find any emails on this page:\t {args.URL}")
        print("-" * 65)
#####NAMES SECTION#####
    usernames_list = []
    for names in ucontent:
        if names not in usernames_list:
            usernames_list.append(names)
    if usernames_list:
        print("-" * 65)
        print(f"Usernames found on this page:\t {args.URL}")
        print("-" * 65)
        for names in usernames_list:
            print(names.replace("@", ''))
        with open('usernames.txt', 'w') as namefile:
            for x in itertools.product(usernames_list):
                for y in x:
                    namefile.writelines(y.replace("@",'') +"\n")
        print("\n")
        print(":" * 65)
        print("Emails saved in:\t emails.txt")
        print("Usernames saved in:\t usernames.txt")
        print(":" * 65)
    else:
        print("-" * 65)
        print(f"Could not find any usernames on this page:\t {args.URL}")
        print("-" * 65)
except KeyboardInterrupt:
    print("\n\nShutting down...")
except:
    print("\nCould not properly parse host. Recheck your URL")