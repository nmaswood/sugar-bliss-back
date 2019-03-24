from dataclasses import dataclass
from datetime import date, time
from enum import Enum
from typing import Dict


class Carrier(Enum):
    ld = 'ld'
    usm = 'usm'


BAG = {
    'other',
    'tiers',
}


class Item:
    LD = 1
    USM = 2


@dataclass
class PriceResult:
    ld: float
    usm: float


@dataclass
class CalculationInput:
    date_: date
    time_start: time
    time_end: time
    zipcode: str
    mapping: Dict[str, int]


@dataclass
class PriceResultFinal:
    ld: float
    usm: float
    ld_dict: Dict[str, float]
    usm_dict: Dict[str, float]


@dataclass
class CarrierDict:
    carrier: Carrier
    price: float
    date_: date
    time_: time


class CalculationException(Exception):
    pass
