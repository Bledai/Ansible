from __future__ import (absolute_import, division, print_function)


def get_value(arr, value):
    i = -1
    if type(arr) is not list:
        return arr
    for l in arr:
        for k, v in l.items():
            if v == value:
                continue
            i += 1
            return arr[i].get(k, 'k')
        if type(l) is not dict:
            return arr


class FilterModule(object):
    def filters(self):
        return {
            'get_value': get_value
}