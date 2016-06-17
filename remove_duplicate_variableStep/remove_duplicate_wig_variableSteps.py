#!/usr/bin/python

import sys

def usage():
    print "usage: python remove_duplicate_wig_variableSteps.py <in.wig> <out.wig>"
    sys.exit(2)


def main():
    if (len(sys.argv) != 3):
        usage()

    infile = sys.argv[1]
    outfile = sys.argv[2]
    print "infile [", infile,"] outfile [", outfile,"]"

    in_fh = open(infile, "r")
    out_fh = open(outfile, "w")

    curr = "INIT"

    for line in in_fh:
        if line.find("variableStep") != -1 and line != curr:
#            print "curr is [",curr,"] and line is [",line,"]"
            curr = line
            out_fh.write(line)
        elif line.find("variableStep") == -1 :
            out_fh.write(line)

    in_fh.close()
    out_fh.close()
    return

main()
