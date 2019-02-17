import calendar
import os.path
import re
from pdb import set_trace

import pandas as pd
from dateutil.parser import parse


def get_overlap(a, b):

    left, right = a

    left_hour, right_hour = left.hour, right.hour

    left_prime, right_prime = b

    left_prime_hour, right_prime_hour = left_prime.hour, right_prime.hour
    return max(
        0,
        min(right_hour, right_prime_hour) - max(left_hour, left_prime_hour))


def get_dfs():
    root = os.path.dirname(__file__)
    _dir = 'csvs/delivery/'

    files = ('city.csv', 'loop.csv', 'suburb.csv')
    files = [os.path.join(root, _dir, f) for f in files]

    def process_df(filename):
        df = pd.read_csv(filename)
        df.Zipcode = df.Zipcode.astype(str)
        return df

    return [process_df(f) for f in files]


def zipcode_to_df(zipcode):

    dfs = get_dfs()

    for df in dfs:
        row = df[df.Zipcode == zipcode]
        if not row.empty:
            return df

    return None


def select_rows(df, zipcode):
    row = df[df.Zipcode == zipcode]

    columns = df.columns
    times = df.loc[0].values
    carriers = df.loc[1].values
    return columns, times, carriers, row.values[0]


def filter_by_carriers(columns, times, carriers, row):

    carrier_indexes = []

    for index, carrier in enumerate(carriers):
        if carrier.strip().startswith('Sugar Bliss'):
            carrier_indexes.append(index)

    times_prime = [times[index].strip() for index in carrier_indexes]

    carrier_regex = re.compile('.*(USM|LS|LD|usm|ls|ld).*')

    carriers_prime = [
        carrier_regex.match(carriers[index]).group(1)
        for index in carrier_indexes
    ]

    columns_prime = [
        re.sub(r'[^a-zA-Z\- ()]+', '', columns[index]).strip()
        for index in carrier_indexes
    ]
    row_prime = [row[index] for index in carrier_indexes]

    return columns_prime, times_prime, carriers_prime, row_prime


def parse_date(string):
    string = string.replace('only', '')
    splitted = string.split('-', 1)
    day_to_number_map = dict(zip(list(calendar.day_abbr), range(7)))
    mapped = [day_to_number_map[x[:3]] for x in splitted]

    return mapped


def parse_single_unit(string):
    # for now just ignore monday thorough friday only
    no_parens = re.sub(r'\([^)]*\)', '', string)
    left, right = no_parens.split('-', 1)

    return (parse(left).time(), parse(right).time())


def parse_time(string):

    string = string.replace(' ', '')
    by_comma = string.split(',')

    return [parse_single_unit(x) for x in by_comma]


def determine_multiplier(start_time, end_time):
    time_window_difference = end_time.hour - start_time.hour
    eight_am = parse('8am').time()
    four_pm = parse('4pm').time()

    multiplier = 1
    # if start_time < eight_am:
    # multiplier *= 2
    # if end_time > four_pm:
    # multiplier *= 2

    # if time_window_difference == 1:
    # multiplier *= 1.5
    # elif time_window_difference == 2:
    # multiplier *= 1.25

    return multiplier


def get_dict(columns, times, carriers, row, date, start_time, end_time):

    weekday = date.weekday()
    parsed_dates = [parse_date(x) for x in columns]

    date_indexes = set()

    for idx, as_number_range in enumerate(parsed_dates):

        if len(as_number_range) == 1:
            if as_number_range[0] == weekday:
                date_indexes.add(idx)
        elif len(as_number_range) == 2:
            left, right = as_number_range
            if left <= weekday <= right:
                date_indexes.add(idx)
        else:
            raise ValueError('Had three dashes...?')

    parsed_time = [parse_time(x) for x in times]

    time_indexes = set()

    parsed_time_tuple = {}

    time_tuple = start_time, end_time

    for idx, date_tuples in enumerate(parsed_time):
        for idx_prime, time_tuple_prime in enumerate(date_tuples):

            overlap = get_overlap(time_tuple, time_tuple_prime)
            if overlap:
                parsed_time_tuple[idx] = idx_prime
                time_indexes.add(idx)

    union = sorted(list(date_indexes & time_indexes))

    # TODO This truncates to a single one.
    # Should check optimal price first

    multiplier = determine_multiplier(start_time, end_time)

    carrier_prices = []

    for index in sorted(union):
        carrier = carriers[index]
        price = float(row[index])

        date = parsed_dates[index]
        if len(date) == 1:
            first = date[0]
            date = calendar.day_abbr[first]
        elif len(date) == 2:
            first, second = date[0], date[1]
            date = '{}-{}'.format(calendar.day_abbr[first],
                                  calendar.day_abbr[second])
        else:
            return {'status': 'fail', 'errors': 'Invalid date range'}

        times = parsed_time[index]
        time = times[parsed_time_tuple[index]]

        if len(time) == 1:
            first = time[0]
            time = str(first)
        elif len(time) == 2:
            first = time[0]
            second = time[1]
            time = '{}-{}'.format(first, second)
        else:
            return {'status': 'fail', 'errors': 'Invalid time range'}

        carrier_prices.append({
            'carrier': carrier,
            'price': price * multiplier,
            'date': date,
            'time': time
        })

    if not carrier_prices:
        return {
            'status': 'fail',
            'errors': 'Could not find a valid time for either carrier.'
        }

    return {
        'status': 'success',
        'multiplier': multiplier,
        'carrier_prices': carrier_prices,
    }


def return_carrier_and_prices(zipcode_df, zipcode, date, start_time, end_time):
    columns, times, carriers, row = select_rows(zipcode_df, zipcode)

    columns_prime, times_prime, carriers_prime, row_prime = filter_by_carriers(
        columns, times, carriers, row)

    return get_dict(columns_prime, times_prime, carriers_prime, row_prime,
                    date, start_time, end_time)
