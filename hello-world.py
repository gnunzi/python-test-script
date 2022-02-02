import time
import traceback
import util.az_lib as az_lib
from util.az_logger import AzetiLogger
logger = AzetiLogger() # In next version, this could be any logger
azLib=az_lib.AzLib() # The azimuth Execution Environment will inject the azLibEE here

try:
    print("This is a test script. We will create a counter and increment it every 5 seconds.")
    print("You will see this message to the console only in your dev environment")
    teststr="test string"
    filename="testfile.txt"
    my_test_file=open(filename,"w")
    print(teststr,file=my_test_file)
except Exception as exception:
    traceback.print_exc()
    logger.logTraceStackToLogFile()

def my_create_data():
    counter = 1
    while True:
        logger.info("Printing data with cycle "+str(counter)+" to file "+filename)
        print(teststr+str(counter),file=my_test_file)
        my_test_file.flush()
        azLib.publish_sensor_value("My test value",counter)
        counter+=1
        time.sleep(5)
