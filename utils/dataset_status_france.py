
import pandas as pd
from opendata.france import FranceOpenData
from opendata.download import DownloadDataset
from opendata.elastic import Elastic

DOWNLOADABLE = 1
NOTDOWNLOADABLE = 0


def main():
    frapi = FranceOpenData()
    downdata = DownloadDataset()

    data = []

    for page in range(0, 1000):
        datasets = frapi.datasets(sort='title', pageSize=100, page=page)
        for i, dataset in enumerate(datasets):

            row = {
                'id': dataset['id'],
                'page': page,
                'id': i,
                'head_title': dataset['title'],
                'title': None,
                'url': None,
                'keyword': dataset.get('tags', ''),
                "format": None,
                'status': None,
                'type_download': None,
            }

            for resource in dataset['resources']:
                url = resource.get('url', '')

                type_download = downdata.get_type_download(url)
                if downdata.is_downloadable(type_download=type_download):
                    status = DOWNLOADABLE
                else:
                    status = NOTDOWNLOADABLE

                row['url'] = url
                row['format'] = resource.get('format', '')
                row['title'] = resource.get('title', '')
                row['status'] = status
                row['type_download'] = type_download

                data.append(row)

            print(f"Page: {page} {i+1}/100", flush=True)

        print()
        print('*'*100)
        print(f"Downloaded info from {len(data)} datasets ")
        dataf = pd.DataFrame(data)
        dataf.to_csv("datasets_france.csv")
        print('*'*100)


def main2():
    frapi = FranceOpenData()
    elastic = Elastic()

    for page in range(0, 1000):
        datasets = frapi.datasets(sort='title', pageSize=100, page=page)
        for i, dataset in enumerate(datasets):
            elastic.save_document('open_france', dataset, dataset['id'])

            print(f"Page: {page} {i+1}/100", flush=True)


if __name__ == "__main__":
    main2()
