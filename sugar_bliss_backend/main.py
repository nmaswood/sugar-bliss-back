import delivery
import combine
import params


def calculate(obj):
    zipcode, time = (obj['zipCode'], obj['dateTime'])
    base_price_dict = delivery.return_carrier_and_prices_global(zipcode, time)
    item_price = params.price(obj)
    combined = combine.combine(base_price_dict, item_price)

    return combined

