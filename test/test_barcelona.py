
import pprint
from opendata.spain import BarcelonaOpenData


def main():
    pp = pprint.PrettyPrinter()
    bapi = BarcelonaOpenData()

    # https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_search?rows=1
    result = bapi.data.api.3.action.package_search()
    print(result)


if __name__ == "__main__":
    main()
