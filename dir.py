import os
import sys
import argparse

def parse():
	parser = argparse.ArgumentParser(description="convert EIGER data by using hdf2tif.py")
	parser.add_argument("-d","--dirs", nargs="+", help="list of the dirs")
	parser.add_argument("-f","--file", help="path/to/filelist",default=None)
	args = parser.parse_args()
	return args

if __name__ == "__main__":
    args = parse()
    dirs = []
    if args.file is None:
	    dirs = args.dirs
    else:
	    # read lines in the file
	    with open(args.file) as fp:
		    for line in fp:
			    dirs.append(line.strip())
	    
    for id in dirs:
	print id
	for root, dirs, files in os.walk(id):
		for file in files:
			if file.endswith("_master.h5"):
				print os.path.join(root, file)
				rest = file.index("_master.h5")
				# create TIFF directory
				if not os.path.exists(root+"\\TIFF"):
    					os.makedirs(root+"\\TIFF")
				#print file[:rest]
				os.system("python hdf2tif_h5py270.py " + os.path.join(root, file) + " -o " + root + "\\TIFF\\" + file[:rest])
