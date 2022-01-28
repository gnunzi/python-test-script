import time
import util.az_lib as az_lib
from util.az_logger import AzetiLogger
logger = AzetiLogger()

try:
    print("Hello world")
    teststr="test string"
    print(teststr)

    my_test_file=open("testfile.txt","w")
    print(teststr,file=my_test_file)

    counter = 1
    while True:
        logger.info("Printing data with cycle: "+str(counter))
        print(teststr+str(counter),file=my_test_file)
        my_test_file.flush()
        az_lib.publish("My test value",counter)
        counter+=1
        time.sleep(5)
except Exception as exception:
    logger.logTraceStackToLogFile()
