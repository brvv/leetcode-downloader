import datetime
import zoneinfo
import os

file_extensions = {'python' : '.py', 'python3' : '.py'}
timezone = "America/Toronto"


def get_submission_date(submission):
    dt = datetime.datetime.fromtimestamp(submission['timestamp'])
    return dt.replace(tzinfo=zoneinfo.ZoneInfo(key=timezone))


def _get_day_suffix(day):
    day = int(day)
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1] 

def generate_filename(title, date):
    day = date.strftime('%d')
    suffix = _get_day_suffix(day)

    date_string = day + suffix + date.strftime(', at %H %M')
    new_title = title.replace('-', ' ')
    return f'{date_string} - {new_title}'

def generate_path(date):
    year = date.strftime('%Y')
    month = date.strftime('%b')
    return os.path.join(year, month)

def generate_full_name(submission):
    date = get_submission_date(submission)
    filename = generate_filename(submission['title'], date)
    extension = file_extensions.get(submission['language'], '')

    path = generate_path(date)
    
    full_name = os.path.join(path, filename + extension)
    return full_name
