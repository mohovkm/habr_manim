from manimlib.imports import Text

TEXT_FONT_FAMILY = "Suisse Intl Regular"


class HistogramText(Text):
    """Перегрузка класса Text для применения шрифта"""

    CONFIG = {
        "font": TEXT_FONT_FAMILY,
    }
