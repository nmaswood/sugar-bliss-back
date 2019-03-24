from . import app_types


def _mini_cupcakes(dzn) -> app_types.PriceResult:
    if 0 <= dzn <= 8:
        return app_types.PriceResult(0, 0)
    elif 9 <= dzn <= 16:
        return app_types.PriceResult(5, 0)
    elif 17 <= dzn <= 24:
        return app_types.PriceResult(10, 0)
    elif 25 <= dzn <= 32:
        return app_types.PriceResult(15, 0)
    elif 33 <= dzn <= 40:
        return app_types.PriceResult(20, 10)
    elif 41 <= dzn <= 48:
        return app_types.PriceResult(25, 20)
    elif 49 <= dzn <= 56:
        return app_types.PriceResult(30, 30)

    raise app_types.PriceException()


def _regular_cupcakes(dzn):

    if 0 <= dzn <= 4:
        return app_types.PriceResult(0, 0)
    elif 5 <= dzn <= 8:
        return app_types.PriceResult(5, 0)
    elif 9 <= dzn <= 12:
        return app_types.PriceResult(10, 0)
    elif 13 <= dzn <= 16:
        return app_types.PriceResult(15, 0)
    elif 17 <= dzn <= 20:
        return app_types.PriceResult(20, 10)
    elif 21 <= dzn <= 24:
        return app_types.PriceResult(25, 20)
    elif 25 <= dzn <= 28:
        return app_types.PriceResult(30, 30)
    elif 29 <= dzn <= 32:
        return app_types.PriceResult(35, 40)
    elif 33 <= dzn <= 36:
        return app_types.PriceResult(40, 50)
    elif 37 <= dzn <= 40:
        return app_types.PriceResult(45, 60)
    elif 41 <= dzn <= 44:
        return app_types.PriceResult(50, 70)
    elif 45 <= dzn <= 48:
        return app_types.PriceResult(55, 80)
    elif 49 <= dzn <= 52:
        return app_types.PriceResult(60, 90)

    raise app_types.PriceException()


def _cake_pops(dzn):
    if 0 <= dzn <= 22:
        return app_types.PriceResult(0, 0)
    elif 23 <= dzn <= 44:
        return app_types.PriceResult(5, 0)
    elif 45 <= dzn <= 66:
        return app_types.PriceResult(10, 15)
    elif 67 <= dzn <= 88:
        return app_types.PriceResult(15, 20)
    elif 89 <= dzn <= 110:
        return app_types.PriceResult(20, 30)

    raise app_types.PriceException()


def _french_macarons(dzn):
    if 0 <= dzn <= 16:
        return app_types.PriceResult(0, 0)
    elif 17 <= dzn <= 32:
        return app_types.PriceResult(5, 0)
    elif 33 <= dzn <= 48:
        return app_types.PriceResult(10, 0)
    elif 49 <= dzn <= 64:
        return app_types.PriceResult(15, 0)
    elif 65 <= dzn <= 79:
        return app_types.PriceResult(20, 30)

    raise app_types.PriceException()


def _tiers(bags):
    if bags >= 6:
        raise app_types.PriceException()

    price = bags * 5
    return app_types.PriceResult(price, price)


_other = _tiers

FUNCTIONS_DICT = {
    'cakePops': _cake_pops,
    'frenchMacarons': _french_macarons,
    'miniCupcakes': _mini_cupcakes,
    'other': _other,
    'regularCupcakes': _regular_cupcakes,
    'tiers': _tiers
}

FUNCTIONS_DICT = {
    'cakePops': _cake_pops,
    'frenchMacarons': _french_macarons,
    'miniCupcakes': _mini_cupcakes,
    'other': _other,
    'regularCupcakes': _regular_cupcakes,
    'tiers': _tiers
}


def empty_dict():
    return {
        'cakePops': 0,
        'frenchMacarons': 0,
        'miniCupcakes': 0,
        'other': 0,
        'regularCupcakes': 0,
        'tiers': 0
    }


def price(food_obj) -> app_types.PriceResultFinal:

    ld_dict = empty_dict()
    usm_dict = empty_dict()
    ld_total = 0
    usm_total = 0
    for name, value in food_obj.items():

        f = FUNCTIONS_DICT[name]
        price_result = f(value)
        ld_dict[name] = price_result.ld
        usm_dict[name] = price_result.usm
        ld_total += price_result.ld
        usm_total += price_result.usm

    return app_types.PriceResultFinal(ld_total, usm_total, ld_dict, usm_dict)
