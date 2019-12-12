import requests
import json

from ..base import BaseOpenDataAPI


class MadridOpenData(BaseOpenDataAPI):
    ENDPOINT_API = "https://datos.madrid.es/egob/{url}"

    def get_by_date(self, begin, end, *args, **kwargs):
        # GET /catalogo/modified/begin/{beginDate}/end/{endDate}
        self._path = ['catalogo', 'modified', 'begin', begin, 'end', end]

        return self.__call__(*args, **kwargs)

    def clean_results(self, json_dict):
        return json_dict['result']['items']
