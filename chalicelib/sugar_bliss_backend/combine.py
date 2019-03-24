from typing import List

from . import app_types


def cheapest_time(
        carrier_dicts: List[app_types.CarrierDict],
        price_result: app_types.PriceResultFinal) -> app_types.ResponseObject:

    ld = None
    min_ld = float('inf')

    usm = None
    min_usm = float('inf')

    for idx, carrier_dict in enumerate(carrier_dicts):

        carrier = carrier_dict.carrier
        price = carrier_dict.price

        if carrier == app_types.Carrier.ld:
            min_ld = min(min_ld, price)
            ld = carrier_dict
        elif carrier == app_types.Carrier.usm:
            min_usm = min(min_usm, price)
            usm = carrier_dict

    if ld is None and usm is None:

        return app_types.ResponseObject(
            carrier_dicts,
            price_result,
            None,
            None,
            False,
        )

    ld_total = min_ld + price_result.ld
    usm_total = min_usm + price_result.usm

    cheapest_price = min(ld_total, usm_total)

    if ld_total < usm_total:
        cheapest_carrier = ld
    else:
        cheapest_carrier = usm

    return app_types.ResponseObject(
        carrier_dicts,
        price_result,
        cheapest_carrier,
        cheapest_price,
        True,
    )
