"""
Debug package.

A container for debug helpers.
"""


class DebugMain:
    """Contain all debug vars."""

    ENABLED = True
    # depending on how we want to log, this class can get complicated
    LOG_ENABLED = True

    def Log(self, stringToPrint):
        """Log the string if LOG_ENABLED is set to true."""
        if self.LOG_ENABLED:
            print(stringToPrint)

DEBUG = DebugMain()
