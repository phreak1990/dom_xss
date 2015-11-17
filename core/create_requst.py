__author__ = 'Phreak'
"""
I am addicted to the way I feel when I think of YoU.
I wish I could do EvrYthNG on Earth with YoU.
"""
# !/usr/bin/env python

import requests
from requests.exceptions import ConnectionError

class CreateRequest():
    def __init__(self):
        self.proxies = {
              "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080"
            }

####################################################################################
    def createRequestObject(self, method, url, headers, data, redirect_flag = True):
        s = requests.Session()

        try:
            request_object = requests.request(method=method, url=url, headers=headers, data=data, allow_redirects=redirect_flag,
                                          verify=False, timeout=7)#, proxies = self.proxies)


        except ConnectionError:
            print "Connection Error in URL :--->{0}".format(url)
            return None

        return request_object

####################################################################################
