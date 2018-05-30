import pytest
import sugar_bliss_backend.delivery as d


@pytest.mark.parametrize('zipcode,time,expected',
                         (
                             ('60601', '2018-04-19T12:00', {
                                 'LS': '19',
                                 'USM': '24'
                             }),
                         ))
def test_return_carrier_and_prices(zipcode, time, expected):
    zipcode_maps = d.zipcode_to_df_map()
    res = d.return_carrier_and_prices(zipcode_maps, zipcode, time)
    assert res == expected
