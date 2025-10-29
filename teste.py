from threading import *
from time import sleep
class One (Thread):
    def run (self) :
        for i in range (20) :
            print ("Class one")
            sleep(1)




class Two (Thread):
    def run (self):
        for i in range (10):
            print ("Class two")
            sleep(1)

one = One()
two = Two()

one.start()
two.start()
