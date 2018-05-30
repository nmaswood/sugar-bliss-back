import sugar_bliss_backend.combine as c


BASE_PRICES = {
    'USM': '65.85',
    'LS': '73'
}

FOOD_ITEMS = {
    'ld_sum': 90,
    'ld_count': 5,
    'usm_sum': 75,
    'usm_count': 4,
    'warnings': [],
    'custom': ['frenchMacarons'],
    'per_item': {'miniCupcakes': {'status': 'OKAY',
                                  '_input': 6,
                                  'ld': 25,
                                  'usm': 20},
                 'regularCupcakes': {'status': 'USM_NULL',
                                     '_input': 4,
                                     'ld': 15,
                                     'usm': None},
                 'cakePops': {
        'status': 'OKAY',
        '_input': 3,
        'ld': 10,
        'usm': 15},
        'frenchMacarons': {'status': 'CUSTOM',
                           '_input': None,
                           'ld': None,
                           'usm': None},
        'tiers': {'status': 'OKAY',
                  '_input': 4,
                  'ld': 20,
                  'usm': 20},
        'other': {'status': 'OKAY',
                  '_input': 4,
                  'ld': 20,
                  'usm': 20}},
    'ld_absent': False,
    'usm_absent': False
}
FOOD_ITEMS_EXPECTED = {'base_price_dict': {'LS': '73', 'USM': '65.85'},
                       'food_item_dict': {'custom': ['frenchMacarons'],
                                          'ld_absent': False,
                                          'ld_count': 5,
                                          'ld_sum': 90,
                                          'per_item': {'cakePops': {'_input': 3,
                                                                    'ld': 10,
                                                                    'status': 'OKAY',
                                                                    'usm': 15},
                                                       'frenchMacarons': {'_input': None,
                                                                          'ld': None,
                                                                          'status': 'CUSTOM',
                                                                          'usm': None},
                                                       'miniCupcakes': {'_input': 6,
                                                                        'ld': 25,
                                                                        'status': 'OKAY',
                                                                        'usm': 20},
                                                       'other': {'_input': 4,
                                                                 'ld': 20,
                                                                 'status': 'OKAY',
                                                                 'usm': 20},
                                                       'regularCupcakes': {'_input': 4,
                                                                           'ld': 15,
                                                                           'status': 'USM_NULL',
                                                                           'usm': None},
                                                       'tiers': {'_input': 4,
                                                                 'ld': 20,
                                                                 'status': 'OKAY',
                                                                 'usm': 20}},
                                          'usm_absent': False,
                                          'usm_count': 4,
                                          'usm_sum': 75,
                                          'warnings': []},
                       'ld_final': 163.0,
                       'price': 140.85,
                       'usm_final': 140.85,
                       'vendor': 'USM'}


def test_combine():
    assert c.combine(BASE_PRICES, FOOD_ITEMS) == FOOD_ITEMS_EXPECTED
