# get the time difference
# pylint: disable=missing-docstring


def months_difference(date, delta):
    month, years = (date.month + delta) % 12, date.year + (date.month + delta - 1) // 12
    if not month:
        month = 12
    days = min(
        date.day,
        [
            31, 29 if years % 4 == 0 and not years % 400 == 0 else
            28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
        ][month - 1]
    )
    return date.replace(day=days, month=month, year=years)
