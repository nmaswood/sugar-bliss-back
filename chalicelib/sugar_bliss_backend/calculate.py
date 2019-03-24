from typing import Any, Dict, List

from dateutil.parser import parse

from . import app_types, combine, constants, delivery, params


def validate(obj: Dict[str, str]) -> List[str]:
    errors = []
    if obj['time'] not in constants.TIMES:
        error = 'Time {} not in valid range of times'.format(obj['time'])
        errors.append(error)

    try:
        date = parse(obj['dateTime'])
    except Exception as e:
        error = 'Could not parse date due to {}'.format(str(e))
        errors.append(error)

    if date.date().weekday() == 6:
        error = 'Cannot specify a Sunday'
        errors.append(error)

    non_zero = False

    for key in constants.FOOD_KEYS:
        try:
            num = int(obj[key])
        except Exception:
            error = 'Could not convert {} to integer.'.format(key)
            errors.append(error)

        food_min, food_max = constants.FOOD_MAXS[key]
        if num != 0:
            non_zero = True
        if not (food_min <= num <= food_max):
            error = 'Number {} for {} is out of the range {}-{}'.format(
                num, key, food_min, food_max)
            errors.append(error)

    if not non_zero:
        errors.append('All values posted were 0')

    return errors


def preprocess(obj: Dict[str, str]) -> app_types.CalculationInput:

    date = parse(obj['dateTime']).date()

    splat = obj['time'].split('-', 1)
    time_start = parse(splat[0]).time()
    time_end = parse(splat[1]).time()

    mapping: Dict[str, int] = {
        k: int(v)
        for k, v in obj.items() if k in constants.FOOD_KEYS
    }
    zipcode = obj['zipcode']

    return app_types.CalculationInput(date, time_start, time_end, zipcode,
                                      mapping)


def calculate(calculation_input: app_types.CalculationInput) -> Dict[str, Any]:

    zipcode_df = delivery.zipcode_to_df(calculation_input.zipcode)

    carrier_dicts: List[app_types.
                        CarrierDict] = delivery.return_carrier_and_prices(
                            calculation_input, zipcode_df)

    prices_dict: app_types.PriceResultFinal = params.price(
        calculation_input.mapping)
    breakpoint()
    return combine.combine(carrier_dicts, prices_dict)
