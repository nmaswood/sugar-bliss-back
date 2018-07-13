def combine(base_price_dict, food_item_dict):

    d = {
        'base_price_dict': base_price_dict,
        'food_item_dict': food_item_dict
    }

    min_ld = float('inf')
    min_ld_i = -1

    min_usm = float('inf')
    min_usm_i = -1

    carrier_prices = base_price_dict['carrier_prices']

    for idx, carrier_price in enumerate(carrier_prices):

        carrier = carrier_price['carrier']
        price = carrier_price['price']

        if carrier.lower() == 'ls':
            min_ld = min(min_ld, price)
            min_ld_i = idx
        elif carrier.lower() == 'usm':
            min_usm = min(min_usm, price)
            min_usm_i = idx

    if min_ld_i != -1:
        base_price_dict['best_ld_carrier'] = carrier_prices[min_ld_i]
        base_price_dict['best_ld_price'] = food_item_dict['ld'] + min_ld

    if min_usm_i != -1:
        base_price_dict['best_usm'] = carrier_prices[min_usm_i]
        base_price_dict['best_usm_price'] = food_item_dict['usm'] + min_usm

    return d
