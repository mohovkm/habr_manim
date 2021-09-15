from typing import Tuple, Union

from numpy import array, ndarray


class ShapePointException(Exception):
    pass


class ShapePointTypeError(ShapePointException):
    pass


class ShapePointTooManyValuesException(ShapePointException):
    pass


class ShapePoint:
    """Класс с информацией о координатах точки на экране"""

    _coords: array

    def __init__(self, coords: Tuple[Union[int, float], Union[int, float]]):
        self.coords = coords

    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, value: Tuple[Union[int, float], Union[int, float]]):
        """Метод - сеттер для валидации и хранения полученных координат.

        Args:
            value (Tuple[Union[int, float], Union[int, float]]): Кортеж из координат.

        Raises:
            ShapePointTypeError: Передан неверный тип данных.
            ShapePointTooManyValuesException: Передано слишком много парамеров в кортеже
            ShapePointTypeError: Передан неверный тип данных внутри кортежа.
        """
        if not isinstance(value, Tuple) and not isinstance(value, ndarray):
            detail = f"coords must be a type of: [tuple, np.ndarray], got [{type(value)}] instead."
            raise ShapePointTypeError(detail)

        if isinstance(value, ndarray):
            value = value[:2]

        if len(value) != 2:
            detail = "coords must contain 2 values"
            raise ShapePointTooManyValuesException(detail)

        for coord in value:
            if not isinstance(coord, int) and not isinstance(coord, float):
                detail = f"values in coords must be a type of: [int, float], got [{coord}:{type(coord)}] instead."
                raise ShapePointTypeError(detail)

        self._coords = array([value[0], value[1], 0])

    def __getitem__(self, item):
        return self.coords[item]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.coords})"
