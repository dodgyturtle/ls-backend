from datetime import datetime, timedelta

from app import db
from dateutil.relativedelta import relativedelta


def errors_convert_dict_to_string(dict_errors: dict):
    for key in dict_errors:
        return(str(key) + ','.join(dict_errors.get(key)))


def filter_for_table(base, period: str):
    datetime_period = {
        'day': (datetime(datetime.today().year, datetime.today().month, datetime.today().day)),
        'week': (datetime.today() - timedelta(days = 7)),
        'month': (datetime.today() - relativedelta(months=1)),
    }
    information_for_table = db.session.query(base).order_by(base.date.desc()).filter(base.date >= datetime_period.get(period, datetime.today())).all()
    
    return information_for_table
