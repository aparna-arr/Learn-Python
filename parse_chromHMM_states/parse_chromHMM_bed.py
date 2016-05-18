#!/usr/bin/python

import sys # needed for CLI args and exit
from collections import defaultdict # needed to make dict of lists

print "Total arguments: ", len(sys.argv)

if (len(sys.argv) < 4) :
    print "\nusage: <ChromHMM dense bed file output> <list of states space seperated> <outfile name>\n"
    sys.exit()

#print "Script has not exited"
#print "opening file:", sys.argv[1]

infile = open(sys.argv[1],"r")
access = sys.argv[2:len(sys.argv) - 1] # everything between the two file names = a state to access
outfileName = sys.argv[len(sys.argv) - 1]

#print "my access is", access
print "Looking for states:", access

mydict = defaultdict(list)

# reading in whole file then accessing states of interest
for line in infile:
    lineAr = line.split() # default splits on spaces
 
    if (lineAr[0] == "track"):
        continue

    if (lineAr[3] not in mydict):
        mydict[lineAr[3]] = list() # init 

    mydict[lineAr[3]].append(line) # like vector.push_back()


infile.close()

outfile = open(outfileName, "w")

for k in access:
    for i in mydict[k]:
        outfile.write(str(i))

outfile.close()

print "Done."

print "\nWARNING: output sorted by access keys (state #'s) NOT by chr, start\n"
