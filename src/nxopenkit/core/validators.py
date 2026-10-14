import math
from typing import Union
from .types import Double


def validate_angle(
    value: Double,
    field_name: str,
) -> Double:

    if isinstance(value, str):
        return

    if not 0 <= value <= 360:
        raise ValueError(
            f"{field_name} must be between 0 and 360."
        )
    return value

def validate_positive(
    value: float,
    field_name: str,
) -> float:

    if value <= 0:
        raise ValueError(
            f"{field_name} must be positive."
        )
    return value

def validate_double(
        value : Double,
        field_name : str
) -> Double:
    if isinstance(value, str):
        return

    if not math.isfinite(value):
        raise ValueError( f"{field_name} must be finite. Got {value}.")
    return value
def validate_positive_double(
    value: Double,
    field_name: str,
) -> Double:
    if isinstance(value, str):
        return

    if not math.isfinite(value):
        raise ValueError( f"{field_name} must be finite. Got {value}.")

    if value <= 0:
        raise ValueError(f"{field_name} must be positive. Got {value}.")
    return value
    

def validate_tolerance(
    tolerance: Union[float, None],
) ->  None:

    if tolerance is None:
        return None, None

    if not math.isfinite(tolerance):
        raise ValueError("tolerance must be finite.")

    if tolerance <= 0:
        raise ValueError("tolerance must be positive.")