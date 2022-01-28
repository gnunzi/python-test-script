"""This module contains all the custom expections.
"""

import json
from requests.models import Response

class AzetiSiteNotFound(Exception):
    """Raised when a site is not found in the azeti cloud."""
    def __init__(self, site:str,response:Response=None) -> None:
        """Builds the exception.

        Args:
            site (str): The name of the site not found.
        """
        message=f"Site {site} not found."
        if response is not None:
            message+=" Response from server: "+json.dumps(response.json())
        super().__init__(message)

class AzetiSensorNotFound(Exception):
    """Raised when a sensor is not found in the azeti cloud."""
    def __init__(self, sensor:str,site:str) -> None:
        """Builds the exception.

        Args:
            sensor (str): The name of the sensor not found.
            site (str): The name of the site not found.
        """
        message=f"Sensor <{sensor}> non found on site <{site}>."
        super().__init__(message)

class AzetiScriptNotFound(Exception):
    """Raised when a script is not found in the directory."""
    def __init__(self, script:str,scripts_dir:str) -> None:
        """Builds the exception.

        Args:
            script (str): The name of the script not found.
            scripts_dir (str): The scripts directory currently used
        """
        message=f"Script <{script}> non found locally. Directory used :{scripts_dir}>."
        super().__init__(message)

class AzetiCredentialsNotFound(Exception):
    """Raised when the credentials for the azeti rest API are not found."""
    def __init__(self,username,password) -> None:
        password="No pwd found" if password is None else "Pwd found"
        message=f"The credentials for the azeti REST API are missing. Username: <{username}>. Password: <{password}>."
        super().__init__(message)

class AzetiInitializationError(Exception):
    """Raised when an error occurs in any  initialization step."""
    def __init__(self,*args: object) -> None:
        super().__init__(self,args)
        
class AzetiAuthenticationError(Exception):
    """Raised when the authentication to the rest api failed."""
    def __init__(self,*args: object) -> None:
        super().__init__(self,args)

class AzetiCloudConnectionError(Exception):
    """Raised when it was not possible to connect to the azeti cloud."""
    def __init__(self, response:Response,exception:Exception=None) -> None:
        """Builds the exception

        Args:
            code (int): The status code as returned by the http request. It can be none.
            exception (Exception): The original exception raised by the http call. It can be none.
        """
        message=""
        if response is not None:
            message="Status code of request: "+str(response.status_code)+"\n"
            message+=str(response.json())
            if exception is not None:
                message+=". Error received: "+str(exception)
        else:
            if exception is not None:
                message="Error received: "+str(exception)
        super().__init__(message)

class AzetiInfluxdbError(Exception):
    """An error reported by the InfluxDB while executing a request via rest api."""
    def __init__(self, query:str,group:str,infos:str) -> None:
        super().__init__("Error from db: "+group+": "+infos+". Submitted query: "+query)
        
class AzetiMaxValueLengthError(Exception):
    """This exception is raised if someone tried to pass a string value to the azeti rest api that is too long.
    
    The purpose of this exception is to avoid that we try to store strings too long in the InfluxDB."""
    def __init__(self,string_given:str,max_length_value_string:int) -> None:
        super().__init__(f"The provided string is too long. The max number of characters is {max_length_value_string}. String given <{string_given}>`")
        