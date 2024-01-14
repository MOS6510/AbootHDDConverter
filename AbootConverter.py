#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Amiga Bridegboard autoboot harddisk file binary image converter.
   Converts a raw HDD image (e.g. from "DOSBox" or "bochs" DOS emulator
   to a Amiga virtual PC disk HDD image usable from a Commodore Bridgeboard and
   vice versa)

   Written by Heiko Prüssing in 2021,2022
"""

import sys
import struct
import fileinput
import os
import math

sectorSize = 512
abootHeaderSize = 512


def inputNumber(str, min, max, default) -> int:
    while True:
        try:
            valstr = input(str)
            if len(valstr) == 0:
                valstr = ("%d" % default)
            val = int(valstr)
            if val < min or val > max:
                print(
                    "Error, the number must be in range [%d..%d]" % (min, max))
            else:
                return val
        except ValueError:
            print("Please enter a valid integer!")


def detectFlatHardDiskGeometry(filename):
    # Detect geometry of a flat harddisk file.abootHeaderSize
    # Take the file size and create a proper CHS for that.
    realFileSize = os.path.getsize(filename)
    # print("realsize size = %d" % realFileSize)
    cylinders = math.ceil(realFileSize / 16.0 / 63.0 / 512.0)
    # print("recalculated size = %d" % (cylinders * 16 * 63 * 512) )
    return (cylinders, 16, 63)


def detectFlatImage(filename):
    result = False
    fin = open(filename, "rb")
    fin.seek(0x1BC)
    id = struct.unpack(">H", fin.read(2))
    if id[0] == 0x5a5a or id[0] == 0x0000:
        fin.seek(0x1FE)
        id = struct.unpack(">H", fin.read(2))
        if id[0] == 0x55AA:
            result = True
    fin.close()
    return result


def main(argv):
    print("==========================================")
    print("Amiga Bridgeboard Aboot HDD file converter\n(V0.2 by Heiko Prüssing in 2021,2022)\n")
    if len(argv) <= 1:
        print("Usage: %s <HDDimagefile>" % (argv[0]))
        exit()
    filename = argv[1]

    print("Using file: %s" % filename)

    # Check if it is a ABOOT Amiga image or raw HDD image (from bochs or DOSBox)
    fin = open(filename, "rb")
    abootHeader = struct.unpack(">8sHHH", fin.read(14))
    if abootHeader[0] == b"ABOOT\0\0\0":

        # Aboot HDD file:
        heads = abootHeader[1]
        sectors = abootHeader[2]
        cylinders = abootHeader[3]

        print("Detected file type: 'Amiga PC ABOOT HDD image file'.")
        print("Detected geometry: Cylinders=%d heads=%d sectors=%d" % (cylinders, heads, sectors))
        print("Convert to a DOSBox / Bochs HDD image ('flat raw HHD image')...")
        
        filenameout = filename.split(".")[0]+".img-out"
        ofilestring = input('Output file name? (default \'{}\'): '.format(filenameout))
        if ofilestring == "":
            ofilestring = filenameout

        print("Skipping rest of ABOOT header...")
        fin.read(abootHeaderSize - 14)

        print("Writing stripped HDD image file...")
        fout = open(filenameout, "wb")
        fout.write(fin.read())
        fout.close()
        print("Success! You can mount the image now with DOSBox command:\n")
        print(" IMGMOUNT C %s -size 512,%d,%d,%d -t hdd\n" % (filenameout, sectors, heads, cylinders))

    elif detectFlatImage(filename):
        # Raw HDD image (from Bochs or DOSBOX)
        print("Detected file type: 'flat HDD image Bochs / DOSBox'.")
        print("Converting file to a Commodore Bridgeboard autoboot harddisk image file...")

        filenameout = filename.split(".")[0]+".aboot-out"
        ofilestring = input( 'Output file name? (default \'{}\'): '.format(filenameout) )
        if ofilestring == "":
            ofilestring = filenameout

        # Try to detecting the CHS geometry from the MBR of the file
        chs = detectFlatHardDiskGeometry(filename)

        print("Please enter the hardfile geometry:'")
        cylinders = inputNumber("Cylinders [1..1024] (default %d) : " % chs[0], min=1, max=1024, default=chs[0])
        heads     = inputNumber("Headers   [1..16]   (default %d) : " % chs[1], min=1, max=16,   default=chs[1])
        sectors   = inputNumber("Sectors   [1..64]   (default %d) : " % chs[2], min=1, max=64,   default=chs[2])

        harddisksize = (sectorSize * heads * sectors * cylinders)

        print("\nResulting hard disk file size: %d (bytes)." % (harddisksize + abootHeaderSize) )
        print("Usable for DOS will be %d MB." % (harddisksize / 1024 / 1024) )

        # Insert the "ABOOT header" which is a 512 bytes block in front of the hdd image file
        fin.close()
        fin  = open(filename, "rb")
        fout = open(ofilestring,"wb")
        fout.write(struct.pack(">8sHHH",
                               b"ABOOT\0\0\0",
                               heads,
                               sectors,
                               cylinders))
        fout.write(bytearray(b'\xf6'*(sectorSize - 14)))
        # Take over the rest of the hardfile...
        fout.write(fin.read())
        fout.close()
        fin.close()
        print("Successfully. Now you can use '%s' as a autoboot harddisk file for your Amiga Bridgeboard. Have fun ;)" % (ofilestring) )

    else:
        print("Unknown harddisk file type...")

    fin.close()


if __name__ == "__main__":
    main(sys.argv)
