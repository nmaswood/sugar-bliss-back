from typing import List

from . import app_types


def cheapest_time(
        carrier_dicts: List[app_types.CarrierDict],
        price_result: app_types.PriceResultFinal) -> app_types.ResponseObject:

    copy = [
        app_types.CarrierDict(x.carrier, x.price, x.date_, x.time_)
        for x in carrier_dicts
    ]

    for idx, carrier_dict in enumerate(copy):
        carrier = carrier_dict.carrier

        if carrier == app_types.Carrier.ld:
            carrier_dict.price += price_result.ld
        elif carrier == app_types.Carrier.usm:
            carrier_dict.price += price_result.usm

    carrier_dicts.sort(key=lambda x: x.price)
    copy.sort(key=lambda x: x.price)
    return app_types.ResponseObject(carrier_dicts, copy, price_result,
                                    bool(carrier_dicts))
