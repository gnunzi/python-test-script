import time
import os
import sys

my_test_file=open("alextestfile.txt","w")

counter = 1
while True:
    print("My script writes: "+str(counter),file=my_test_file)
    my_test_file.flush()
    time.sleep(5)
    counter+=1