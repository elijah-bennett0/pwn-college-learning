from pwn import *

magic_number = b"cIMG"
version = p16(2)

# 1x4
width = p8(1)
height = p8(4)


# char desired_output[] = "\x1b[38;2;231;017;130mc\x1b[0m\x1b[38;2;179;172;090mI\x1b[0m\x1b[38;2;228;104;104mM\x1b[0m\x1b[38;2;206;189;205mG\x1b[0m\x00";
# if (cimg.num_pixels != sizeof(desired_output)/sizeof(term_pixel_t)) -> 102 / 24 = 4
size = 4

# color codes come from the desired_output ; as well as the desired characters cimg
colors = {b'c':bytes([0xE7,0x11,0x82]), b'I':bytes([0xB3,0xAC,0x5A]), b'M':bytes([0xE4,0x68,0x68]), b'G':bytes([0xCE,0xBD,0xCD])}
data = b''

for k,v in colors.items():
	data+=v+k

payload = b''

payload+=magic_number+version+width+height+data

with open("/tmp/test.cimg", 'wb') as file:
	file.write(payload)
