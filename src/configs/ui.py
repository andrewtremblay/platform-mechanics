"""UI constants and variables."""

from base.color import Color


class UiConfig:
    """
    The base class for UI variables.

    UI contains variables for:
     * screen dimensions
     * volume levels
     * color assignments

    UI does NOT contain variables for:
     * button mapping
     * color assignments
    """

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    BANNER_TEXT_COLOR = Color.White


UI = UiConfig()
