import re

def parse_time(time_str):
    # Strip whitespace and ensure lowercase for matching
    time_str = time_str.strip().lower()
    match = re.match(r"(\d{1,2}):(\d{2})(am|pm)", time_str)
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2))
    meridiem = match.group(3)
    if meridiem == 'pm' and hour != 12:
        hour += 12
    elif meridiem == 'am' and hour == 12:
        hour = 0
    return hour + minute / 60.0