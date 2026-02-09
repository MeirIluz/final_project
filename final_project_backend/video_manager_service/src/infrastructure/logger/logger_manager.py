import datetime
import logging
import os
from typing import Dict
from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.interfaces.managers.ilogger_manager import ILoggerManager
from src.globals.consts.const_collections import ConstCollections

class LoggerManager(ILoggerManager):
    def __init__(self):
        self._loggers: Dict[str, logging.Logger] = {}
        self._set_logging_level_names()

    def log(self, log_name: str, msg: str, level=logging.DEBUG):
        logger = self._get_or_create_logger(log_name, level)
        logger.log(level, msg)

    def _get_or_create_logger(self, log_name: str, level) -> logging.Logger:
        if log_name in self._loggers:
            return self._loggers[log_name]

        logs_folder = os.getenv(ConstsStrings.LOG_ENV)
        os.makedirs(logs_folder, exist_ok=True)

        # Find newest file in folder
        log_files = [
            file_path
            for file_path in [
            os.path.join(logs_folder, file_name)
            for file_name in os.listdir(logs_folder)
        ]
            if os.path.isfile(file_path)
        ]
        if log_files:
            log_file_path = max(log_files, key=os.path.getmtime)
        else:
            # If folder empty → create a new file
            log_file_path = os.path.join(
                logs_folder,
                f"{log_name}_{datetime.datetime.now().strftime(ConstsStrings.DATE_TIME_FORMAT)}.log"
            )

        logger = logging.getLogger(log_name)
        logger.setLevel(level)

        if not logger.handlers:
            if (log_name in ConstCollections.LOG_NAMES_WITH_FILE):
                self._add_file_handler(level, log_file_path, logger)
            if (log_name in ConstCollections.LOG_NAMES_WITH_CONSOLE):
                self._add_console_handler(level, logger)
        self._loggers[log_name] = logger
        return logger

    def _add_file_handler(self, level, log_file_path, logger):
        file_handler = logging.FileHandler(
            log_file_path, mode=ConstsStrings.LOG_MODE)
        file_handler.setLevel(level)
        formatter = logging.Formatter(ConstsStrings.LOG_FORMATTER)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def _add_console_handler(self, level, logger):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter(ConstsStrings.LOG_FORMATTER)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    def _set_logging_level_names(self) -> None:
        logging.addLevelName(logging.CRITICAL, ConstsStrings.ALGORITHM_MANAGER_CRITICAL_LOG_LEVEL_NAME)
        logging.addLevelName(logging.ERROR,    ConstsStrings.ALGORITHM_MANAGER_ERROR_LOG_LEVEL_NAME)
        logging.addLevelName(logging.WARNING,  ConstsStrings.ALGORITHM_MANAGER_WARNING_LOG_LEVEL_NAME)
        logging.addLevelName(logging.INFO,     ConstsStrings.ALGORITHM_MANAGER_INFO_LOG_LEVEL_NAME)
        logging.addLevelName(logging.DEBUG,    ConstsStrings.ALGORITHM_MANAGER_DEBUG_LOG_LEVEL_NAME)
