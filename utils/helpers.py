# utils/helpers.py
from datetime import datetime, timedelta

def get_yesterday_date():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%d-%b-%Y')
