import requests
from ..base import BaseOpenDataAPI


class SpainOpenData(BaseOpenDataAPI):
    ENDPOINT_API = "https://datos.gob.es/apidata/{url}"

    def clean_results(self, json_dict):
        return json_dict['result']['items']
