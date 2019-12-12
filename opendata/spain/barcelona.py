import requests
import json

from ..base import BaseOpenDataAPI


class BarcelonaOpenData(BaseOpenDataAPI):
    ENDPOINT_API = "https://opendata-ajuntament.barcelona.cat/{url}"

    def clean_results(self, json_dict):
        return json_dict['result']['items']
