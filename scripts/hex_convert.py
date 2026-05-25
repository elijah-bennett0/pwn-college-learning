import sys
import argparse

parser = argparse.ArgumentParser(prog='hex_convert')
parser.add_argument("number", help="Number to convert")
parser.add_argument('-e', default="little", choices=["little", "big"], help="Endianness")
parser.add_argument('-s', default=None, type=int, help="Size in bytes of output")

# example: hex_convert 79 -o hex -e little -> 4f000000

def main():
	args = parser.parse_args()
	print((lambda n, size, endian: int(n,0).to_bytes(size, endian).hex() if size else int(n,0) if n.startswith("0x") else hex(int(n,0)))(args.number, args.s, args.e))


if __name__ == "__main__":
	main()
