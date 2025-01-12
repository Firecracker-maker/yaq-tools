from datetime import date, datetime
from typing import Union

import pytz


def datetime_to_str(dt: Union[str, datetime, date]):
    """
    Function to convert python datetime object to str
    Parameters
    ----------
    dt: datetime object

    Returns
    -------

    """
    if isinstance(dt, (datetime, date)):
        return dt.strftime("%Y-%m-%d")


def to_utc_datetime(
    dt: Union[str, datetime, date], exp_fmt: str = "%Y%m%d %H:%M:%S %z"
):
    """
    Transform date to include timezone
    Parameters
    ----------
    dt: date to transform
    exp_fmt: expected format

    Returns
    -------

    """

    if isinstance(dt, str):
        dt = datetime.strptime(dt, exp_fmt)

    if isinstance(dt, (date, datetime)):
        dt.replace(tzinfo=pytz.UTC)

    return dt
