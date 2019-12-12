import requests
from ..base import BaseOpenDataAPI


class FranceOpenData(BaseOpenDataAPI):
    # https://www.data.gouv.fr/es/apidoc/
    ENDPOINT_API = "https://www.data.gouv.fr/api/1/{url}"

    def clean_results(self, json_dict):
        return json_dict['data']

