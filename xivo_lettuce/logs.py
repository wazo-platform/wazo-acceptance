import datetime

ASTERISK_DATE_FORMAT = "[%b %d %H:%M:%S]"
ASTERISK_DATE_LEN = 17


def add_year_to_datetime(ts, year=None):
    year = year or datetime.datetime.now().year
    timestamp = datetime.datetime(
        year=year,
        month=ts.month,
        day=ts.day,
        hour=ts.hour,
        minute=ts.minute,
        second=ts.second)

    return timestamp


def read_last_log_lines(text, min_timestamp):

    current_year = datetime.datetime.now().year

    lines = text.split("\n")
    for line in lines:
        datetext = line[0:ASTERISK_DATE_LEN]

        timestamp = datetime.datetime.strptime(datetext, ASTERISK_DATE_FORMAT)
        timestamp = add_year_to_datetime(timestamp)

        if timestamp >= min_timestamp:
            lines.append(line)

    return lines
