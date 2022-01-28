import json
import os

from requests.models import Response
from util.az_logger import AzetiLogger
import requests
from cachetools import cached, LFUCache
from util.az_exceptions import (AzetiCloudConnectionError, AzetiInfluxdbError, AzetiSensorNotFound,
                                AzetiSiteNotFound, AzetiCredentialsNotFound, AzetiAuthenticationError, AzetiMaxValueLengthError)
from datetime import datetime
from util import az_util
from util.az_values import SENSOR_GATEWAY, az_environment_variables

BASE_URL = 'https://cloud.azeti.net/acp-service'
# The credentials for api authentication need to be found in env variables
# names as below
CACHE_SIZE = 30
# The maximum length of the string values in InfluxDB 256 is a first guess. TODO: Check max value
MAX_LENGTH_VALUE_STRING = 256
logger = AzetiLogger()

class AzLib():
    """The main class for the wrapper."""

    def __init__(self,) -> None:
        # It will contain the auth token
        self.rest_headers: dict[str, str] = {}
        logger.info("Initializing az Lib EE")#add address of cloud
        self.mqttClient=mqttClient
        self.auth_to_azeti()

    def auth_to_azeti(self) -> str:
        """Perform the authentication to the azeti rest pi.
        The credentials are to be given as environment variables.

            Raises:
                AzetiCredentialsNotFound: Raised if the credentials are not found

            Returns:
                str: The auth token."""
        logger.debug("Authenticating with azeti api...")
        username = os.getenv(
            az_environment_variables.username_api_orchestrator)
        password = os.getenv(
            az_environment_variables.password_api_orchestrator)
        if username is None or password is None:
            raise AzetiCredentialsNotFound(username, password)
        try:
            query = {'username': username, 'password': password}
            headers: dict[str, str] = {}
            response = requests.post(
                BASE_URL+"/authentication/auth", headers=headers, json=query)
            if response.status_code != 200:
                logger.error("Error while authenticating. Code: " +
                             str(response.status_code))
                raise AzetiAuthenticationError(
                    f"Authentication error with username <{username}>. Error code: {response.status_code}")
        except requests.exceptions.RequestException as exception:
            logger.error(
                "Connection error to rest api. Error: "+str(exception))
            raise AzetiCloudConnectionError(response, exception) from exception
        logger.debug(
            f"Authenticated. We might need to authenticated again, since the token as limited lifetime.")
        self.auth_token = response.json()['token']
        self.rest_headers = {'X-Authorization': self.auth_token}
        return self.auth_token

    @cached(LFUCache(CACHE_SIZE))
    def get_site_guid(self, name_site: str = None, serial_sc: str = None) -> str:
        """Get the uid of a site from its name.
        This method is cached: if a uui has been already retrieved, this methods will not be 
        executed.

            Args:
                name_site (str): The name of the site.

            Raises:
                AzetiSiteNotFound: Raised if the site is not found.

            Returns:
                str: The name of the site."""
        if name_site is None and serial_sc is None:
            raise Exception("Both name site and serial are not given!")
        if not name_site is None and not serial_sc is None:
            raise Exception("Both name site and serial are given!")
        if serial_sc is None:
            logger.debug(f"Getting uuid of site <{name_site}>")
        else:
            logger.debug(
                f"Getting site uuid of serial controller with name <{serial_sc}>")
        response = requests.get(
            BASE_URL+"/sites", headers=self.rest_headers)
        # try again after authentication
        if self.is_unauthorized_response(response):
            response = requests.get(
                BASE_URL+"/sites", headers=self.rest_headers)
        # Check response
        if response.status_code != 200:
            raise AzetiSiteNotFound(name_site, response)
        for dict_element in response.json():
            if name_site is not None and dict_element['name'] == name_site:
                logger.debug("Found guid " + dict_element['guid'])
                return dict_element['guid']
            elif dict_element['serial'] == serial_sc:
                logger.debug("Found guid " + dict_element['guid'])
                return dict_element['guid']
        raise AzetiSiteNotFound(name_site, response)

    # TODO: Write general method with function get/put as argument
    def is_unauthorized_response(self, response: Response) -> bool:
        """Check if a request was unauthorized and in this case performs the authentication.

        If the request was unauthorized, then this method performs authentication and it returns True.
        The caller can check the return value and in case of True can perform the request again.

        :return: True is the response is unauthorized."""
        if response.status_code == 401:
            self.auth_to_azeti()
            return True
        return False

    @cached(LFUCache(CACHE_SIZE))
    def get_sensor_uid(self, sensor_name: str, site_name: str) -> str:
        """Gets the uuid of a sensor from its name.

        Args:
            site_name (str): The name of the site where the sensor is located.
            sensor_name (str): The name of the sensor

        Raises:
            Exception: [description]
            Exception: [description]
            Exception: [description]

        Returns:
            str: The uuid of the given sensor."""
        logger.info(f"Getting sensor <{sensor_name}> from site <{site_name}>")
        site_uuid = self.get_site_guid(site_name)
        data = {'siteUuid': site_uuid}
        response = requests.get(BASE_URL+"/sensors",
                                headers=self.rest_headers, params=data)
        if response.status_code != 200:
            raise Exception(f"Error while retrieve sensor <{sensor_name}> from site <{site_name}>." +
                            f"Error: {response.text}")
        for dict_element in response.json():
            if dict_element['id'] == sensor_name:
                return dict_element['guid']
        # Nothing found? Raise exception
        raise AzetiSensorNotFound(sensor_name, site_name)

    # returns [str,float,str]
    def get_sensor_value_last(self, site_guid: str, sensor_name: str):
        """Returns the last value of a sensor.

        The returned value can be None if no value is found.
        """
        logger.debug(f"Retrieving last value of <{sensor_name}>.")
        # sensor_uuid=self.get_sensor_uid(site_name,sensor_name)
        # site_uuid=self.get_site_uid(site_name)
        #query = f"SELECT LAST(value) as float_value, LAST(value_string) as string_value FROM Value WHERE sensor_id='{sensor_name}' AND location_guid='{site_guid}'"
        # Remember that SELECT LAST will not work
        query = f"SELECT value as float_value, value_string as string_value FROM Value WHERE sensor_id='{sensor_name}' AND location_guid='{site_guid}' ORDER BY time DESC LIMIT 1"
        logger.debug(f"Submitting query {query}")
        data = {'q': query}
        response = requests.get(BASE_URL+"/timeseries/query",
                                headers=self.rest_headers, params=data)
        logger.debug("Response from api: "+str(response.json()))
        # try again after authentication
        if self.is_unauthorized_response(response):
            response = requests.get(BASE_URL+"/timeseries/query",
                                    headers=self.rest_headers, params=data)
        if response.status_code != 200:
            self.check_response_for_db_errors(query, response)
        if response.json()['results'][0]['series'] is None:  # No value returned
            return [None, None, None]
        return response.json()['results'][0]['series'][0]['values'][0]

    def get_sensor_values(self, site_guid: str, sensor_name: str, from_time: datetime, from_included: bool = False):
        logger.debug(
            f"Retrieving values of <{sensor_name}> from time <{from_time}>.")
        # sensor_uuid=self.get_sensor_uid(site_name,sensor_name)
        # site_uuid=self.get_site_uid(site_name)
        operator = '>=' if from_included else '>'
        from_time_iso = az_util.convert_datetime_to_iso8601(from_time)
        query = f"SELECT \"value\",\"value_string\" FROM \"Value\" WHERE \"sensor_id\"='{sensor_name}' AND \"location_guid\"='{site_guid}' AND \"time\" {operator} '{from_time_iso}'"
        #query = f"SELECT \"value_string\" FROM \"Value\" WHERE sensor_id='{sensor_name}' LIMIT 10"
        logger.debug("Submitting query: "+query)
        data = {'q': query}
        response = requests.get(BASE_URL+"/timeseries/query",
                                headers=self.rest_headers, params=data)
        logger.debug("Response from api: "+str(response.json()))
        # try again if unauthorized
        if self.is_unauthorized_response(response):
            response = requests.get(BASE_URL+"/timeseries/query",
                                    headers=self.rest_headers, params=data)
        if response.status_code != 200:
            self.check_response_for_db_errors(query, response)
        if response.json()['results'] is None:
            return None
        if response.json()['results'][0]['series'] is None:
            return None  # TODO: implement type hint
        return response.json()['results'][0]['series'][0]['values']

    def check_response_for_db_errors(self, query: str, response: Response) -> None:
        if not response.json()['error'] is None:
            raise AzetiInfluxdbError(query, str(
                response.json()['group']), str(response.json()['infos']))

    def publish_sensor_value_raw(self, sensor_id, sensor_value):
        json_payload = {"error_code": 0, "result_dict": {sensor_id: {
            "changed": True, "value": sensor_value}}, "sensor_gateway_id": SENSOR_GATEWAY, "partial": True}
        self.mqttClient.publish("raw_result/"+SENSOR_GATEWAY,
                                json.dumps(json_payload))

    def publish_sensor_value(self, sensor_id, sensor_value):
        json_payload = {"error_code": 0, "sensor_id": sensor_id, "value": sensor_value}F
        self.mqttClient.publish("calibrated_result/"+sensor_id,
                                json.dumps(json_payload))
