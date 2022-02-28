from az_lib.az_logger import AzetiLogger

# The maximum length of the string values in InfluxDB 256 is a first guess. TODO: Check max value
MAX_LENGTH_VALUE_STRING = 256


class AzLib():

    def __init__(self, scriptName=None) -> None:
        self.logger = AzetiLogger(scriptName)

    # returns [str,float,str]
    def get_sensor_value_last(site_guid: str, sensor_name: str):
        """Returns the last value of a sensor.

        The returned value can be None if no value is found.
        """
        # logger.debug(f"Retrieving last value of <{sensor_name}>.")

    def get_sensor_values(site_guid: str, sensor_name: str, from_time: datetime, from_included: bool = False):
        # logger.debug(
        # f"Retrieving values of <{sensor_name}> from time <{from_time}>.")

    def publish_sensor_value_raw(sensor_id, sensor_value):
        pass

    def publish_sensor_value(self, sensor_id, sensor_value):
        str = f">> PUBLISH {sensor_id}: {sensor_value}"
        if self.logger:
            self.logger.info(str)
        else:
            print(str)
