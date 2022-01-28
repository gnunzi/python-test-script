from datetime import datetime,timezone
from dateutil import parser

def convert_datetime_to_iso8601(utc_time:datetime) -> str:
    """Converts a datetime to a string conformant to ISO8601 - useful for InfluxDB.
    
    InfluxDB requires time to be properly formatted. This function creates the time
    string so that it can be used for InfluxDB.
    The given time must be UTC."""
    return utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+"Z"

def  now_in_iso8601() -> str:
    """Returns the current time (datetime.now()) formatted as ISO8601 - useful for InfluxDB.
    """
    return convert_datetime_to_iso8601(datetime.now(timezone.utc))

def convert_iso8601_to_datetime_local_time_zone(iso_date:str)->datetime:
    iso_date_without_Z=iso_date[:-1]
    #return datetime.strptime(iso_date_without_Z,'%Y-%m-%dT%H:%M:%S.%f')
    return parser.parse(iso_date)