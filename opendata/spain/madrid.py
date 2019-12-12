import requests
import json

from ..base import BaseOpenDataAPI


class MadridOpenData(BaseOpenDataAPI):
    ENDPOINT_API = "https://datos.madrid.es/egob/{url}"

    def __call__(self, fmt='json', *args, **kwargs):
        """Callable for the object
        """
        parametes = [f'{key}={value}' for key, value in kwargs.items()]
        url = "/".join(self._path) + f'.{fmt}' + '?' + "&".join(parametes)
        url = self.ENDPOINT_API.format(url=url)

        headers = {
            'Accept': 'application/json',
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/78.0.3904.97 Safari/537.36'),
        }

        response = requests.get(url, headers=headers, allow_redirects=True)

        if not response.ok:
            attribute = self._path[-1]
            message = (f"AttributeError: '{self.__class__.__name__}' object has no attribute "
                       f"'{attribute}' '{response.content}'")
            raise AttributeError(message)

        self._path = []
        return response.json()['result']['items']

    def get_by_date(self, begin, end, *args, **kwargs):
        # GET /catalogo/modified/begin/{beginDate}/end/{endDate}
        self._path = ['catalogo', 'modified', 'begin', begin, 'end', end]

        return self.__call__(*args, **kwargs)
