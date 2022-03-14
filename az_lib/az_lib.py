from az_lib.az_logger import AzetiLogger

# The maximum length of the string values in InfluxDB 256 is a first guess. TODO: Check max value
MAX_LENGTH_VALUE_STRING = 256


class AzLib():

    def __init__(self, scriptName=None) -> None:
        self.logger = AzetiLogger(scriptName)

    def publish_sensor_value1(self, register_number, sensor_value):
        str = f">> PUBLISH PRE-DEFINED SENSOR#{register_number}: {sensor_value}"
        if self.logger:
            self.logger.info(str)
        else:
            print(str)

    def publish_sensor_value2(self, sensor_id, sensor_value):
        str = f">> PUBLISH SENSOR {sensor_id}: {sensor_value}"
        if self.logger:
            self.logger.info(str)
        else:
            print(str)
