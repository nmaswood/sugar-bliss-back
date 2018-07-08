import chalicelib.sugar_bliss_backend.delivery as delivery
import chalicelib.sugar_bliss_backend.combine as combine
import chalicelib.sugar_bliss_backend.params as params
from dateutil.parser import parse

sample = {
    'miniCupcakes': '10',
    'regularCupcakes': '20',
    'cakePops': '30',
    'frenchMacarons': '40',
    'tiers': '50',
    'other': '60',
    'zipCode': '60601',
    'dateTime': '2018-07-21',
    'time': '10am-12am'
}

FOOD_KEYS = {
    'miniCupcakes'
    'regularCupcakes'
    'cakePops'
    'frenchMacarons',
    'tiers',
    'other'
}

VALID_TIMES = {
    '8am-9am', '8am-10am', '9am-10am', '9am-11am', '10am-11am',
    '10am-12am', '11am-12pm', '12pm-1pm', '12pm-2pm', '1pm-2pm',
    '1pm-3pm', '2pm-3pm', '2pm-4pm', '3pm-4pm', '3pm-5pm', '4pm-5pm'
}

ZIP_CODE_PREFIX = '60'


def validate(obj):
    errors = []

    if obj['time'] not in VALID_TIMES:
        error = 'Time {} not in valid range of times'
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

    if not obj['zipcode'].startswith(ZIP_CODE_PREFIX):
        error = "{} is not supported zipcode. Zipcode must start with '06'"
        errors.append(error)

    for key in FOOD_KEYS:
        if obj[key] < 0:
            error = '{} cannot have negative value.'.format(key)
            errors.append(error)
        try:
            int(key)
        except Exception:
            error = 'Could not convert {} to integer.'.format(key)
            errors.append(error)

    return errors


def preprocess(obj):
    pass


def calculate(obj):
    zipcode, time = (obj['zipCode'], obj['dateTime'])
    zipcode_map = delivery.zipcode_to_df_map()
    base_price_dict = delivery.return_carrier_and_prices(
        zipcode_map,
        zipcode,
        time)
    item_price = params.price(obj)
    combined = combine.combine(base_price_dict, item_price)

    return combined
