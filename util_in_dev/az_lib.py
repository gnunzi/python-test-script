import os
import sys
from util_in_dev.az_logger import AzetiLogger
logger = AzetiLogger()

# try:
#     import util.az_lib_ee as az_lib_ee
#     try:
#         azLibEE=az_lib_ee.AzLibEE()
#         MY_SCRIPT_NAME=os.getcwd()
#         #todo: check versions
#         logger.info(f"Running under azimuth Execution Environment (azEE) v. {AZEE_VERSION}. My script name is {MY_SCRIPT_NAME}")
#     except Exception as exception:
#         logger.error("Generic error: "+str(exception))
#         sys.exit(-1)
# except Exception as exception:
#     logger.info("No azimuth Execution Environment (azEE) found. Original error: "+str(exception))

from datetime import datetime

# The maximum length of the string values in InfluxDB 256 is a first guess. TODO: Check max value
MAX_LENGTH_VALUE_STRING = 256

# returns [str,float,str]
def get_sensor_value_last(site_guid: str, sensor_name: str):
    """Returns the last value of a sensor.

    The returned value can be None if no value is found.
    """
    logger.debug(f"Retrieving last value of <{sensor_name}>.")

def get_sensor_values(site_guid: str, sensor_name: str, from_time: datetime, from_included: bool = False):
    logger.debug(
        f"Retrieving values of <{sensor_name}> from time <{from_time}>.")

def publish_sensor_value_raw(sensor_id, sensor_value):
    pass

def publish(sensor_id, sensor_value):
    if azLibEE:
        azLibEE.publish_sensor_value(sensor_id,sensor_value,MY_SCRIPT_NAME)
    else:
        logger.info(f">> PUBLISH {sensor_id}: {sensor_value}")
        #add print to csv file
