from src.infrastructure.interfaces.managers.ilogger_manager import ILoggerManager
from src.infrastructure.logger.logger_manager import LoggerManager


class LoggerFactory:
    logger_manager: ILoggerManager = None

    @staticmethod
    def get_logger_manager() -> ILoggerManager:
        if LoggerFactory.logger_manager is None:
            LoggerFactory.logger_manager = LoggerManager()
        return LoggerFactory.logger_manager
