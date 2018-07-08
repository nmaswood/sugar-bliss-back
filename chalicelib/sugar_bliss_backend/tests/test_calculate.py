from pdb import set_trace
import chalicelib.sugar_bliss_backend.calculate as cal
from dateutil.parser import parse


def generate_results():

    sample = {
        'miniCupcakes': '10',
        'regularCupcakes': '20',
        'cakePops': '30',
        'frenchMacarons': '40',
        'tiers': '50',
        'other': '60',
        'zipCode': '60601',
        'dateTime': '2018-07-21',
        'time': '10am-12pm'
    }

    return sample


def test_validate():
    init_obj = generate_results()
    no_errors = cal.validate(init_obj)

    assert len(no_errors) == 0

    time_off = dict(init_obj)
    time_off['time'] = '9pm-10pm'

    time_errors = cal.validate(time_off)

    assert 'Time 9pm-10pm not in valid range of times' in time_errors

    zip_off = dict(init_obj)
    zip_off['zipCode'] = '12345'
    zip_errors = cal.validate(zip_off)

    assert "12345 is not supported zipcode. Zipcode must start with '06'" in zip_errors

    negative_off = dict(init_obj)
    negative_off['other'] = '-1'
    negative_errors = cal.validate(negative_off)

    assert 'other cannot have negative value.' in negative_errors

    sunday_off = dict(init_obj)
    sunday_off['dateTime'] = '2018-07-08'
    sunday_errors = cal.validate(sunday_off)

    assert 'Cannot specify a Sunday' in sunday_errors


def test_preprocess():
    init_obj = generate_results()

    expected = {
        'miniCupcakes': 10,
        'regularCupcakes': 20,
        'cakePops': 30,
        'frenchMacarons': 40,
        'tiers': 50,
        'other': 60,
        'zipCode': '60601',
        'date': parse('2018-07-21').date(),
        'time_start': parse('10am').time(),
        'time_end': parse('12pm').time(),
    }

    actual = cal.preprocess(init_obj)
    assert expected == actual


def test_calculate():
    i_one = {
        'miniCupcakes': '25',
        'regularCupcakes': 0,
        'cakePops': 0,
        'frenchMacarons': 0,
        'tiers': 0,
        'other': 0,
        'zipCode': '60601',
        'dateTime': '2018-05-16',
        'time': '10am-12pm'
    }

    expected = {'base_price_dict': {'LS': '19', 'USM': '24'},
                'food_item_dict': {'custom': [],
                                   'ld_absent': False,
                                   'ld_count': 1,
                                   'ld_sum': 15,
                                   'per_item': {'cakePops': {'_input': 0,
                                                             'ld': None,
                                                             'status': 'NIL',
                                                             'usm': None},
                                                'frenchMacarons': {'_input': 0,
                                                                   'ld': None,
                                                                   'status': 'NIL',
                                                                   'usm': None},
                                                'miniCupcakes': {'_input': 4,
                                                                 'ld': 15,
                                                                 'status': 'USM_NULL',
                                                                 'usm': None},
                                                'other': {'_input': 0,
                                                          'ld': None,
                                                          'status': 'NIL',
                                                          'usm': None},
                                                'regularCupcakes': {'_input': 0,
                                                                    'ld': None,
                                                                    'status': 'NIL',
                                                                    'usm': None},
                                                'tiers': {'_input': 0,
                                                          'ld': None,
                                                          'status': 'NIL',
                                                          'usm': None}},
                                   'usm_absent': False,
                                   'usm_count': 0,
                                   'usm_sum': 0,
                                   'warnings': []},
                'ld_final': 34.0,
                'price': 24.0,
                'usm_final': 24.0,
                'vendor': 'USM'}

    validated = cal.validate(i_one)
    preprocessed = cal.preprocess(i_one)
    assert not validated
    res = cal.calculate(preprocessed)
    assert res == expected
