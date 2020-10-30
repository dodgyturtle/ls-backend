from datetime import datetime, timedelta

from app import db
from dateutil.relativedelta import relativedelta


def errors_convert_dict_to_string(dict_errors: dict):
    for key in dict_errors:
        key = str(key)
        errors = ','.join(dict_errors.get(key))
        return(f'{key}: {errors}.')


def filter_for_table_between_date(base, startdate, finishdate):
    finishdate = finishdate + timedelta(days=1)
    information_for_table = db.session.query(base).order_by(
        base.date.desc()).filter(
        base.date >= startdate).filter(
        base.date < finishdate).all()

    return information_for_table
