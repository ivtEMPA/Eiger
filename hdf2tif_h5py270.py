#!/usr/bin/env python

"""
usage: hdf2tif.py [-h] [-o OUTPUT] files [files ...]

convert EIGER hdf data sets to tif file

positional arguments:
  files                 list of master hdf files

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        /path/to/output/basename
"""

import argparse
import os

# try to import albula from site packages
try:
    from dectris import albula
except Exception as e:
    print ("[WARNING] ALBULA API not found in python site-packages, using tifffile and h5py instead.")
    albula = None
    import h5py
    import tifffile
    from bitshuffle import h5


__author__ = "SasG"
__date__ = "16-10-26"

def parseArgs():
    """
    parse user input and return arguments
    """
    parser = argparse.ArgumentParser(description = "convert EIGER hdf data sets to tif file")

    parser.add_argument("files", nargs="+", help="list of master hdf files")
    parser.add_argument("-o", "--output", help="/path/to/output/basename", default=None)
    args = parser.parse_args()

    return args
def printname(name):
    print name

def dataGetter(fname):
    """
    lazy iterator for EIGER h5 data sets
    """
    block_size=0
    with h5py.File(fname,"r") as f:
        data = f["/entry/data/"]
        f.visit(printname)
        #print("{0}".format(data.iteritems()))
        for dset, _ in sorted(data.iteritems()):
            #dcpl = dset.get_create_plist()
            #numfilt = dcpl.get_nfilters()
            #print("Number of filters associated with dataset: %d" % numfilt)
            print("data set methods: {0}".format(dir(data[dset])))
            print("data set value: {0}".format(data[dset].value))
            print("data set shape: {0}".format(data[dset].len()))
            print("data set type : {0}".format(data[dset].dtype))
            print("data set name : {0}".format(data[dset].name)) 
            print("data {0}".format(data[dset][1,1,1]))
            for i in range(data[dset].len()):
                yield data[dset][i,:,:]

def h5pyConversion(fname, outputBasename):
    """
    use h5py and tifffile to convert hdf data sets to .tiff files
    return the number of saved files
    """
    imagenumber = 1
    print ("Filename: {0}".format(fname))
    for data in dataGetter(fname):
        try:
            output = outputBasename + "_%04d.tif" %imagenumber
            print ("[*] saving %s" %output)
            tifffile.imsave(output, data)
            imagenumber += 1
        except Exception as e:
            print (e)

    return imagenumber

def albulaConversion(fname, outputBasename):
    """
    use ALBULA API to convert hdf data sets to .tif files
    return the number of saved files
    """
    series = albula.DImageSeries(fname)
    for i in range(series.first(), series.first() + series.size()):
        output = outputBasename + "_%04d.tif" %i
        print ("[*] saving %s" %output)
        albula.DImageWriter.write(series[i], output)
    return i
    

if __name__ == "__main__":
    args = parseArgs()
    basename = args.output
    filenumber = 1
    for f in args.files:
        if args.output is None:
            basename, _ = os.path.splitext(f)
        print ("[*] working on %s" %f)
        if albula:
            imagenumber = albulaConversion(f, basename + "_%02d" %filenumber)
        else:
            imagenumber = h5pyConversion(f, basename + "_%02d" %filenumber)

        print ("[*] wrote %d tif files" %imagenumber)
        filenumber += 1
    
