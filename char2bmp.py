__author__ = "Adam Mnemonic"
__version__ = "1.0"

'''
Use this utility to convert rom dumps of Commodore 64 Character Generator
to monochrome bitmap. Charmap is stored in 4kB chips marked as:

325056-03
901225-01
325018-02
901225-01
325018-02
906143-02

'''

import math, struct, argparse


# PARSE ARGUMENTS
parser = argparse.ArgumentParser(description='Convert charmap to bmp')
parser.add_argument('-i',nargs=1, required=True, metavar='char_rom.bin'    , help='4kB rom dump of CHARGEN')
parser.add_argument('-o',nargs=1, required=True, metavar='char_bitmap.bmp' , help='Bitmap with Charset')
args = parser.parse_args()



li = lambda n: struct.pack("<i", n) #dword

def bmp(rawdata, w, h):
    rawdata  = list(rawdata)
    bitdata  = [0]*len(rawdata)

    #transpone ROM to bitfields
    for y in range(0, 16): #16 rows
        for x in range(0,32): #32 chars in row
                for l in range(0,8): #8 bytes for single character
                    bitdata[(32*l) + (31-x) + (256*y)] = rawdata[l + (x*8) + (y*32*8)]

    return (b"BM"               + #signature 2bytes \x42\x4D
            b"\x00\x00\x00\x00" + #filesize  (ignored by most editors) 
            b"\x00\x00\x00\x00" + #reserved
            b"\x3E\x00\x00\x00" + #bfOffBits
            b"\x28\x00\x00\x00" + #headerszie always 0x28
            li(w)               + #biWidth
            li(h)               + #biHeight
            b"\x01\x00"         + #planes always1
            b"\x01\x00"         + #bitcount 1=monochrome
            b"\x00\x00\x00\x00" + #compression
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" +
            b"\x00\x00\x00\x00\x00\x00\x00\x00" +
            b"\xff\xff\xff\x00" + #colors[0]
            b"\x00\x00\x00\x00" + #colors[1]
            b"".join([bytes(reversed(bitdata))])
            )




with open(args.i[0],'rb') as inf:
    buff = inf.read()


with open(args.o[0], "wb") as outf:
    outf.write(   bmp(buff,256,128)   )
