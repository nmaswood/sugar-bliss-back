import chalicelib.sugar_bliss_backend.delivery as delivery
import chalicelib.sugar_bliss_backend.combine as combine
import chalicelib.sugar_bliss_backend.params as params
from dateutil.parser import parse

from pdb import set_trace


FOOD_KEYS = {
    'cakePops',
    'frenchMacarons',
    'miniCupcakes',
    'other',
    'regularCupcakes',
    'tiers',
}

OTHER_KEYS = {
    'zipCode',
    'dateTime',
    'time_start',
    'time_end'
}

VALID_TIMES = {
    '7am-8am', '7am-9am',
    '8am-9am', '8am-10am', '9am-10am', '9am-11am', '10am-11am',
    '10am-12pm', '11am-12pm', '12pm-1pm', '12pm-2pm', '1pm-2pm',
    '1pm-3pm', '2pm-3pm', '2pm-4pm', '3pm-4pm', '3pm-5pm', '4pm-5pm'
}

ZIP_CODE_PREFIX = '60'

FOOD_MAXS = {
    'miniCupcakes': (1, 56),
    'regularCupcakes': (1, 52),
    'cakePops': (1, 110),
    'frenchMacarons': (1, 79),
    'tiers': (1, 5),
    'other': (1, 5)
}


def validate(obj):
    errors = []

    if obj['time'] not in VALID_TIMES:
        error = 'Time {} not in valid range of times'.format(obj['time'])
        errors.append(error)

    try:
        date = parse(obj['dateTime'])
        date = date.date()
        if date.weekday() == 6:
            error = 'Cannot specify a Sunday'
            errors.append(error)
    except Exception as e:
        error = 'Could not parse date due to {}'.format(str(e))
        errors.append(error)

    if not obj['zipCode'].startswith(ZIP_CODE_PREFIX):
        error = "{} is not supported zipcode. Zipcode must start with '06'".format(
            obj['zipCode'])
        errors.append(error)

    non_zero = False
    for key in FOOD_KEYS:
        # if key not in obj:
            # continue
        try:
            num = int(obj[key])
        except Exception:
            error = 'Could not convert {} to integer.'.format(key)
            errors.append(error)

        food_min, food_max = FOOD_MAXS[key]
        if num != 0:
            non_zero = True
            if not (food_min <= num <= food_max):
                error = 'Number {} for {} is out of the range {}-{}'.format(
                        num, key, food_min, food_max)
                errors.append(error)

    if not non_zero:
        errors.append('All values posted were 0')

    return errors


def preprocess(obj):

    new_obj = {}
    date = parse(obj['dateTime'])
    new_obj['date'] = date.date()

    splat = obj['time'].split('-', 1)
    new_obj['time_start'] = parse(splat[0]).time()
    new_obj['time_end'] = parse(splat[1]).time()

    for key in FOOD_KEYS:
        new_obj[key] = int(obj[key])

    new_obj['zipCode'] = obj['zipCode']

    return new_obj


def split_data(obj):

    food_obj = {
        k: v for k, v in obj.items()
        if k in FOOD_KEYS
    }

    time_obj = {
        k: v for k, v in obj.items()
        if k not in FOOD_KEYS
    }

    return food_obj, time_obj


def calculate(food_obj, time_obj):

    zipcode = time_obj['zipCode']
    date = time_obj['date']
    start_time = time_obj['time_start']
    end_time = time_obj['time_end']

    zipcode_df = delivery.zipcode_to_df(zipcode)


    if zipcode_df is None:
        return {
            'status': 'fail',
            'errors': ['Could not find zipcode in data']
        }

    base_price_dict = delivery.return_carrier_and_prices(zipcode_df,
                                                         zipcode,
                                                         date,
                                                         start_time,
                                                         end_time)

    if not base_price_dict or base_price_dict['status'] == 'fail':
        return {
            'status': 'fail',
            'errors': ['Calculation failed while finding base price.']
        }

    prices_dict = params.price(food_obj)

    # if prices_dict['ld'] == 0 and prices_dict['usm'] == 0 and not prices_dict['custom']:
        # return {
            # 'status': 'fail',
            # 'errors': ['Could not calculate price for carriers.']
        # }

    combined = combine.combine(base_price_dict, prices_dict)
    return {
        'status': 'success',
        'data': combined
    }
