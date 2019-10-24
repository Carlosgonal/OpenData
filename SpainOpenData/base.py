
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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pp = pprint.PrettyPrinter()


class SpainOpenData():
    ENDPOINT_API = "https://datos.gob.es/apidata/{url}"

    def __init__(self, call_name=None, path=[], *args, **kwargs):

        self._path = path
        self._call_name = call_name

    def __getattr__(self, name):
        name = name.replace('_', '-')
        self._path.append(name)
        self._call_name = name

        return self

    def __call__(self, *args, **kwargs):
        """Callable for the object
        """
        parametes = [f'{key}={value}' for key, value in kwargs.items()]
        url = "/".join(self._path) + '?' + "&".join(parametes)
        url = self.ENDPOINT_API.format(url=url)

        response = requests.request("GET", url, verify=False)

        if not response.ok:
            attribute = self._path[-1]
            message = f"AttributeError: '{self.__class__.__name__}' object has no attribute '{attribute}'"
            raise AttributeError(message)

        self._path = []
        return response.json()['result']['items']



def main():
    pp = pprint.PrettyPrinter()
    spapi = SpainOpenData()

    result = spapi.catalog.dataset(_sort='title', _pageSize=1, _page=0)
    pp.pprint(result)
    result = spapi.catalog.dataset.l01281230_calidad_del_aire(_sort='title', _pageSize=10, _page=0)
    pp.pprint(result)
    # dataf = spapi.get_dataset(
    #     dataset_id="u03400001-estudiantes-matriculados-en-estudios-oficiales")

    # print(dataf)
    pp = pprint.PrettyPrinter()
    # pp.pprint(result)


if __name__ == "__main__":
    main()
