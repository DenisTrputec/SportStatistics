import re
from datetime import datetime


def __is_date(string):
    try:
        datetime.strptime(string, '%d %B %Y')
        return True
    except ValueError:
        return False


def __values_to_check(match, keys):
    values = []
    for key, value in match.items():
        if key not in keys:
            values.append(value)
    return values


def read_wiki_match(filepath="wiki.txt", ignore_keys=None):
    matches = []
    match = {
        "date": None,
        "home_team_name": None,
        "away_team_name": None,
        "home_goals": None,
        "away_goals": None,
        "stadium": None,
        "attendance": None,
        "referee": None
    }
    ignore_keys = ignore_keys if ignore_keys else []

    with open(filepath, encoding="utf8") as handle:
        lines = handle.readlines()
        for line in lines:
            line = re.sub(r"\[.*\]", "", line[:-1])
            result = re.search(r"\d+\s*–\s*\d+", line)

            if __is_date(line):
                match["date"] = line.replace("\xa0", " ")
            elif result:
                t = re.split(r"\d+\s*–\s*\d+", line)
                match["home_team_name"] = t[0].replace("\xa0", "").strip()
                match["away_team_name"] = t[1].replace("\xa0", "").strip()
                r = result.group(0).split('–')
                match["home_goals"] = int(r[0])
                match["away_goals"] = int(r[1])
            elif not re.search(r"\d", line) and re.search(r", ", line):
                match["stadium"] = line
            elif line.startswith("Attendance:"):
                match["attendance"] = int(line.split(": ")[1].replace(",", ""))
            elif line.startswith("Referee:"):
                match["referee"] = line.split(": ")[1]

            for value in __values_to_check(match, ignore_keys):
                if value is None:
                    break
            else:
                print(match)
                matches.append(match)
                match = dict.fromkeys(match, None)

    return matches
