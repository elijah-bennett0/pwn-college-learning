# this line shows that the first 4 bytes of the .cimg file should be CNMg. simply putting that into a .cimg gives
# the flag.
# assert header[:4] == b"CNMg",

printf 'CNMg' > test.cimg
python3 cimg test.cimg
