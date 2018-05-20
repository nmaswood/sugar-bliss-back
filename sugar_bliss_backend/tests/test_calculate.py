from pdb import set_trace
import sugar_bliss_backend.calculate as cal


def generate_results():
    i_one = {
        'miniCupcakes': '25',
        'regularCupcakes': 0,
        'cakePops': 0,
        'frenchMacarons': 0,
        'tiers': 0,
        'other': 0,
        'zipCode': '60601',
        'dateTime': '2018-05-16T10:00'
    }


def test_calculate():
    i_one = {
        'miniCupcakes': '25',
        'regularCupcakes': 0,
        'cakePops': 0,
        'frenchMacarons': 0,
        'tiers': 0,
        'other': 0,
        'zipCode': '60601',
        'dateTime': '2018-05-16T10:00'
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

    res = cal.calculate(i_one)
    assert res == expected
