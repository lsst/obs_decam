from __future__ import print_function
import sys
import re
import os
import numpy as np

# python $OBS_DECAM_DIR/examples/cfhtls_wide_to_astrometry_net.py CFHT.txt CFHTLS_W_ugriz_090*cat

nobj = 0
vstack = np.empty((0, 15))
outfile = sys.argv[1]
infiles = sys.argv[2:]
for file in infiles:
    # id       x          y        ra        dec         r2   flag    u
    # g        r        i         z       uerr     gerr     rerr     ierr
    # zerr   e(b-v) u(SExflag) g(SExflag) r(SExflag) i(SExflag)   z(SExflag)
    # dk

    data = np.loadtxt(file, unpack=True, comments="#")
    flags = data[6].astype(np.int)
    isStar = flags & 1                  # star galaxy separation : 0/1  galaxy/star
    isNotSat = np.logical_not(flags & 2)  # saturated star in one of the filters
    isBright = data[9] < 23               # r-band mag
    idx = np.where(isNotSat & isStar & isBright)

    ra = data[3][idx]
    decl = data[4][idx]
    u = data[7][idx]
    g = data[8][idx]
    r = data[9][idx]
    i = data[10][idx]
    z = data[11][idx]
    du = np.sqrt(0.001**2 + data[12][idx]**2)
    dg = np.sqrt(0.001**2 + data[13][idx]**2)
    dr = np.sqrt(0.001**2 + data[14][idx]**2)
    di = np.sqrt(0.001**2 + data[15][idx]**2)
    dz = np.sqrt(0.001**2 + data[16][idx]**2)
    isStar = isStar[idx]
    isVar = np.zeros_like(isStar)
    ids = np.cumsum(np.ones_like(isStar)) + nobj
    nobj = max(ids)

    vstack = np.vstack(
        (vstack, np.array((ids, ra, decl, u, g, r, i, z, du, dg, dr, di, dz, isStar, isVar)).T))

header = "id,ra,dec,u,g,r,i,z,u_err,g_err,r_err,i_err,z_err,starnotgal,variable"
np.savetxt(outfile, vstack, header=header, delimiter=",",
           fmt=["%d", "%.7f", "%.7f", "%.3f", "%.3f", "%.3f", "%.3f", "%.3f", "%.3f", "%.3f", "%.3f", "%.3f", "%.3f", "%.1d", "%.1d"])

print("""
Next you need to grab a new-ish version of astrometry.net

 cd $OBS_DECAM_DIR/../astrometry_net
 wget http://astrometry.net/downloads/astrometry.net-0.50.tar.gz
 tar -xzvf astrometry.net-0.50.tar.gz 
 cd astrometry.net-0.50
 ./configure 
 make
 make install INSTALL_DIR=$PWD/../0.50
 cd ../0.50
 setup -k -r .
 rehash
 
And run the commands to make index files from the outfile defined in sys.argv[1].  If you
have trouble, reference http://astrometry.net/doc/build-index.html

 cd ../astrometry_net_data_decam
 text2fits.py -s "," -f "jddffffffffffjj" outfile.txt outfile.fits
 setenv P 1234567
 build-astrometry-index -i outfile.fits -o index-${P}00.fits -I ${P}00 -P 0 -S r -n 100 -L 20 -E -j 0.4 -r 1 -A ra -d dec

 # DEBUGGED UP TO HERE
 
 build-astrometry-index -1 index-${P}00.fits -o index-${P}01.fits -I ${P}01 -P 1 -S r -L 20 -E -M -j 0.4
 build-astrometry-index -1 index-${P}00.fits -o index-${P}02.fits -I ${P}02 -P 2 -S r -L 20 -E -M -j 0.4
 build-astrometry-index -1 index-${P}00.fits -o index-${P}03.fits -I ${P}03 -P 3 -S r -L 20 -E -M -j 0.4
 build-astrometry-index -1 index-${P}00.fits -o index-${P}04.fits -I ${P}04 -P 4 -S r -L 20 -E -M -j 0.4
 ls index-1234567* | awk '{printf("modhead %s+7 REFCAT '1234567'\\n",$1)}' | sh

We only needed astrometry.net-0.50 to build the index files, so re-setup the default one

 setup astrometry_net
 cp -r $ASTROMETRY_NET_DIR/ups .
 setup -k -r .

And finally, edit script andConfig.py

 vi andConfig.py
   root.starGalaxyColumn = "starnotgal"
   filters = ('u', 'g', 'r', 'i', 'z')
   root.magColumnMap = dict([(f,f) for f in filters])
   root.magErrorColumnMap = dict([(f, f + '_err') for f in filters])
   root.indexFiles = [
       'index-123456700.fits',
       'index-123456701.fits',
       'index-123456702.fits',
       'index-123456703.fits',
       'index-123456704.fits',
       ]
""")
