#!/usr/bin/python

import sys, getopt
from collections import defaultdict

# -a  ==========
# -b    ==  ==
# out ==  ==  ==

def usage():
    print "usage: python intersectV.py -a <bedfile> -b <bedfile>"
    print "\nThis script acts like bedtools intersect -a -b but for -v"
    print "-a  =========="
    print "-b    ==  ==  "
    print "out ==  ==  =="

    print "\nOutput is STDOUT"
    sys.exit()
    

def readBed ( file ):
#    print "Reading file:", file

    peaks = defaultdict(list)

    fh = open(file, "r")

    for line in fh:
        lineAr = line.split("\t")
        peaks[lineAr[0]].append({'start':int(lineAr[1]), 'end':int(lineAr[2]), "intersect": []})
#        print "line is",line.rstrip() # chomp
#        print "peak size is ", len(peaks)
#        print "for key", lineAr[0], "list len is", len(peaks[lineAr[0]])
#        print "just added list element start is:", peaks[lineAr[0]][len(peaks[lineAr[0]]) - 1]["start"]

    fh.close() 
    return peaks
     

def find_intersects(alist, blist):
    b_index = 0

    for a_elem in alist:

        if (b_index > 0):
            if blist[b_index - 1]["start"] <= a_elem["end"] and blist[b_index - 1]["end"] >= a_elem["start"] :
                a_elem["intersect"].append(blist[b_index - 1])
        
        if (blist[b_index]["start"] > a_elem["end"]):
            continue

        while(b_index != len(blist) and blist[b_index]["end"] < a_elem["start"]):
            b_index += 1

        if (b_index == len(blist)):
            break

        while (b_index < len(blist) and blist[b_index]["start"] <= a_elem["end"] and blist[b_index]["end"] >= a_elem["start"]):
            a_elem["intersect"].append(blist[b_index])

            b_index += 1

    return

def handle_intersects(alist, result):

    for a_elem in alist:
        if (len(a_elem["intersect"]) == 0):
            result.append({"start": a_elem["start"], "end": a_elem["end"]})
            continue

        for b_index, b_elem in enumerate(a_elem["intersect"]):
            if a_elem["start"] < b_elem["start"]:
                result.append({"start": a_elem["start"], "end": b_elem["start"] - 1})
                if (a_elem["end"] > b_elem["end"] and b_index == len(a_elem["intersect"]) - 1) :
                    result.append({"start": b_elem["end"] + 1, "end": a_elem["end"]})
                else:
                    a_elem["start"] = b_elem["end"] + 1
    
            else:
                if (a_elem["end"] > b_elem["end"]):
                    if (b_index == len(a_elem["intersect"]) - 1):
                        result.append({"start": b_elem["end"] + 1, "end": a_elem["end"]})
                    else:
                        a_elem["start"] = b_elem["end"] + 1

    return
                    
def main():
    afile = 'INIT'
    bfile = 'INIT'

    if (len(sys.argv) < 3):
        usage()

    opts,args = getopt.getopt(sys.argv[1:],"ha:b:")

#    print "opts is :",opts
 
    for opt,arg in opts:
#        print "opt:", opt, "arg:", arg
        if opt == '-h':
            usage()
        elif opt == '-a':
            afile = arg
        elif opt == '-b':
            bfile = arg
        else:
            usage()

#    print "afile is", afile, "bfile is", bfile
    
    afile_hash = readBed(afile)
    bfile_hash = readBed(bfile)

    final = defaultdict(list)
    for chrom in afile_hash:
        if (chrom not in bfile_hash):
            continue

#       print chrom
    
        find_intersects(afile_hash[chrom], bfile_hash[chrom])
    
        handle_intersects(afile_hash[chrom], final[chrom])

    for chrom in sorted(final, key=final.get):
        for elem in final[chrom]:
            print chrom, "\t", elem["start"], "\t", elem["end"]
         
    return

main()

'''
# attempt #1
    for chrom in afile_hash:
        if (chrom not in bfile_hash):
            continue

        print chrom

        for a_elem in afile_hash[chrom]:        
   
            # a =====
            # b         ======
            if (a_elem["end"] < bfile_hash[chrom][0]["start"]):
                continue

            print "a_elem:",a_elem

            # a        =========
            # b =====
            i = 0
            while (i < len(bfile_hash[chrom]) and bfile_hash[chrom][i]["end"] < a_elem["start"]):
                i += 1

            # a =====
            # b    =====

            # a     =====
            # b  =====
        
            # a   ===
            # b =======

            # a  ============
            # b     ====

            # a ========
            # b ========

            if i == len(bfile_hash[chrom]):
                continue

            b_elem = bfile_hash[chrom][i]            
            
            if a_elem["start"] < b_elem["start"]:
                if a_elem["end"] > b_elem["end"]:
                    # a  ============
                    # b     ====
    
                    index_a = afile_hash[chrom].index(a_elem)
                    # not allowed to do this:
                    # python doesn't let you modify a list while iterating
#                    afile_hash[chrom].insert({"start": b_elem["end"] + 1, "end": a_elem["end"]})

                # a =====.....
                # b    =====
                a_elem["end"] = b_elem["end"] - 1;
'''                    
