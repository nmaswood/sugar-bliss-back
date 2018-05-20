import sugar_bliss_backend.delivery as delivery
import sugar_bliss_backend.combine as combine
import sugar_bliss_backend.params as params


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
