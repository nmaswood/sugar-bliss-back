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


def process_zipcodes(df):
    codes = set(df['Zipcode'].values[2:])
    codes = {code.replace('.0', '') for code in codes}
    return codes, df


def zipcode_to_df_map():
    dfs = get_dfs()
    return [process_zipcodes(df) for df in dfs]


def zipcode_to_df(zipcode_maps, zipcode, time):
    for zipcode_map, df in zipcode_maps:
        if zipcode in zipcode_map:
            return df
    return None


def select_rows(df, zipcode, time):

    row = df[df.Zipcode == zipcode]
    if row.empty:
        raise 'Nothing matched with that zipcode...'
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
    carriers_prime = [
        carriers[index].replace('Sugar Bliss Price using', '').strip()
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
    splitted = string.split('-')
    day_to_number_map = dict(zip(list(calendar.day_abbr), range(7)))
    mapped = [day_to_number_map[x[:3]] for x in splitted]

    return splitted, mapped


def parse_single_unit(string):
    # for now just ignore monday thorough friday only
    if '(' in string:
        string = string.split('(', 1)[0]

    left, right = string.split('-', 1)
    return [parse(left).hour, parse(right).hour]


def parse_time(string):
    string = string.replace(' ', '')

    by_comma = string.split(',')
    parsed = sum([parse_single_unit(x) for x in by_comma], [])
    return min(parsed), max(parsed)


def get_dict(columns, times, carriers, row, time):
    weekday = time.weekday()
    parsed_dates = [parse_date(x) for x in columns]

    date_indexes = set()

    for idx, (_, as_number_range) in enumerate(parsed_dates):
        if len(as_number_range) == 1 and as_number_range[0] == weekday:
            date_indexes.add(idx)
        if len(as_number_range) == 2:
            left, right = as_number_range
            if left <= weekday <= right:
                date_indexes.add(idx)
    parsed_time = [parse_time(x) for x in times]

    time_indexes = set()
    hour = time.hour

    for idx, (left, right) in enumerate(parsed_time):

        if left <= hour <= right:
            time_indexes.add(idx)

    union = sorted(list(date_indexes & time_indexes))

    carriers_prime = [carriers[index] for index in union]
    row_prime = [row[index] for index in union]

    res = dict(zip(carriers_prime, row_prime))

    return res


def return_carrier_and_prices(zipcode_map, zipcode, time):
    df = zipcode_to_df(zipcode_map, zipcode, None)
    columns, times, carriers, row = select_rows(df, zipcode, None)
    parsed_time = parse(time).astimezone()
    (
        columns_prime, times_prime, carriers_prime,
        row_prime) = filter_by_carriers(columns, times, carriers, row)

    info_dict = get_dict(columns_prime, times_prime, carriers_prime, row_prime,
                         parsed_time)

    return info_dict
