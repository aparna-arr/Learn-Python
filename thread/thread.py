#!/usr/bin/python

import threading, sys

class myThread(threading.Thread):
    def __init__(self, idnum):
        threading.Thread.__init__(self)
        self.ID = idnum
        self.count = 0;
    def run(self):
        mutex.acquire()
        print "Start Thread:", self.ID

        while(self.count < 10):
            self.count += 1 
            print "Thread", self.ID, "count is",self.count
        mutex.release()

mutex = threading.Lock()

threadlist = []

thread1 = myThread(1); 
thread2 = myThread(2);

thread1.start()
thread2.start()

threadlist.append(thread1) 
threadlist.append(thread2)

for t in threadlist:
    t.join()

print "Done" 
