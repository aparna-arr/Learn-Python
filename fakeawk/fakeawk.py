#!/usr/bin/python

import sys

'''
  input: <filename>
  output: stats on
    total bp in file
    avg length in file
    total lines/peaks in file
'''

if len(sys.argv) < 2 :
    print "usage: python fakeawk.py <input bed file>"
    sys.exit()

infile = open(sys.argv[1], "r")

total_bp = 0
linecount = 0
genome = 2725765481

for line in infile :
    lineAr = line.split()

    if (lineAr[0] == "track" or lineAr[0] == "#"):
        continue

    chrom = lineAr[0]
    start = int(lineAr[1])
    end = int(lineAr[2])

#    print chrom, "", start, "", end
    linecount += 1 # there is no ++ in python!!!
    total_bp += end - start

print "STATS"
print "avg len:", total_bp/linecount
print "total bp:", total_bp
# python defaults to INT!
print "perc genome (mm9):", (float(total_bp) / float(genome) * 100)
print "total peaks:", linecount
