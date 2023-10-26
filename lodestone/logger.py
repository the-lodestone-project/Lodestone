from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Back, Style
import structlog
import platform
import logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="%H:%M:%S"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer(),
    ]
)

logger = structlog.getLogger(__name__)
