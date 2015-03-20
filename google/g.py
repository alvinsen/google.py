# coding=utf8

"""
    g
    ~

    Search available fast google ip for blocked users.
"""

import os
import sys
import json
import logging
import urllib
import webbrowser

import requests
import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all(thread=False, select=False)
from gevent.event import AsyncResult


class G(object):

    def __init__(self, pool_size=300, timeout=1):
        self.pool_size = pool_size
        self.timeout = timeout

        logging.basicConfig(format='%(message)s')
        self.logger = logging.getLogger(name='g')
        self.logger.setLevel(logging.INFO)

        self.pool = Pool(self.pool_size)
        self.async_result = AsyncResult()

    def url(self, ip, params=None):
        if params:
            suffix = '/search?q=%s' % urllib.quote_plus(' '.join(params))
        else:
            suffix = ''
        return 'http://%s%s' % (ip, suffix)

    def worker(self, ip):
        if not self.async_result.ready():
            try:
                resp = requests.head(self.url(ip), timeout=self.timeout)
            except requests.exceptions.RequestException:
                pass  # ignore timeouts, connection errors
            else:
                if resp.status_code == requests.codes.ok:
                    if not self.async_result.ready():
                        self.async_result.set(ip)

    def run(self):
        # read and parse ip json file
        gdir = os.path.dirname(__file__)
        path = os.path.join(gdir, 'ips.json')
        ips = json.load(open(path))
        # start a thread for pool
        gevent.spawn(self.pool.map, self.worker, ips)
        # block main thread for the 1st available IP
        try:
            ip = self.async_result.get(timeout=5)
        except gevent.timeout.Timeout:
            self.logger.info('Timeout (5s).')
        else:
            self.pool.kill()
            self.logger.info(ip)
            webbrowser.open(self.url(ip, params=sys.argv[1:]))


def main():
    g = G()
    g.run()


if __name__ == '__main__':
    main()
