
import pprint
from opendata.france import FranceOpenData


def main():
    pp = pprint.PrettyPrinter()
    frapi = FranceOpenData()

    # https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_search?rows=1
    result = frapi.datasets(page_size=1)
    print(result)
   

if __name__ == "__main__":
    main()