#!/usr/bin/env python
# encoding: utf-8

"""
Common functions
"""

import datetime
import hashlib
import logging
import time


def hash_password(passwd):
    """hash the password
    similar to how MySQL hashes passwords with the password() function.
    :rtype: str
    """
    hpasswd = hashlib.sha1(passwd.encode('utf-8')).digest()
    hpasswd = hashlib.sha1(hpasswd).hexdigest()
    hpasswd = '*' + hpasswd.upper()
    return hpasswd


def datetime_to_timestamp(a_date):
    """Transform a datetime.datetime to a timestamp
    microseconds are lost !
    :type a_date: datetime.datetime
    :rtype: float
    """
    return time.mktime(a_date.timetuple())


def timestamp_to_datetime(tstamp):
    """Convert a timestamp to a datetime
    :type tstamp: float
    :rtype: datetime.datetime"""
    return datetime.datetime.fromtimestamp(tstamp)


if __name__ == '__main__':
    logging.basicConfig()
