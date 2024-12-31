from datetime import datetime


def pretty_date_time(date_time):
    """Print the date in friendly format
    Adapted from: http://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python

    Args:
        date_time (_type_): The date

    Returns:
       str: A friendly format date
    """

    now = datetime.now()

    if isinstance(date_time, int):
        diff = now - datetime.fromtimestamp(date_time)
    elif isinstance(date_time, datetime):
        diff = now - date_time
    elif not date_time:
        diff = now - now

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""
    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "1 minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "1 hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " week(s) ago"
    if day_diff < 365:
        return str(day_diff // 30) + " month(s) ago"
    return str(day_diff // 365) + " year(s) ago"
