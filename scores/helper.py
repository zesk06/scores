# coding=utf-8

import functools


def required_fields(fields):
    """This decorator permits to check that there are some fields in the
    data keyword parameter, or in the second argument if no keyword is found.
    In order to prevent keyerror.

    ex:
        @required_fields(['toto', tutu'])
        def some_function(self, data):
            data['toto'] = 'shall not fail';
    """
    def required_fields(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if 'data' in kwargs:
                data = kwargs['data']
            else:
                data = args[1]
            for field in fields:
                if field not in data:
                    raise KeyError('Missing field %s in %s' %
                                   (field, func.__name__))
            return func(*args, **kwargs)

        return wrapper
    return required_fields
