from datetime import datetime


def format_timestamp(timestamp):
    date = datetime.fromtimestamp(timestamp)

    if date.date() == datetime.today().date():
        return date.strftime("%H:%M:%S")
    else:
        return date.strftime("%d/%m/%Y")
