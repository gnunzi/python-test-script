import time
import traceback
import util.az_lib as az_lib
from util.az_logger import AzetiLogger
logger = AzetiLogger() # In next version, this could be any logger
azLib=az_lib.AzLib() # The azimuth Execution Environment will inject the azLibEE here

def say_hello():
    logger.info("Hello")
    teststr="Hello World"
    filename="testfile.txt"
    my_test_file=open(filename,"w")
    print(teststr,file=my_test_file)

try:
    print("This is a test script.")
except Exception as exception:
    traceback.print_exc()
    logger.logTraceStackToLogFile()
