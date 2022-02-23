import time
import traceback
import az_lib.az_lib as az_lib
#from util.az_logger import AzetiLogger
#logger = AzetiLogger() # In next version, this could be any logger
azLib=az_lib.AzLib() # The azimuth Execution Environment will inject the azLibEE here

def my_create_data():
    counter = 1
    filename="testfile.txt"
    my_test_file=open(filename,"w")
    while True:
 #       logger.info("Printing data with cycle "+str(counter)+" to file "+filename)
        print("Printing data with cycle "+str(counter)+" to file "+filename)
        print("My test value: "+str(counter),file=my_test_file)
        my_test_file.flush()
        azLib.publish_sensor_value("My test value",str(counter))
        counter+=1
        if counter==40:
            return
        time.sleep(5)

try:
    print("This is a test script. We will create a counter and increment it every 5 seconds.")
    print("You will see this message to the console only in your dev environment")
    my_create_data()
except Exception as exception:
    traceback.print_exc()
    #logger.logTraceStackToLogFile()

