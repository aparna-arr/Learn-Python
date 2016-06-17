#!/usr/bin/python

import sys, getopt

def usage():
    print "usage: python count_wig_chrs.py -i file.wig"
    sys.exit()

def main():

    if (len(sys.argv) < 2):
        usage()

    opts, args = getopt.getopt(sys.argv[1:], "hi:")

    myfile = ""
    for opt, arg in opts:
        if opt == '-h':
            usage();
        elif opt == '-i':
            myfile = arg
        else:
            usage()

    fh = open(myfile, "r")

    chrs = dict()
    chrs_peak = dict()

    for line in fh:
        if (line.find("variableStep") != -1):
            trash, keep = line.split("chrom=")
            chrom, trash = keep.split(" ")
#            print "chrom:",chrom

            if chrom not in chrs:
                chrs[chrom] = 1
            else:
                chrs[chrom] = chrs[chrom] + 1

        else:
                if chrom not in chrs_peak:
                    chrs_peak[chrom] = 1    
                else:
                    chrs_peak[chrom] = chrs_peak[chrom] + 1

    fh.close()

    for chrom in chrs:
        print chrom,": [",chrs[chrom],"] : [",chrs_peak[chrom],"]"
       

main() 
