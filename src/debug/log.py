"""
Debug package.

A container for debug helpers.
"""
import config as conf


def Debug(stringToPrint):
    """Log the string if DEBUG_LOG_ENABLED in config is set to true."""
    if conf.DEBUG_LOG_ENABLED:
        print(stringToPrint)
