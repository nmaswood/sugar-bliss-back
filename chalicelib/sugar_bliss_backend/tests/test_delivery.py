import pytest
import chalicelib.sugar_bliss_backend.delivery as d
from dateutil.parser import parse


@pytest.mark.parametrize('zipcode,time,start_time,end_time,expected',
                         (
                             ('60601', parse('2018-04-19').date(),
                                 parse('10am').time(),
                                 parse('12pm').time(),
                                 {
                                     'LS': 23.75,
                                     'USM': 30.0,
                                     'multiplier': 1.25
                             }),
                         ))
def test_return_carrier_and_prices(zipcode, time, start_time, end_time,
                                   expected):
    zipcode_maps = d.zipcode_to_df(zipcode)
    res = d.return_carrier_and_prices(zipcode_maps, zipcode, time, start_time,
                                      end_time)
    assert res == expected
