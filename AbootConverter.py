#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Amiga Bridegboard Aboot HDD binary image converter.
   Converts a raw HDD image (e.g. from "DOSBox" or "bochs" DOS emulator
   to a Amiga virtial PC disk HDD image usable from a Commodore Bridgeboard)

   Written by Heiko Pruessing in 2021
"""

import sys,struct,fileinput

def main(argv):
  print("Amiga Bridgeboard Aboot HDD file converter V0.1 by Heiko Pruessing in 2021\n")
  if len(argv) <= 1:
      print("Usage: %s <HDDimagefile>" % (argv[0]))
      exit()
  filename=argv[1]

  # Check if it is a ABOOT Amiga image or raw HDD image (from bochs or DOSBox)
  fin  = open(filename, "rb")
  abootHeader = struct.unpack(">8sHHH", fin.read(14))
  if abootHeader[0] == b"ABOOT\0\0\0":

      # Aboot HDD file:
      heads = abootHeader[1]
      sectors = abootHeader[2]
      cylinders = abootHeader[3]

      print("File '%s' seems an Amiga PC ABOOT HDD image with geometry:\n\n heads=%d\n sectory=%d\n cylinders=%d\n" % (filename, heads, sectors, cylinders))
      ch = input("Convert to a DOSBox / Bochs HDD image ('raw HHD image') (y/n) ?")
      if ch == 'y':
          filenameout = filename.split(".")[0]+".img-out"
          fout=open(filenameout, "wb")
          fout.write(fin.read())
          fout.close()
          print("Finished. You can mount the image now with DOSBox command:\n")
          print(" IMGMOUNT C %s -size 512,%d,%d,%d -t hdd" % (filenameout,sectors,heads,cylinders) )
      else:
          print("bye bye...")
  else:

      # Raw HDD image (from Bochs or DOSBOX)
      print("File '%s' seems a raw HDD image from Bochs / DOSBox." % (filename) )
      ch = raw_input("Should the file be converted to a Amiga PC virtual HDD image (usable as hard disk for a Amiga Bridgeboard) [y/n]? ")
      if ch == 'y':
          filenameout = filename.split(".")[0]+".aboot-out"
          ofilestring = raw_input( 'Output file? (Default \'{}\'): '.format(filenameout) )
          if ofilestring == "":
              ofilestring = filenameout
          heads     = int(raw_input("headers : "))
          sectors   = int(raw_input("sectors : "))
          cylinders = int(raw_input("cylinders : "))

          harddisksize = (512 * heads * sectors * cylinders)
          print("\nThe hard disk will be of file size %d (bytes)" % (harddisksize + 512) )
          print("Usable for DOS will be %d (bytes)" % (harddisksize) )

          # Writing the "ABOOT" header as a 512 bytes header to the hdd image file
          fout = open(ofilestring,"wb")
          fout.write(struct.pack(">8sHHH",
                                  b"ABOOT\0\0\0",
                                  heads,
                                  sectors,
                                  cylinders))
          fout.write(bytearray(b'\xf6'*(512-14)))
          fout.close()
          print("Copy the file '%s' to your Amiga and use it as a PC virtual harddisk for a Bridgeboard." % (ofilestring) )

      else:
          print("bye bye...")

  fin.close()


if __name__ == "__main__":
    main(sys.argv)
