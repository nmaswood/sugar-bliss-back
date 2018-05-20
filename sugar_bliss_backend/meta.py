import csv
from glob import glob
from pdb import set_trace


def read_files():
    return glob('csvs/.csv')


FOUR = ' ' * 4


def i_none(token):
    return token in {None, '', ' '}


def process_basic(file_name):

    f = open(file_name, 'r')
    stream = csv.reader(f)

    builder = []
    function_name = file_name.split('/', 2)[1].split(".")[0]
    builder.append('def {}(dzn):\n'.format(function_name))
    builder.append(FOUR)

    next(stream)

    for idx, line in enumerate(stream):
        left, right = line[0].strip().split('-', 2)

        if idx == 0:
            verb = 'if'
        else:
            verb = 'elif'

        builder.append('{} {} <= dzn <= {}:\n'.format(verb, left, right))

        if idx == 0:
            builder.append(FOUR)
        else:
            builder.append(FOUR)

        num_bags = line[1]

        ls = line[2]
        usm = '' if len(line) == 3 else line[3]

        status = ''
        if i_none(ls) and i_none(usm):
            status = 'LS_AND_USM_NULL'
        elif i_none(ls):
            status = 'LS_NULL'
        elif i_none(usm):
            status = 'USM_NULL'
        else:
            status = 'OKAY'
        builder.append(FOUR)
        builder.append('return Status.{}, {}, {}, {}\n'.format(
            status,
            num_bags,
            ls or None,
            usm or None))
        builder.append(FOUR)

    builder.append('return Status.CUSTOM, None, None, None')
    f.close()

    return ''.join(builder)


def process_other(file_name):

    f = open(file_name, 'r')
    stream = csv.reader(f)

    builder = []
    function_name = file_name.split('/', 2)[1].split(".")[0]
    builder.append('def {}(bags):\n'.format(function_name))
    builder.append(FOUR)

    next(stream)

    for idx, line in enumerate(stream):

        num_bags = line[1]
        if idx == 0:
            verb = 'if'
        else:
            verb = 'elif'

        builder.append('{} bags == {}:\n'.format(verb, num_bags))
        builder.append(FOUR)

        num_bags = line[1]

        ls = line[2]
        usm = '' if len(line) == 3 else line[3]

        status = ''
        if i_none(ls) and i_none(usm):
            status = 'LS_AND_USM_NULL'
        elif i_none(ls):
            status = 'LS_NULL'
        elif i_none(usm):
            status = 'USM_NULL'
        else:
            status = 'OKAY'
        builder.append(FOUR)
        builder.append('return Status.{}, {}, {}, {}\n'.format(
            status,
            num_bags,
            ls or None,
            usm or None))
        builder.append(FOUR)

    builder.append('return Status.CUSTOM, None, None, None')
    f.close()

    return ''.join(builder)
