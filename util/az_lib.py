import os
import sys
from util.az_logger import AzetiLogger
logger = AzetiLogger()

AZ_LIB_VERSION=0.1
AZEE_VERSION=os.getenv("AZIMUTH_EXECUTION_ENVIRONMENT_VERSION")

if AZEE_VERSION:
    AZEE_VERSION=int(AZEE_VERSION)
    if AZ_LIB_VERSION<AZEE_VERSION:
        logger.error(f"Incompatible versions. azLib: {AZ_LIB_VERSION}. Azimuth Edge: {AZEE_VERSION}")
#        sys.exit(-1)
    else:
        MY_SCRIPT_NAME=os.getcwd()
        logger.info(f"Running under azimuth Execution Environment (azEE) v. {AZEE_VERSION}. My script name is {MY_SCRIPT_NAME}")
    import az_lib_ee
    azLibEE=az_lib_ee.AzLibEE()
else:
    logger.info("No azimuth Execution Environment (azEE) found")

import json

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
    if AZEE_VERSION:
        azLibEE.publish_sensor_value(sensor_id,sensor_value,MY_SCRIPT_NAME)
    else:
        logger.info(f">> PUBLISH {sensor_id}: {sensor_value}")
        #add print to csv file
