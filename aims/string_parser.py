from datetime import datetime


def str_to_int(string):
    if not string or string == 'FULL':
        return 0
    return int(string)


def str_to_bool(string):
    if string == 'Y':
        return True
    if string == 'N':
        return False
    raise ValueError(string + ' is not a valid boolean value')


def str_to_list(string):
    return [v.strip() for v in string.split(',')]


def str_to_date(string):
    return datetime.strptime(string, '%d/%m/%Y')


def str_to_daterange(string):
    """
    e.g. '24/01/2016 - 30/01/2016' -> (dateobject(), dateobject())
    """
    if not string:
        return (None, None)
    dates = [x.replace(' ', '') for x in string.split('-')]
    return (str_to_date(dates[0]), str_to_date(dates[1]))


def str_to_time(string):
    return int(string.replace(':', ''))


def str_to_timerange(string):
    """
    store the range as tuple
    e.g. 12:00 - 13:00 -> (1200, 1300)
    """
    if not string:
        return (None, None)
    times = string.split('-')
    return (str_to_time(times[0]), str_to_time(times[1]))
