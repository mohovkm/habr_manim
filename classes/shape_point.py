from typing import Tuple, Union

from numpy import array, ndarray


class ShapePointException(Exception):
    pass


class ShapePointTypeError(ShapePointException):
    pass


class ShapePointTooManyValuesException(ShapePointException):
    pass


class ShapePoint:
    """Class for validation and storing information about screen points"""

    _coords: ndarray

    def __init__(self, coords: Tuple[Union[int, float], Union[int, float]]):
        self.coords = coords

    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, value: Tuple[Union[int, float], Union[int, float]]):
        """Method -setter for validation and storing coordinates.

        Args:
            value (Tuple[Union[int, float], Union[int, float]]): tuple with coordinates

        Raises:
            ShapePointTypeError: Wrong data type was passed.
            ShapePointTooManyValuesException: You put too many variables inside tuple.
            ShapePointTypeError: Data inside tuple is in the wrong format.
        """
        if not isinstance(value, Tuple) and not isinstance(value, ndarray):
            detail = f"Coords must be a type of: [tuple, np.ndarray], got [{type(value)}] instead."
            raise ShapePointTypeError(detail)

        if isinstance(value, ndarray):
            value = value[:2]

        if len(value) != 2:
            detail = "Coords must contain 2 values"
            raise ShapePointTooManyValuesException(detail)

        for coord in value:
            if not isinstance(coord, int) and not isinstance(coord, float):
                detail = f"Values in coords must be a type of: [int, float], got [{coord}:{type(coord)}] instead."
                raise ShapePointTypeError(detail)

        self._coords = array([value[0], value[1], 0])

    def __getitem__(self, item):
        return self.coords[item]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.coords})"
