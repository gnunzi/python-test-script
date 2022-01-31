import time
import traceback
import util.az_lib as az_lib
from util.az_logger import AzetiLogger
logger = AzetiLogger()

try:
    print("Hello world")
    teststr="test string"
    print(teststr)
    filename="testfile.txt"
    my_test_file=open(filename,"w")
    print(teststr,file=my_test_file)

    counter = 1
    while True:
        logger.info("Printing data with cycle "+str(counter)+" to file "+filename)
        print(teststr+str(counter),file=my_test_file)
        my_test_file.flush()
        az_lib.publish("My test value",counter)
        counter+=1
        time.sleep(5)
except Exception as exception:
    traceback.print_exc()
    logger.logTraceStackToLogFile()
