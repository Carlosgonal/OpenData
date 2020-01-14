
import requests
from ..base import BaseOpenDataAPI

import rdflib

import json


class EuropeOpenData(BaseOpenDataAPI):
    # https://www.europeandataportal.eu/data/search/search?q=&filter=dataset&page=10&
    ENDPOINT_API = "https://www.europeandataportal.eu/data/search/{url}"

    def clean_results(self, json_dict):
        return json_dict['result']

    def get_dataset(self, dataset_id):
        url = self.ENDPOINT_API.format(url=f"apiodp/action/package_show")
        response = requests.request("POST", url, json={'id': dataset_id}, verify=False)

        if not response.ok:
            message = (f"Error in request ")
            raise AttributeError(message)

        data = self.clean_results(response.json())
        del data['rdf']

        return data
