#   0x00000000004015de <+222>:	cmp    al,0x5b
#   0x00000000004015e0 <+224>:	jne    0x4015fa <main+250>
#   0x00000000004015e2 <+226>:	movzx  eax,BYTE PTR [rbp-0x1b]
#   0x00000000004015e6 <+230>:	cmp    al,0x6c
#   0x00000000004015e8 <+232>:	jne    0x4015fa <main+250>
#   0x00000000004015ea <+234>:	movzx  eax,BYTE PTR [rbp-0x1a]
#   0x00000000004015ee <+238>:	cmp    al,0x4d
#   0x00000000004015f0 <+240>:	jne    0x4015fa <main+250>
#   0x00000000004015f2 <+242>:	movzx  eax,BYTE PTR [rbp-0x19]
#   0x00000000004015f6 <+246>:	cmp    al,0x67
# ran using gdb gef

printf '\x5b\x6c\x4d\x67' > test.cimg
./cimg test.cimg
