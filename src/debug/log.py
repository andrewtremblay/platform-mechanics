"""
Debug package.

A container for debug helpers.
"""
import configs as conf


def Debug(stringToPrint):
    """Log the string if DEBUG_LOG_ENABLED in config is set to true."""
    if conf.DEBUG.LOG_ENABLED:
        print(stringToPrint)
