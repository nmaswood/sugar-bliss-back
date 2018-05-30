from enum import Enum
from pdb import set_trace

DZN = {'cakePops', 'frenchMacarons', 'miniCupcakes', 'regularCupcakes'}
BAG = {'other', 'tiers'}


class Status(Enum):
    LD_NULL = 1
    USM_NULL = 2
    LD_AND_USM_NULL = 3
    CUSTOM = 4
    OKAY = 5
    NIL = 6


def _mini_cupcakes(dzn):

    if dzn == 0:
        return Status.NIL, 0, None, None

    if 1 <= dzn <= 8:
        return Status.LD_AND_USM_NULL, 1, None, None
    elif 9 <= dzn <= 16:
        return Status.USM_NULL, 2, 5, None
    elif 17 <= dzn <= 24:
        return Status.USM_NULL, 3, 10, None
    elif 25 <= dzn <= 32:
        return Status.USM_NULL, 4, 15, None
    elif 33 <= dzn <= 40:
        return Status.OKAY, 5, 20, 10
    elif 41 <= dzn <= 48:
        return Status.OKAY, 6, 25, 20
    elif 49 <= dzn <= 56:
        return Status.OKAY, 7, 30, 30

    return Status.CUSTOM, None, None, None


def _regular_cupcakes(dzn):

    if dzn == 0:
        return Status.NIL, 0, None, None

    if 1 <= dzn <= 4:
        return Status.LD_AND_USM_NULL, 1, None, None
    elif 5 <= dzn <= 8:
        return Status.USM_NULL, 2, 5, None
    elif 9 <= dzn <= 12:
        return Status.USM_NULL, 3, 10, None
    elif 13 <= dzn <= 16:
        return Status.USM_NULL, 4, 15, None
    elif 17 <= dzn <= 20:
        return Status.OKAY, 5, 20, 10
    elif 21 <= dzn <= 24:
        return Status.OKAY, 6, 25, 20
    elif 25 <= dzn <= 28:
        return Status.OKAY, 7, 30, 30
    elif 29 <= dzn <= 32:
        return Status.OKAY, 8, 35, 40
    elif 33 <= dzn <= 36:
        return Status.OKAY, 9, 40, 50
    elif 37 <= dzn <= 40:
        return Status.OKAY, 10, 45, 60
    elif 41 <= dzn <= 44:
        return Status.OKAY, 11, 50, 70
    elif 45 <= dzn <= 48:
        return Status.OKAY, 12, 55, 80
    elif 49 <= dzn <= 52:
        return Status.OKAY, 13, 60, 90
    return Status.CUSTOM, None, None, None


def _cake_pops(dzn):
    if dzn == 0:
        return Status.NIL, 0, None, None

    if 1 <= dzn <= 22:
        return Status.LD_AND_USM_NULL, 1, None, None
    elif 23 <= dzn <= 44:
        return Status.USM_NULL, 2, 5, None
    elif 45 <= dzn <= 66:
        return Status.OKAY, 3, 10, 15
    elif 67 <= dzn <= 88:
        return Status.OKAY, 4, 15, 20
    elif 89 <= dzn <= 110:
        return Status.OKAY, 5, 20, 30
    return Status.CUSTOM, None, None, None


def _french_macarons(dzn):
    if dzn == 0:
        return Status.NIL, 0, None, None

    if 1 <= dzn <= 16:
        return Status.LD_AND_USM_NULL, 1, None, None
    elif 17 <= dzn <= 32:
        return Status.USM_NULL, 2, 5, None
    elif 33 <= dzn <= 48:
        return Status.USM_NULL, 3, 10, None
    elif 49 <= dzn <= 64:
        return Status.USM_NULL, 4, 15, None
    elif 65 <= dzn <= 79:
        return Status.OKAY, 5, 20, 30
    return Status.CUSTOM, None, None, None


def _tiers(bags):

    if bags == 0:
        return Status.NIL, 0, None, None

    if bags == 1:
        return Status.OKAY, 1,  5,  5
    elif bags == 2:
        return Status.OKAY, 2,  10, 10
    elif bags == 3:
        return Status.OKAY, 3,  15, 15
    elif bags == 4:
        return Status.OKAY, 4,  20, 20
    elif bags == 5:
        return Status.OKAY, 5,  25, 25
    return Status.CUSTOM, None, None, None


def _other(bags):
    if bags == 0:
        return Status.NIL, 0, None, None

    if bags == 1:
        return Status.OKAY, 1, 5, 5
    elif bags == 2:
        return Status.OKAY, 2, 10, 10
    elif bags == 3:
        return Status.OKAY, 3, 15, 15
    elif bags == 4:
        return Status.OKAY, 4, 20, 20
    elif bags == 5:
        return Status.OKAY, 5, 25, 25
    return Status.CUSTOM, None, None, None


FUNCTIONS_DICT = {
    'cakePops': _cake_pops,
    'frenchMacarons': _french_macarons,
    'miniCupcakes': _mini_cupcakes,
    'other': _other,
    'regularCupcakes': _regular_cupcakes,
    'tiers': _tiers
}


def _convert_numeric_inner(data_obj):
    copy = dict(data_obj)

    keys = {
        'cakePops', 'frenchMacarons', 'miniCupcakes',
        'regularCupcakes', 'other', 'tiers'
    }

    for key in keys:

        value = copy[key]
        copy[key] = int(float(value))

    return copy


def _convert_numeric(data_obj):
    try:
        return 200, _convert_numeric_inner(data_obj)
    except Exception as e:
        return 401, e


def _sanitize(data_obj):
    copy = dict(data_obj)

    for key, value in copy.items():

        if value < 0:
            copy[key] = 0

    return 200, copy


def _filter(data_obj):

    return 200, {
        k: v for k, v in data_obj.items() if
        k in DZN or k in BAG
    }


def _food_item_pricing(data_obj):

    d = {
        'ld_sum': 0,
        'ld_count': 0,
        'usm_sum': 0,
        'usm_count': 0,
        'warnings': [],
        'custom': [],
        'per_item': {}
    }

    for name, value in data_obj.items():

        f = FUNCTIONS_DICT[name]
        status, _input, ld, usm = f(value)

        d['per_item'][name] = {
            'status': str(status).split('.', 1)[-1],
            '_input': _input,
            'ld': ld,
            'usm': usm,
        }

        d['ld_absent'] = False
        d['usm_absent'] = False

        if status == Status.NIL:
            pass
        elif status == Status.LD_NULL:
            d['usm_count'] += 1
            d['usm_sum'] += usm
            d['ld_absent'] = True
        elif status == Status.USM_NULL:
            d['ld_count'] += 1
            d['ld_sum'] += ld

            d['usm_absent'] = True
        elif status == Status.LD_AND_USM_NULL:
            d['ld_absent'] = True
            d['usm_absent'] = True
            pass
        elif status == Status.CUSTOM:
            d['custom'].append(name)
        elif status == Status.OKAY:
            d['ld_count'] += 1
            d['ld_sum'] += ld
            d['usm_count'] += 1
            d['usm_sum'] += usm

    return d


def price(data_object):

    copy = dict(data_object)

    preprocess = (
        _filter,
        _convert_numeric,
        _sanitize
    )

    for f in preprocess:

        res, copy = f(copy)

        if res != 200:
            raise Exception(f'{res} has been raised in {f}')

    return _food_item_pricing(copy)
