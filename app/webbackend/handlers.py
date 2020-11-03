from datetime import datetime, timedelta

from app import db
from app.models import Sale
from dateutil.relativedelta import relativedelta


def errors_convert_dict_to_string(dict_errors: dict):
    for key in dict_errors:
        key = str(key)
        errors = ",".join(dict_errors.get(key))
        return f"{key}: {errors}."


def filter_for_table_between_date(
    base, startdate: datetime, finishdate: datetime, client_id=None
):
    finishdate = finishdate + timedelta(days=1)
    if client_id:
        information_for_table = (
            db.session.query(base)
            .filter(Sale.client_id == client_id)
            .order_by(base.date.desc())
            .filter(base.date >= startdate)
            .filter(base.date < finishdate)
            .all()
        )
        return information_for_table
    information_for_table = (
        db.session.query(base)
        .order_by(base.date.desc())
        .filter(base.date >= startdate)
        .filter(base.date < finishdate)
        .all()
    )

    return information_for_table
