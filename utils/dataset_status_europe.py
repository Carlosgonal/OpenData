
from urllib.parse import urlparse

from opendata.europe import EuropeOpenData
from opendata.elastic import Elastic


def clean_key(key):
    if '@' in key:
        new_key = key.replace('@', '')
    else:
        key_parse = urlparse(key)
        new_key = key_parse.path.replace('/','_')

    return new_key


if __name__ == "__main__":

    euopen = EuropeOpenData()
    elastic = Elastic()

    page = 0
    data_recovered = 0
    while True:
        datasets = euopen.search(q='', filter='dataset', page=page, limit=200)
        results = datasets['results']

        if not results:
            print(f"Data recovered: {data_recovered}")
            break

        for i, dataset in enumerate(results):
            print(f"Page {page} : {i}/{len(results)}")
            elastic.save_document('open_europe', dataset, dataset['id'])
            data_recovered += 1

        page += 1
        print("-"*100)
