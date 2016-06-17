#!/usr/bin/python

import sys, getopt


def usage():
    print "usage: python process_peak_gff.py -i <in.gff> -o <out.bed> -n <track name>"
    sys.exit(2)

def main():
    if (len(sys.argv) <= 1):
        usage()

    opts,args = getopt.getopt(sys.argv[1:], "i:o:n:")

    infile = "INIT"
    outfile = "INIT"
    name = "PEAKBED"

    for opt,arg in opts:
        if opt == '-i':
            infile = arg
        elif opt == '-o':
            outfile = arg
        elif opt == '-n':
            name = arg
        else:
            usage()

    if (infile == "INIT" or outfile == "INIT" or infile == outfile):
        print "ERROR: Your infile and/or outfile are not set OR are the same file!"
        usage()
    
    fh = open(infile, "r")
    fh_out = open(outfile, "w")

    fh_out.write("track name=\"" + name + "\"\n")

    for line in fh:
        if (not line.startswith("chr")):
            continue
    
        lineAr = line.split()

        fh_out.write(lineAr[0] + "\t" + lineAr[3] + "\t" + lineAr[4] + "\n")

    fh.close()
    fh_out.close()       
        
main()
