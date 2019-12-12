import requests
from ..base import BaseOpenDataAPI


class SpainOpenData(BaseOpenDataAPI):
    ENDPOINT_API = "https://datos.gob.es/apidata/{url}"

    def __call__(self, *args, **kwargs):
        """Callable for the object
        """
        parametes = [f'{key}={value}' for key, value in kwargs.items()]
        url = "/".join(self._path) + '?' + "&".join(parametes)
        url = self.ENDPOINT_API.format(url=url)

        response = requests.request("GET", url, verify=False)

        if not response.ok:
            attribute = self._path[-1]
            message = (f"AttributeError: '{self.__class__.__name__}' object has no attribute "
                       f"'{attribute}'")
            raise AttributeError(message)

        self._path = []
        return response.json()['result']['items']
