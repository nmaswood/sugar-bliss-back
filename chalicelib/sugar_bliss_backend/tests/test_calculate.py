from pdb import set_trace
import chalicelib.sugar_bliss_backend.calculate as cal
from dateutil.parser import parse


def generate_results():

    sample = {
        'miniCupcakes': '10',
        'regularCupcakes': '20',
        'cakePops': '30',
        'frenchMacarons': '40',
        'tiers': '3',
        'other': '3',
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

    assert 'Number -1 for other is out of the range 1-5' in negative_errors

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
        'tiers': 3,
        'other': 3,
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
    expected = {'status': 'success', 'data': {'base_price_dict': {'status': 'success', 'multiplier': 1, 'carrier_prices': [{'carrier': 'LS', 'price': 19, 'date': 'Mon-Sun', 'time': '11:00:00-13:00:00'}, {'carrier': 'USM', 'price': 24, 'date': 'Mon-Fri', 'time': '11:00:00-13:00:00'}], 'best_ld_carrier': {'carrier': 'LS', 'price': 19, 'date': 'Mon-Sun', 'time': '11:00:00-13:00:00'}, 'best_ld_price': 34, 'best_usm': {'carrier': 'USM', 'price': 24, 'date': 'Mon-Fri', 'time': '11:00:00-13:00:00'}, 'best_usm_price': 24}, 'food_item_dict': {'ld': 15, 'usm': 0, 'custom': [], 'per_item': {'frenchMacarons': {'status': 'NIL', '_input': 0, 'ld': None, 'usm': None}, 'regularCupcakes': {'status': 'NIL', '_input': 0, 'ld': None, 'usm': None}, 'miniCupcakes': {'status': 'OKAY', '_input': 25, 'ld': 15, 'usm': 0}, 'tiers': {'status': 'NIL', '_input': 0, 'ld': None, 'usm': None}, 'other': {'status': 'NIL', '_input': 0, 'ld': None, 'usm': None}, 'cakePops': {'status': 'NIL', '_input': 0, 'ld': None, 'usm': None}}}}}



    errors = cal.validate(i_one)
    assert not errors
    preprocessed = cal.preprocess(i_one)

    food_obj, time_obj = cal.split_data(preprocessed)

    res = cal.calculate(food_obj, time_obj)
    assert res == expected
