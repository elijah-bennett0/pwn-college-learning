from pwn import *

width = 275
height = 1

payload  = b'cIMG'
payload += p16(1)
payload += p32(width)
payload += p8(height)

# cmp edx, 0x113 -> 275
payload += b'A' * 275
payload += b' ' * (width * height - 275)

open('/tmp/test.cimg', 'wb').write(payload)
