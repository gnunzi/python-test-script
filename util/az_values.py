#OPERATION_SC = '~ Orchestrator: Operation'
#REPO_URLS = '~ Orchestrator: Repos urls'
from dataclasses import dataclass


SENSOR_GATEWAY="EdgeOrchestratorGateway"#Needed to generate raw results

@dataclass(frozen=True)
class SENSOR_NAMES:
    operation_sc: str = '~ EdgeOrchestrator: Operation'
    #repos_urls:str='~ Orchestrator: Repos urls'
    #time_last_pull: str = '~ Orchestrator: Time last pull'
    SCRIPTS = '~ EdgeOrchestrator: Scripts'


@dataclass(frozen=True)
class az_environment_variables:
    path_to_scripts: str = ''
    username_api_orchestrator = "USERNAME_API_ORCHESTRATOR"
    password_api_orchestrator = "PASSWORD_API_ORCHESTRATOR"
    logger_name = 'AZ_LOGGER_NAME'
    serial_sc = "AZ_SERIAL_SC"
    enable_verbosity = "AZ_VERBOSE_DEBUG"


@dataclass(frozen=True)
class az_commands:
    MQTT_COMMAND_TOPIC: str = 'calibrated_result/~ EdgeOrchestrator: Command'
    COMMAND_PULL_OPERATION: str = 'pull operation'
    COMMAND_DELETE_ALL_SCRIPTS: str = 'delete scripts'


@dataclass(frozen=True)
class az_ipc_operations:
    pull_operation: str = 'pull operation'
    pull_script: str = 'pull script'


@dataclass(frozen=True)
class OPERATIONS:
    SCRIPTS_INIT = 'scripts init'
    delete_scripts = 'delete all scripts'


@dataclass(frozen=True)
class az_exit_codes_orchestrator:
    shutdown: int = 0
    credentials_rest_api_not_found: int = 1
    serial_sc_missing: int = 2
    pipe_not_found: int = 3
    no_mqtt_connection: int = 4
