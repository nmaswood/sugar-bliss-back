def combine(base_price_dict, food_item_dict):
    d = {
        'base_price_dict': base_price_dict,
        'food_item_dict': food_item_dict
    }

    usm_absent = food_item_dict['usm_absent']
    ld_absent = food_item_dict['ld_absent']

    d['ld_final'] = (
        float(base_price_dict.get('LS', 0)) + food_item_dict['ld_sum'])

    d['usm_final'] = (
        float(base_price_dict.get('USM', 0)) + food_item_dict['usm_sum']
    )

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
