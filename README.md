# ABOOT HDD Image Converter
A small tool to convert Amiga PC Bridgeboard (A2088/A2286/A2386) virtual HDD files to hard disk images usable with DOSBox or Bochs DOS emulators on Windows/Linux/Mac and vice versa.

Since Amiga PC virtual hard files are raw HDD files with only a small header (containing geometry), you can not use it out-of-the-box with a DOS emulator on Windows/Linux/Mac like DOSBox or bochs. You need to convert this file and that is what this tool can do:

**ABoot Amiga HDD file => DOSBox HDD File**

**DOSBox HDD File => ABoot Amiga HDD file**

Usefull if you want to create hard disk files for your Amiga Bridgeboard on Mac/Windows/Linux or to read and modify these files with DOSBox / Bochs.

# How to use
## Create a PC virtual disk image for Amiga PC Bridgeboard (A2088/A2286/A2386) on a Mac/Linux/Windows

Create a new hard image with tool 'bximage' from bochs:

```
========================================================================
                                bximage
  Disk Image Creation / Conversion / Resize and Commit Tool for Bochs
         $Id: bximage.cc 13481 2018-03-30 21:04:04Z vruppert $
========================================================================

1. Create new floppy or hard disk image
2. Convert hard disk image to other format (mode)
3. Resize hard disk image
4. Commit 'undoable' redolog to base image
5. Disk image info

0. Quit

Please choose one [0] 1

Create image

Do you want to create a floppy disk image or a hard disk image?
Please type hd or fd. [hd] hd

What kind of image should I create?
Please type flat, sparse, growing, vpc or vmware4. [flat] flat

Choose the size of hard disk sectors.
Please type 512, 1024 or 4096. [512] 512

Enter the hard disk size in megabytes, between 10 and 8257535
[10] 10

What should be the name of the image?
[c.img] PCHARDDISK.img

Creating hard disk image 'PCHARDDISK.img' with CHS=20/16/63 (sector size = 512)

The following line should appear in your bochsrc:
  ata0-master: type=disk, path="PCHARDDISK.img", mode=flat
```

Now mount the created image in DOSBox (or bochs):

```
IMGMOUNT 2 <PathTo>/PCHARDDISK.img -size 512,63,16,20 -t hdd -fs none
```

Boot with MSDOS 6.22 floppy image (swap floppy files with CTRL-F4 keys):

```
boot DOS622-1.img DOS622-2.img DOS6.22-3.img -l c
```

Format the hard disk file:

```
format c: /s
```

Install (MS)DOS:

```
A:setup
```

Do what ever you like to do with the fresh created (MS)DOS image...

Convert raw DOSBox hard disk image to ABOOT file usable for PC Bridgeboard:


```
./AbootConverter.py PCHARDDISK.img 
==========================================
Amiga Bridgeboard Aboot HDD file converter
(V0.2 by Heiko Prüssing in 2021,2022)

Using file: PCHARDDISK.img
Detected file type: 'flat HDD image Bochs / DOSBox'.
Converting file to a Commodore Bridgeboard autoboot harddisk image file...
Output file name? (default 'PCHARDDISK.aboot-out'): 
Please enter the hardfile geometry:'
Cylinders [1..1024] (default 20) : 20
Headers   [1..16]   (default 16) : 16
Sectors   [1..64]   (default 63) : 63

Resulting hard disk file size: 10322432 (bytes).
Usable for DOS will be 9 MB.
Successfully. Now you can use 'PCHARDDISK.aboot-out' as a autoboot harddisk file for your Amiga Bridgeboard. Have fun ;)
```

Copy the file to your Amiga.

Adjust the content of ```sys:PC/system/aboot.ctrl``` (main configuration of the Bridgeboard) to point to the new image file.

Restart. Amiga PC bridgeboard should now boot from fresh created hard disk image.

Enjoy :-) 
