import logging
import logging.handlers
import os
import sys
import traceback

ENV_LOGGER_FILENAME='AZ_LOGGER_NAME'
#LOGGER_FILENAME=os.getenv(ENV_LOGGER_FILENAME,os.path.join(os.getcwd(),'az_lib.log'))
LOGGER_FILENAME=os.path.join(os.getcwd(),'az_lib.log')

class ConsoleFormatter(logging.Formatter):
    """The formatter used for the console output. It introduces colors based on the log level
    and then prints nicely."""
    def __init__(self, default=None):
        self._default_formatter = default
        super().__init__()

    def format(self, record):
        color_suffix="\033[0m"
        match record.levelno:
            case logging.DEBUG:
                color_prefix="\033[90m" # grey
            case logging.WARNING:
                color_prefix="\033[33m" # yellow
            case logging.ERROR:
                color_prefix="\033[31m" # red
            case logging.CRITICAL:
                color_prefix="\033[31m" # red
            case _:
                color_prefix="\033[37m" # white
        #return self._default_formatter.format(record)
        filename_without_extension=record.filename[0:-3][:10] #make sure that 10 is also the number in {filename_without_extension:10s}a
        if hasattr(record,'script_name'):
            optional_script_name=record.script_name[:30] #make sure that 30 is also the same number in {optional_script_name:30s} below 
        else: optional_script_name=""
        funcName=record.funcName.replace("__","").replace("_"," ").replace("-"," ").strip() # user friendly output with spaces
        funcName=funcName[:16] #make sure that 12 is also the same number in {funcName:<12s}
        msg=record.message #.replace("_"," ").strip()
        string_to_return=f"{color_prefix}{filename_without_extension:10s}{optional_script_name:30s}{funcName:<16s}|"+\
            f"{msg}{color_suffix}"
        string_to_return.replace("__","").replace("_"," ").strip()
        return string_to_return

class AzetiLogger(logging.Logger):
    """Our Logger. It has two handlers: file handler and shell handler for console output."""
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
            cls.__instance.__initialized = False
        return cls.__instance
        
    def __init__(self) -> None:
        if(self.__initialized): return # singletone
        self.__initialized = True# singletone
        super().__init__("AZ_LOGGER",logging.DEBUG)
        # Handler for the log file, useful for debugging
        FORMAT = "%(asctime)s | %(filename)-15s:%(lineno)-4s - %(funcName)-10s > %(message)s"
        self.fileHandler=logging.handlers.RotatingFileHandler(LOGGER_FILENAME)
        self.fileHandler.setFormatter(logging.Formatter(FORMAT))
        self.fileHandler.setLevel(logging.DEBUG)
        self.addHandler(self.fileHandler)
        # Handler for the console output, i.e. for the end user.
        self.shellHandler=logging.StreamHandler(sys.stderr)
        self.addHandler(self.shellHandler)
        self.info(f"=== az logger started. Log file: {LOGGER_FILENAME} ===")
        self.shellHandler.setFormatter(ConsoleFormatter())
        self.shellHandler.setLevel(logging.DEBUG)
        self.debug(f"You can change the log filename with env variable <{ENV_LOGGER_FILENAME}>.")

    def setLevelShellOutput(self,level:int):
        self.shellHandler.setLevel(level)
        
        
    def print_sensor(self,sensor:str)->None:
        self.info(f"FIX ME print sensor")

    def logTraceStackToLogFile(self):
        self.error(traceback.format_exc())
    
def printException(exception:Exception,showStack:bool=False):
    traceback.print_exc()