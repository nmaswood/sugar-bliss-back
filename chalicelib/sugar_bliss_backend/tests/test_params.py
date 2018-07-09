import pytest
import chalicelib.sugar_bliss_backend.params as p
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
            # 'numberOfBags': 0,
            'zipCode': '60601',
            'dateTime': '2018-04-14T20:56:34.698Z'}
