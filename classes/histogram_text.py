from manimlib.imports import Text

TEXT_FONT_FAMILY = "Suisse Intl Regular"


class HistogramText(Text):
    """Overriden class of Text to assign a new font"""

    CONFIG = {
        "font": TEXT_FONT_FAMILY,
    }
