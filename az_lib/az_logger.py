import logging
import logging.handlers
import sys
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
        filename_without_extension = record.filename[0:-3][:10]
        funcName = record.funcName.replace("__", "").replace("_", " ").replace(
            "-", " ").strip()
        funcName = funcName[:16]
        msg = record.message
        string_to_return = f"{color_prefix}{filename_without_extension:10s}{self.scriptName:30s}{funcName:<16s}|" +\
            f"{msg}{color_suffix}"
        string_to_return.replace("__", "").replace("_", " ").strip()
        return string_to_return


class AzetiLogger(logging.Logger):
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
        super().__init__("AZ_LOGGER", logging.INFO)
        self.shellHandler = logging.StreamHandler(sys.stderr)
        self.addHandler(self.shellHandler)
        self.info(f"=== az logger started. ===")
        self.shellHandler.setFormatter(ConsoleFormatter(scriptName))
        self.shellHandler.setLevel(logging.DEBUG)
