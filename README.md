##Disclaimer - none of the tools listed in this repository is to be used in a malicious or nefarious way. All scripts are made in educational purposes and made to be tested/used on your own applications.

## jml-php-upload.php
This is just an easy way to quickly transfer files via PUT or HTTP. The file will be uploaded to the directory from where the server is started. Make sure the directory has the correct permissions in order for this to work properly. (rename the file to index.php for easier handling)

Can be used in different ways.
Use it either with php-server, apache2, or nginx.

For use with php-server
```
php -S 0.0.0.0:80
```
a) Either navigate to the address and use the form and upload a file

or

b) Use curl with PUT¹ or POST.
```
curl -XPOST -F "file=@file.txt" -F "path=/" http://ip-to-your-php-server/
```
(1) For PUT you need to use a PUT supported webserver, like nginx or apache2. Once configured properly you can use this command.
```
curl -T file.txt http://ip-to-your-PUT-server/
```
# List tools

## Listjoiner
Easy as it sounds. Joins two lists of your choice into a file with a ":" seperator. 
```
./jml-listjoiner.py firstnames.txt surnames.txt joinednames.txt
```
## Listworker
Easy as it sounds. Joins two lists of your choice into a file with a specified seperator.
```
./jml-listworker.py firstnames.txt surnames.txt joinednames.txt ':'
```

# Scraping tools

## egrabber.py
Grabs the emails of a site and parses emails and usernames into seperate files.
```
./jml-egrabber.py http://localhost
```

## MAC-lookup.py
Searches for company and country of provided MAC address
![bild](https://user-images.githubusercontent.com/123998153/228343138-110a744d-e8f4-4a04-9a2e-2f614a5803ce.png)
```
./jml-MAC-lookup.py 
xx:xx:xx:xx:xx:xx
```
# Scanning Tools 

## jml-portscanner.py
Super simple not so good portscanner.
```
└─$ python3 jml-portscanner.py -H 127.0.0.1 -P 65535

 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |J|M|L|-|p|o|r|t|s|c|a|n|n|e|r|
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

[+] Port 21 is open
[+] Port 22 is open
[+] Port 44 is open
[+] Port 80 is open
[+] Port 65535 is open
```

## jml-filetransfer.py
Simple and stealthy webserver which allows file PUT and file POST for encrypted filetransfer..
```
└─$ ./jml-filetransfer.py  -h
usage: jml-filetransfer.py [-h] [-i I] [-p P]

options:
  -h, --help  show this help message and exit
  -i I        specify ip to listen on.
  -p P        specify port to listen on.

```

# Other Tools

## jml-ShellShock.py
Easy script to exploit the shellshock vulnerability. Only tested on virutal vulnhub machine symfonos3.
```
./jml-ShellShock.py -U http://symfonos.local/cgi-bin/underworld/
[+] What is your command?: cat /etc/passwd
```



