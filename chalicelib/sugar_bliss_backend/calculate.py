import chalicelib.sugar_bliss_backend.delivery as delivery
import chalicelib.sugar_bliss_backend.combine as combine
import chalicelib.sugar_bliss_backend.params as params
from dateutil.parser import parse


FOOD_KEYS = {
    'miniCupcakes',
    'regularCupcakes',
    'cakePops',
    'frenchMacarons',
    'tiers',
    'other'
}

VALID_TIMES = {
    '7am-8am', '7am-9am',
    '8am-9am', '8am-10am', '9am-10am', '9am-11am', '10am-11am',
    '10am-12pm', '11am-12pm', '12pm-1pm', '12pm-2pm', '1pm-2pm',
    '1pm-3pm', '2pm-3pm', '2pm-4pm', '3pm-4pm', '3pm-5pm', '4pm-5pm'
}

ZIP_CODE_PREFIX = '60'


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
        error = "{} is not supported zipcode. Zipcode must start with '06'".format(obj['zipCode'])
        errors.append(error)

    for key in FOOD_KEYS:
        try:
            int(obj[key])
        except Exception:
            error = 'Could not convert {} to integer.'.format(key)
            errors.append(error)

        if int(obj[key]) < 0:
            error = '{} cannot have negative value.'.format(key)
            errors.append(error)

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


def calculate(obj):
    zipcode = obj['zipCode']
    date = obj['date']
    start_time = obj['time_start']
    end_time = obj['time_end']


    zipcode_map = delivery.get_dfs()
    assert 0

    base_price_dict = delivery.return_carrier_and_prices(
        zipcode_map,
        zipcode,
        time)
    item_price = params.price(obj)
    combined = combine.combine(base_price_dict, item_price)

    return combined
