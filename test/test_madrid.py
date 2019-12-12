
import pprint
from opendata.spain import MadridOpenData


def main():
    pp = pprint.PrettyPrinter()
    mapi = MadridOpenData()

    # GET /catalogo/format/{format}.{fmt}
    # https://datos.madrid.es/egob/catalogo/format/csv.csv
    result = mapi.catalogo.format.json()
    print(result)
   

if __name__ == "__main__":
    main()