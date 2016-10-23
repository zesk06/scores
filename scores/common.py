#!/usr/bin/env python
# encoding: utf-8

import hashlib


def hash_password(passwd):
    """hash the password
    similar to how MySQL hashes passwords with the password() function.
    :rtype: str
    """
    hpasswd = hashlib.sha1(passwd.encode('utf-8')).digest()
    hpasswd = hashlib.sha1(hpasswd).hexdigest()
    hpasswd = '*' + hpasswd.upper()
    return hpasswd
