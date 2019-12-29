
import pandas as pd
import hashlib
from opendata.spain import SpainOpenData
from opendata.download import DownloadDataset
from opendata.elastic import Elastic

DOWNLOADABLE = 1
NOTDOWNLOADABLE = 0


def main():
    spapi = SpainOpenData()
    downdata = DownloadDataset()

    data = []

    for page in range(0, 1000):
        datasets = spapi.catalog.dataset(
            _sort='title', _pageSize=100, _page=page)
        for i, dataset in enumerate(datasets):
            if isinstance(dataset, list):
                dataset = dataset[0]

            distribution = dataset.get('distribution', {})
            if isinstance(distribution, list):
                distribution = distribution[0]

            url = distribution.get('accessURL', '')
            type_download = downdata.get_type_download(url)
            if downdata.is_downloadable(type_download=type_download):
                status = DOWNLOADABLE
            else:
                status = NOTDOWNLOADABLE

            row = {
                'issued': dataset['issued'],
                'page': page,
                'id': i,
                'title': dataset['title'],
                'url': url,
                'keyword': dataset.get('keyword', ''),
                'theme': dataset.get('theme', ''),
                'status': status,
                'type_download': type_download,
            }
            data.append(row)
            print(f"Page: {page} {i+1}/100", flush=True)

        print()
        print('*'*100)
        print(f"Downloaded info from {len(data)} datasets ")
        dataf = pd.DataFrame(data)
        dataf.to_csv("datasets.csv")
        print('*'*100)


def main2():
    spapi = SpainOpenData()
    elastic = Elastic()

    for page in range(0, 1000):
        datasets = spapi.catalog.dataset(
            _sort='title', _pageSize=100, _page=page)
        for i, dataset in enumerate(datasets):
            if isinstance(dataset, list):
                dataset = dataset[0]

            distribution = dataset.get('distribution', {})
            if isinstance(distribution, list):
                distribution = distribution[0]

            url = distribution.get('accessURL', '')
            id_doc = hashlib.md5(url.encode('utf-8'))
            elastic.save_document('open_spain', dataset, id_doc.hexdigest())

            print(f"Page: {page} {i+1}/100", flush=True)


if __name__ == "__main__":
    main2()
