import time
import traceback
import az_lib.az_lib as az_lib
azLib = az_lib.AzLib('create-data')


def my_create_data():
    counter = 1
    filename = "testfile.txt"
    my_test_file = open(filename, "w")
    azLib.logger.info('Starting main loop...')
    while True:
     #       logger.info("Printing data with cycle "+str(counter)+" to file "+filename)
        #print("Printing data with cycle "+str(counter)+" to file "+filename)
        azLib.logger.info("Publishing test value: " +
                          str(counter))
        my_test_file.flush()
        azLib.publish_sensor_value1("My test value", str(counter))
        azLib.publish_sensor_value2(1, str(counter))
        counter += 1
        if counter > 20:
            return
        time.sleep(5)


try:
    print("This is a test script. We will create a counter and increment it every 5 seconds.")
    print("You will see this message to the console only in your dev environment")
    azLib.logger.info('Starting script - new version...')
    my_create_data()
except Exception as exception:
    traceback.print_exc()
    azLib.logger.error('Got error'+str(exception))
    # logger.logTraceStackToLogFile()
