
import json
import os
import pprint
import shutil
import time
import urllib
import urllib.request

import pandas as pd
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pp = pprint.PrettyPrinter()


class BaseOpenDataAPI():
    ENDPOINT_API = ""

    NUMBERS = {
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine'
    }

    def __init__(self, *args, **kwargs):

        self._path = []
        self._call_name = ''

    def __getattr__(self, name):
        name = name.replace('__', '-')
        self._path.append(name)
        self._call_name = name

        return self

    def __call__(self, body={}, *args, **kwargs):
        """Callable for the object
        """
        parametes = [f'{key}={value}' for key, value in kwargs.items()]
        url = "/".join(self._path)
        if parametes:
            url += '?' + "&".join(parametes)
        url = self.ENDPOINT_API.format(url=url)

        response = requests.request("GET", url, json=body, verify=False)

        if not response.ok:
            attribute = self._path[-1]
            message = (f"AttributeError: '{self.__class__.__name__}' object has no attribute "
                       f"'{attribute}'")
            raise AttributeError(message)

        self._path = []
        return self.clean_results(response.json())

    def clean_results(self, json_dict):
        return json_dict['result']['items']
