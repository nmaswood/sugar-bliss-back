import pytest
import params as p
from pdb import set_trace

LD_INDEX = 2
USM_INDEX = 3


@pytest.mark.parametrize('function,f_input,ld,usm', [
    (p._mini_cupcakes, 0, None, None),
    (p._mini_cupcakes, 42, 25, 20),
    (p._mini_cupcakes, 1000, None, None),
    (p._regular_cupcakes, 46, 55, 80),
    (p._tiers, 5, 25, 25),
])
def test_foods(function, f_input, ld, usm):

    actual = function(f_input)

    ld_actual = actual[LD_INDEX]
    usm_actual = actual[USM_INDEX]

    assert ld_actual == ld
    assert usm_actual == usm


@pytest.fixture()
def sample():
    return {'miniCupcakes': 41,
            'regularCupcakes': 13,
            'cakePops': 45,
            'frenchMacarons': 1000,
            'tiers': 4,
            'other': 4,
            'numberOfBags': 0,
            'zipCode': '60601',
            'dateTime': '2018-04-14T20:56:34.698Z'}


@pytest.fixture()
def sample_expected_price():
    return {
        'custom': ['frenchMacarons'],
        'ld_absent': False,
        'ld_count': 5,
        'ld_sum': 90,
        'per_item': {'cakePops':
                     {'_input': 3, 'ld': 10, 'status': 'OKAY', 'usm': 15},
                     'frenchMacarons': {'_input': None,
                                        'ld': None,
                                        'status': 'CUSTOM',
                                        'usm': None},
                     'miniCupcakes': {'_input': 6,
                                      'ld': 25,
                                      'status': 'OKAY',
                                      'usm': 20},
                     'other': {'_input': 4, 'ld': 20, 'status': 'OKAY', 'usm': 20},
                     'regularCupcakes': {'_input': 4,
                                         'ld': 15,
                                         'status': 'USM_NULL',
                                         'usm': None},
                     'tiers': {'_input': 4, 'ld': 20, 'status': 'OKAY', 'usm': 20}},
        'usm_absent': False,
        'usm_count': 4,
        'usm_sum': 75,
        'warnings': []}


def test_price(sample, sample_expected_price):
    actual = p.price(sample)

    assert actual == sample_expected_price
