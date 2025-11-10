import pandas as pd
import re
def pandas_show_all():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)


def split_courts(s):
    """
       Split a booking string into court-specific entries.
    """
    matches = re.findall(r"(Court \d+[^C]*)", s)
    courts = {}
    for m in matches:
        num = re.search(r"Court (\d+)", m).group(1)
        value = re.sub(r"Court \d+", "", m).strip()
        courts[f"Court {num}"] = value
    return courts