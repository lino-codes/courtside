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

def time_to_int(time_str):
    time_str = time_str.lower().strip()
    if 'am' in time_str:
        hour = int(time_str.replace('am', '').strip())
        return 0 if hour == 12 else hour
    elif 'pm' in time_str:
        hour = int(time_str.replace('pm', '').strip())
        return 12 if hour == 12 else hour + 12
    return None


def format_time_ampm(time_val):
    # Accepts float or string, converts to "h:mm AM/PM"
    if isinstance(time_val, float):
        hour = int(time_val)
        minute = int((time_val - hour) * 60)
    else:
        time_val = float(time_val)
        hour = int(time_val)
        minute = int((time_val - hour) * 60)
    from datetime import time
    dt = time(hour, minute)
    return dt.strftime("%I:%M %p").lstrip('0')