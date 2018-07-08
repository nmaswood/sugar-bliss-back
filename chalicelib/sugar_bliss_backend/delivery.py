import pandas as pd
from dateutil.parser import parse
import re
import os.path

import calendar


def get_dfs():
    root = os.path.dirname(__file__)
    _dir = 'csvs/delivery/'

    files = ('city_final.csv', 'loop_final.csv', 'suburb_final.csv')
    files = [
        os.path.join(root, _dir, f)
        for f in files
    ]

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

    for idx, date_tuples in enumerate(parsed_time):

        for start_time_prime, end_time_prime in date_tuples:
            if start_time <= start_time_prime and end_time >= end_time_prime:
                time_indexes.add(idx)
                continue

    union = sorted(list(date_indexes & time_indexes))

    # TODO This truncates to a single one.
    # Should check optimal price first

    res = {}

    for index in union:
        carrier = carriers[index]
        price = row[index]
        res[carrier] = price

    return res


def return_carrier_and_prices(zipcode_df, zipcode, date, start_time, end_time):
    columns, times, carriers, row = select_rows(zipcode_df, zipcode)

    columns_prime, times_prime, carriers_prime, row_prime = filter_by_carriers(
        columns, times, carriers, row)

    info_dict = get_dict(columns_prime, times_prime, carriers_prime, row_prime,
                         date, start_time, end_time)

    return info_dict
