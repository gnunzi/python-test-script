"""This module defines the loggers of the Orchestrator package."""
import logging
import logging.handlers
import os
import sys
import traceback
from logging import StreamHandler


class ConsoleFormatter(logging.Formatter):
    """The formatter used for the console output. It introduces colors based on the log level
    and then prints nicely."""

    def __init__(self, scriptName=""):
        self._default_formatter = None  # cant remember what is this for
        super().__init__()
        self.scriptName = scriptName

    def format(self, record):
        color_suffix = "\033[0m"
        match record.levelno:
            case logging.DEBUG:
                color_prefix = "\033[90m"  # grey
            case logging.WARNING:
                color_prefix = "\033[33m"  # yellow
            case logging.ERROR:
                color_prefix = "\033[31m"  # red
            case logging.CRITICAL:
                color_prefix = "\033[31m"  # red
            case _:
                color_prefix = "\033[37m"  # white
        # make sure that 15 is also the number in {filename_without_extension:10s}a
        filename_without_extension = record.filename[0:-3][:15]
        funcName = record.funcName.replace("__", "").replace("_", " ").replace(
            "-", " ").strip()  # user friendly output with spaces
        # make sure that 12 is also the same number in {funcName:<1s}
        funcName = funcName[:20]
        msg = record.message  # .replace("_"," ").strip()
        string_to_return = f"{color_prefix}{filename_without_extension:10s}{self.scriptName:30s}{funcName:<20s}|" +\
            f"{msg}{color_suffix}"
        string_to_return.replace("__", "").replace("_", " ").strip()
        return string_to_return


class AzetiLogger(logging.Logger):
    """Our Logger. It has two handlers: file handler and shell handler for console output."""
    __instance = None

    def __new__(cls, scriptName=None, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, scriptName=None) -> None:
        if(self.__initialized):
            return  # singletone
        self.__initialized = True  # singletone
        super().__init__("AZ_LOGGER", logging.DEBUG)
        # self.scriptName=scriptName#if none, the logger is for the orchestrator
        if not scriptName:  # scriptName is given when the logger is created by Script.py in the Orchestrator
            # Here the scriptName is taken from the script being executed
            scriptName = os.getenv("AZ_SCRIPT_NAME", "")
        # Handler for the log file, useful for debugging
        FORMAT = "%(asctime)s | %(filename)-15s:%(lineno)-4s - %(funcName)-15s > %(message)s"
        if scriptName:
            self.fileHandler = logging.handlers.RotatingFileHandler(
                "az_lib.log")
        self.fileHandler.setFormatter(logging.Formatter(FORMAT))
        self.fileHandler.setLevel(logging.DEBUG)
        self.addHandler(self.fileHandler)
        # Handler for the console output, i.e. for the end user.
        self.shellHandler = logging.StreamHandler(sys.stderr)
        #FORMAT = "%(filename)-15s - %(funcName)-10s > %(message)s"
        # sh.setFormatter(logging.Formatter(FORMAT))
        self.addHandler(self.shellHandler)
        self.shellHandler.setFormatter(ConsoleFormatter(scriptName))
        self.shellHandler.setLevel(logging.DEBUG)

    def setLevelShellOutput(self, level: int):
        self.shellHandler.setLevel(level)

    def print_sensor(self, sensor: str) -> None:
        self.info(f"FIX ME print sensor")

    def logTraceStackToLogFile(self):
        self.error(traceback.format_exc())


def printException(exception: Exception, showStack: bool = False):
    traceback.print_exc()
