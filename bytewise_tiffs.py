import io
import base64

import time

tiff_file = 'C:\\Users\\Kyle\\Desktop\\test_4\\Full resolution\\test_MagellanStack.tif'
"""
f = open(tiff_file, "r")
#str = f.read().decode('utf-16-le')
tags = f.read(1)
print(tags)
"""
"""
f = open(tiff_file, "rb")
print(type(f))
for b in f:
    #str = b.decode('utf-8')
    #print('NEW BYTE')
    print(b)
    #time.sleep(5)
"""

with open(tiff_file, "rb") as byte_reader:
    print('Standard TIFF Header')
    print(byte_reader.read(8))
    print('Index map offset header (54773648 =  0x0343C790)')
    print(byte_reader.read(4))
    print('Index map offset')
    print(byte_reader.read(4))
    print('Display settings offset header')
    print(byte_reader.read(4))
    print('Display settings offset')
    print(byte_reader.read(4))
    print('Comments offset header')
    print(byte_reader.read(4))
    print('Comments offset')
    print(byte_reader.read(4))
    print('Summary metadata header')
    print(byte_reader.read(4))
    print('Summary metadata length')
    print(byte_reader.read(4))
    print('Summary metadata')
    print(byte_reader.read(479))
    #print(byte_reader.seek(519))
    print('Index map 4 byte header')
    print(byte_reader.read(4))

