from pdb import set_trace


def combine(base_price_dict, food_item_dict):
    d = {
        'base_price_dict': base_price_dict,
        'food_item_dict': food_item_dict
    }

    usm_absent = food_item_dict['usm_absent']
    ld_absent = food_item_dict['ld_absent']

    d['ld_final'] = float(base_price_dict.get('LS', 0)) + food_item_dict['ld_sum']
    d['usm_final'] = float(base_price_dict.get('USM', 0)) + food_item_dict['usm_sum']

    if usm_absent and ld_absent:
        vendor = ''
        price = 0
    elif usm_absent:
        vendor = 'LD'
        price = d['ld_final']
    elif ld_absent:
        vendor = 'USM'
        price = d['usm_final']
    else:
        if d['ld_final'] >= d['usm_final']:
            vendor = 'USM'
            price = d['usm_final']
        else:
            vendor = 'LD'
            price = d['ld_final']

    d['vendor'] = vendor
    d['price'] = price

    return d


if __name__ == '__main__':
    base_price_dict = {
        'USM': '65.85',
        'LS': '73'
    }
    food_item_dict = {'ld_sum': 90, 'ld_count': 5, 'usm_sum': 75, 'usm_count': 4, 'warnings': [], 'custom': ['frenchMacarons'], 'per_item': {'miniCupcakes': {'status': 'OKAY', '_input': 6, 'ld': 25, 'usm': 20}, 'regularCupcakes': {'status': 'USM_NULL', '_input': 4, 'ld': 15, 'usm': None}, 'cakePops': {
        'status': 'OKAY', '_input': 3, 'ld': 10, 'usm': 15}, 'frenchMacarons': {'status': 'CUSTOM', '_input': None, 'ld': None, 'usm': None}, 'tiers': {'status': 'OKAY', '_input': 4, 'ld': 20, 'usm': 20}, 'other': {'status': 'OKAY', '_input': 4, 'ld': 20, 'usm': 20}}, 'ld_absent': False, 'usm_absent': False}

    res = combine(base_price_dict, food_item_dict)
    set_trace()
