import os
import sys
import logging
from datetime import datetime

from app.core.contextvar import tenant_context
from dotenv import load_dotenv

load_dotenv()

class DynamicExtraFormatter(logging.Formatter):
    """
    Custom formatter to dynamically include extra keys inside the square brackets,
    excluding specific keys like 'taskName'.
    """
    EXCLUDED_KEYS = ['taskName']  # Add any other keys you want to exclude here

    def format(self, record):
        # Base fields in the square brackets
        base_fields = [
            f"Tenant: {getattr(record, 'tenant_id', '')}",
            f"Email: {getattr(record, 'email_id', '')}",
            f"event_type: {getattr(record, 'event_type', '')}"
        ]

        # Add any additional fields from extras dynamically, excluding the ones in EXCLUDED_KEYS
        for key, value in record.__dict__.items():
            if key not in ('tenant_id', 'email_id', 'event_type', 'asctime', 'levelname', 'message', 'msg', 'args',
                           'created', 'exc_info', 'exc_text', 'filename', 'funcName', 'levelno', 'lineno', 'module',
                           'msecs', 'msecs', 'msecs', 'name', 'pathname', 'process', 'processName', 'relativeCreated',
                           'stack_info', 'thread', 'threadName', 'extra') and key not in self.EXCLUDED_KEYS:
                base_fields.append(f"{key}: {value}")

        # Join all fields for the square bracket section
        square_bracket_section = ", ".join(base_fields)

        # Format the log message
        log_message = f"{self.formatTime(record)} - {record.levelname} - [{square_bracket_section}] - {record.getMessage()}"
        return log_message

multi_tenant_logger = None

def get_logger_instance():
    """
    Get or create the multi-tenant logger instance.

    Returns:
        logging.Logger: The multi-tenant logger instance.
    """
    global multi_tenant_logger
    if multi_tenant_logger is None:
        multi_tenant_logger = logging.getLogger('multi_tenant_logger')
        
        # Read the logging level from the environment variable
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Map the log level to the logging module's level
        if log_level == 'DEBUG':
            multi_tenant_logger.setLevel(logging.DEBUG)
        elif log_level == 'INFO':
            multi_tenant_logger.setLevel(logging.INFO)
        elif log_level == 'ERROR':
            multi_tenant_logger.setLevel(logging.ERROR)
        else:
            # Default to DEBUG if the log level is not recognized
            multi_tenant_logger.setLevel(logging.DEBUG)
        
        # Check if the logger already has handlers
        if not multi_tenant_logger.handlers:
            ch = logging.StreamHandler(sys.stdout)
            # formatter = logging.Formatter('%(asctime)s - %(levelname)s - [Tenant: %(tenant_id)s, Email: %(email_id)s, event_type: %(event_type)s] - %(message)s')
            formatter = DynamicExtraFormatter()
            ch.setLevel(multi_tenant_logger.level)
            ch.setFormatter(formatter)
            multi_tenant_logger.addHandler(ch)

    return multi_tenant_logger

class CustomLogger:
    """
    Custom logger class for multi-tenant logging.
    """

    @classmethod
    def info(cls, message, event_type=None, extras=None):
        """
        Log an info level message.

        Args:
            message (str): The log message.
            event_type (str, optional): The event type. Defaults to None.
            extras (dict, optional): Additional fields to include in the log. Defaults to None.
        """
        cls._log_with_extra(logging.INFO, message, event_type, extras)

    @classmethod
    def debug(cls, message, event_type=None, extras=None):
        """
        Log a debug level message.

        Args:
            message (str): The log message.
            event_type (str, optional): The event type. Defaults to None.
            extras (dict, optional): Additional fields to include in the log. Defaults to None.
        """
        cls._log_with_extra(logging.DEBUG, message, event_type, extras)

    @classmethod
    def warning(cls, message, event_type=None, extras=None):
        """
        Log a warning level message.

        Args:
            message (str): The log message.
            event_type (str, optional): The event type. Defaults to None.
            extras (dict, optional): Additional fields to include in the log. Defaults to None.
        """
        cls._log_with_extra(logging.WARNING, message, event_type, extras)

    @classmethod
    def error(cls, message, event_type=None, extras=None):
        """
        Log an error level message.

        Args:
            message (str): The log message.
            event_type (str, optional): The event type. Defaults to None.
            extras (dict, optional): Additional fields to include in the log. Defaults to None.
        """
        cls._log_with_extra(logging.ERROR, message, event_type, extras)

    @classmethod
    def _log_with_extra(cls, level, message, event_type=None, extras=None):
        """
        Internal helper method to log messages with standard and custom extra fields.

        Args:
            level (int): The logging level.
            message (str): The log message.
            event_type (str, optional): The event type. Defaults to None.
            extras (dict, optional): Additional fields to include in the log. Defaults to None.
        """
        if extras is None:
            extras = {}
        tenant_data = tenant_context.get()
        
        # Merge tenant data and additional extras
        log_extras = {
            **tenant_data
        }
        if event_type:
            log_extras['event_type'] = event_type
        log_extras.update(extras)  # Merge extras into log_extras
        
        logger = get_logger_instance()
        logger.log(level, message, extra=log_extras)