# if (cimg.header.magic_number[0] != '{' || cimg.header.magic_number[1] != 'n' || cimg.header.magic_number[2] 
# != 'm' || cimg.header.magic_number[3] != '6')
#

printf '{nm6' > test.cimg
./cimg2 test.cimg
