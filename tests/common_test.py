#!/usr/bin/env python
# encoding: utf-8

"""A test module"""

import datetime
import tempfile
import os
import shutil

import scores.common as common


class TestCommon(object):
    """ A Test class"""

    def test_date_function(self):
        """Test"""
        a_date = datetime.datetime.now()
        a_date = a_date.replace(microsecond=0)
        tstamp = common.datetime_to_timestamp(a_date)
        assert tstamp > 0
        converted_bck = common.timestamp_to_datetime(tstamp)
        assert converted_bck == a_date
