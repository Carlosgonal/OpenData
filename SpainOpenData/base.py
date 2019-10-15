
import json

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SpainOpenData():
    ENDPOINT = "https://datos.gob.es/apidata/"

    def __init__(self, call_name=None, path=[], *args, **kwargs):

        self._path = path
        self._call_name = call_name

    def __getattr__(self, name):
        name = name.replace('_', '-')
        self._path.append(name)
        print(self._path)

        return SpainOpenData(
            call_name=name,
            path=self._path
        )

    def __call__(self, *args, **kwargs):
        """Callable for the object
        """

        parametes = [f'{key}={value}' for key, value in kwargs.items()]
        url = "/".join(self._path) + '?' + "&".join(parametes)
        url = self.ENDPOINT + url

        print(
            f"Wrapping: {self._path} Args: '{args}'. Kwargs: '{kwargs}' \n {url}"
        )

        self._path = []
        print(self, self._path)
        try:
            response = requests.request("GET", url, verify=False)
            return response.json()

        except Exception as error:
            print("error")
            print(error)
            return None


def main():
    spapi = SpainOpenData()

    result = spapi.catalog.dataset(_sort='title', _pageSize=10, _page=0)
    print(spapi._path)
    result = spapi.catalog.dataset.l01281230_calidad_del_aire()


if __name__ == "__main__":
    main()
