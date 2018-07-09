def combine(base_price_dict, food_item_dict):

    d = {
        'base_price_dict': base_price_dict,
        'food_item_dict': food_item_dict
    }

    ld_price = food_item_dict['ld']
    usm_price = food_item_dict['usm']

    ld_final = base_price_dict.get('LS', 0) + ld_price
    usm_final = base_price_dict.get('USM', 0) + usm_price


    return {
        'usm_final': usm_final,
        'ld_final': ld_final,
        'all': d
    }
