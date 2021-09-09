from manimlib.imports import Text


class HistogramText(Text):
    """Перегрузка класса Text для применения шрифта"""

    CONFIG = {"font": "Suisse Intl Regular"}
# зачем
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
