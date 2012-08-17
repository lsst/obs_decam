#!/usr/bin/env python

""" Rename SST files to the following layout:

/path/to/root/$FIELD/$DATE/$YEAR$DOY_$SOD.fits
"""

import os
import re
import sys
import shutil
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", required=True, help="Root directory for output files.")
parser.add_argument("-f", "--field", required=True, help="Field name")
parser.add_argument("-x", "--execute", action="store_true", default=False,
                    help="Actually execute the renames?")
parser.add_argument("-c", "--copy", action="store_true", default=False,
                    help="Copy instead of move the files?")
parser.add_argument("-l", "--link", action="store_true", default=False,
                    help="Link instead of move the files?")
parser.add_argument("files", nargs="+", help="Names of file")

def getFrameInfo(filename):
    filename = os.path.basename(filename)
    year, doy, frac = re.search(r"(\d{4})(\d{3})_(\d{6})", filename).groups()

    #hours = int(frac*24/10**6)
    #sec = frac*86400/10**6 - hours*3600

    date = (datetime.date(int(year), 1, 1) + datetime.timedelta(days=int(doy)-1)).isoformat()    


    return {'year': year,
            'doy': doy,
            'frac': frac,
            'date': date,
            }

def getFinalFile(root, field, filename):
    """ Return the final filename from the passed in info dictionary. """
    info = getFrameInfo(filename)
    return os.path.join(root, field, info['date'], os.path.basename(filename))

def main():
    args = parser.parse_args()

    if args.copy and args.link:
        sys.stderr.write("May only set one of --copy and --link")
        raise SystemExit()

    for infile in args.files:
        outfile = getFinalFile(args.root, args.field, infile)

        if args.execute:
            # Actually do the moves. 
            outdir = os.path.dirname(outfile)
            try:
                if not os.path.isdir(outdir):
                    os.makedirs(outdir)
                if args.copy:
                    shutil.copyfile(infile, outfile)
                    print "copied %s to %s" % (infile, outfile)
                elif args.link:
                    os.symlink(os.path.abspath(infile), outfile)
                    print "linked %s to %s" % (infile, outfile)
                else:
                    os.rename(infile, outfile)
                    print "moved %s to %s" % (infile, outfile)
            except Exception, e:
                sys.stderr.write("failed to move or copy %s to %s: %s\n" % (infile, outfile, e))
        else:        
            print infile, outfile

if __name__ == "__main__":
    main()
