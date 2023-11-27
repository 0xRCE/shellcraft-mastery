#!/usr/bin/env python3
#xpl-challenge1.py

from pwn import *
context.os = 'linux'
context.arch = 'amd64'

binary = './challenge1'

if args.DEBUG:
    io = gdb.debug(binary)
else:
    io = process(binary)
    
def not_implemented_shellcode(func):
    msg=f"\n=======>{func} not implemented!\n\n"
    sc= shellcraft.write(1,msg,len(msg))
    sc+=shellcraft.exit(0)
    return sc
    
def spawn_shell():
    return not_implemented_shellcode("shell")    

def print_flag():
    return not_implemented_shellcode("open flag.txt") 
    
def echo():
    return not_implemented_shellcode("echo server")  

banner = io.recvuntil(b'shellcode:')
############output process output
print()
print(banner.decode('utf-8'))
print()


if args.ECHO:
    shellcode = echo()
elif args.FLAG:
    shellcode = print_flag()
elif args.SHELL:
    shellcode = spawn_shell()
else:
    log.success("Please implement your shellcode, this just an example.")
    log.success("There are a lot of ways to implement this, depending on you knowledge-level you could use:\n- Machine-code\n- Pwn-tools shellcraft\n- Plain assembly\n- msfvenom -f python -p linux/x64/<some-payload>\n- https://shell-storm.org/shellcode  (see under 'Linux' section Intel x86-64)")
    shellcode = b"\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x7d\x21\x0b\x0b\x0b\x01\x01\x01\x48\x31\x04\x24\x48\xb8\x7c\x7c\x20\x20\x20\x20\x20\x7c\x50\x48\xb8\x20\x20\x20\x20\x20\x20\x20\x20\x50\x48\xb8\x20\x20\x20\x20\x20\x20\x20\x20\x50\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x2c\x2c\x2c\x76\x21\x7d\x0b\x21\x48\x31\x04\x24\x48\xb8\x20\x20\x20\x20\x20\x7c\x7c\x2d\x50\x48\xb8\x20\x20\x20\x20\x20\x20\x20\x20\x50\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x5d\x2e\x5d\x0b\x21\x21\x21\x21\x48\x31\x04\x24\x48\xb8\x20\x20\x20\x20\x20\x20\x20\x29\x50\x48\xb8\x20\x20\x20\x28\x5f\x5f\x29\x5c\x50\x48\xb8\x20\x20\x20\x20\x20\x20\x20\x20\x50\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x5e\x5e\x5e\x5e\x5e\x0b\x21\x21\x48\x31\x04\x24\x48\xb8\x20\x28\x6f\x6f\x29\x5c\x5f\x5f\x50\x48\xb8\x20\x20\x20\x20\x20\x20\x5c\x20\x50\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x5e\x5f\x21\x0b\x21\x21\x21\x21\x48\x31\x04\x24\x48\xb8\x20\x20\x5c\x20\x20\x20\x5e\x5f\x50\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x0b\x21\x21\x21\x21\x21\x21\x21\x48\x31\x04\x24\x48\xb8\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x50\x48\xb8\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x50\x48\xb8\x20\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x50\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x6c\x71\x6d\x64\x21\x3f\x0b\x21\x48\x31\x04\x24\x48\xb8\x74\x20\x61\x6e\x20\x65\x78\x61\x50\x48\xb8\x73\x20\x69\x73\x20\x6a\x75\x73\x50\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x5e\x5e\x0b\x3d\x21\x55\x69\x68\x48\x31\x04\x24\x48\xb8\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x50\x48\xb8\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x50\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x0b\x21\x21\x5e\x5e\x5e\x5e\x5e\x48\x31\x04\x24\x6a\x01\x5f\x31\xd2\xb2\xd5\x48\x89\xe6\x6a\x01\x58\x0f\x05\x31\xff\x6a\x3c\x58\x0f\x05"

payload = b''
if type(shellcode) == type(b''):
    #no assembling needed, shellcode already in machine format
    payload += shellcode
else:
    payload += asm(shellcode)

if args.DUMP_SHELLCODE:
    print(shellcode)

io.send(payload)

#start interactive session (STDIN, STDOUT and STDERR forwarded to process)
io.interactive()
