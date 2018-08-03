# ！usr/bin/env python

__author__ = 'Camille'

import time
import threading
import requests


def exe_time(fun):
    def wrapper(*args, **kwargs):
        t = time.time()
        data = fun(*args, **kwargs)
        print(time.time() - t)

        return data

    return wrapper


@exe_time
def test():
    requests.get('url')


data = 3

if __name__ == '__main__':
    for i in range(data):
        t = threading.Thread(target=test)
        t.start()
