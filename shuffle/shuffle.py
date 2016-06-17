#!/usr/bin/python

import sys, threading
from subprocess import call
import subprocess

class myThread(threading.Thread):
    def __init__(self, IDnum, cmd, tmpcmd, files):
        threading.Thread.__init__(self)
        self.ID = str(IDnum)
        self.cmd1 = cmd
        self.tmpcmd = tmpcmd
        self.files = files
    
    def run(self):

        print "starting", self.ID
        nospace = self.tmpcmd + [self.ID]
 
        tmp_fh = open("".join(nospace), "a")
        call(self.cmd1, stdout=tmp_fh)
        tmp_fh.close()

        for index in range(0,int(len(self.files)/2),1):
            cmd2 = ["bedtools", "intersect", "-a", "".join(nospace), "-b", self.files[index]]
            pipe1 = subprocess.Popen(cmd2, stdout=subprocess.PIPE)
            cmd3 = ["awk", "{print $3 - $2}"] 
            pipe2 = subprocess.Popen(cmd3, stdin=pipe1.stdout, stdout=subprocess.PIPE)      
            cmd4 = ["awk", "{sum+=$1} END {print sum}"]

            out_fh = open(self.files[index + int(len(self.files)/2)], "a")
            pipe3 = subprocess.Popen(cmd4, stdin=pipe2.stdout, stdout=out_fh)
            out_fh.close()

#        call(["rm", "".join(nospace)])
        print "ending", self.ID
    

def usage():
    print "usage: python shuffle.py <gap file> <genome file> <tmp file dir> <number of shuffles> <file to be shuffled> <files to be intersected> <outfiles>"

def main():

    if (len(sys.argv) < 7):
        usage()
        sys.exit(2)

    gapfile = sys.argv[1]
    genomefile = sys.argv[2]
    tmpdir = sys.argv[3]
    numshuffles = sys.argv[4]
    shufflefile = sys.argv[5]
   
    print "Your gapfile is [",gapfile,"]"
    print "Your genomefile is [",genomefile,"]"
    print "Your tmpdir is [",tmpdir,"]"
    print "Your numshuffles is [",numshuffles,"]"

    if (not numshuffles.isdigit()):
        usage()
        print "Your numshuffles argument is not an integer!"
        sys.exit(2)

    numshuffles = int(numshuffles)
    print "Your shufflefile is [",shufflefile,"]"
    
 
    if ((len(sys.argv) - 6) % 2 != 0):
        usage()
        print "your arg number is",sys.argv,"! Num of files to be intersected and num outfiles MUST be the same."

        for i in (len(sys.argv) - 6):
            print "arg [",(i+6),"] is [",sys.argv(i+6),"]"

        sys.exit(2) 

    files = sys.argv[6:len(sys.argv)]

    mutex = threading.Lock()

    cmd = ["bedtools", "shuffle", "-chrom", "-excl", gapfile, "-i", shufflefile, "-g", genomefile] 
    tmp = [tmpdir, "/temp_"]

# def __init__(self, IDnum, cmd, tmpcmd, files):

    thread1 = myThread(0, cmd, tmp, files)

    thread1.start()

    threadlist = []
    threadlist.append(thread1)

    for t in threadlist:
        t.join()

    print "Done"

    return
'''
# testing
    i = str(0)
    nospace = [tmpdir, "/temp_", i, ";"]
    cmd = ["bedtools", "shuffle", "-chrom", "-excl", gapfile, "-i", shufflefile, "-g", genomefile] 

    print " ".join(cmd)

    tmp_fh = open("".join(nospace), "a")
    call(cmd, stdout=tmp_fh)
    close tmp_fh
'''

main();
