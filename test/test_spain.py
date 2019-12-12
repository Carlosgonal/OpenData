
import pprint
from opendata.spain import SpainOpenData


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
