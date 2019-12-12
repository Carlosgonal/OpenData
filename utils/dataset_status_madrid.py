
import pandas as pd
from opendata.spain import MadridOpenData
from opendata.download import DownloadDataset

DOWNLOADABLE = 1
NOTDOWNLOADABLE = 0


def get_info_datasets(function, params, filename):
    downdata = DownloadDataset()

    data = []
    num_data = 0
    page = 0
    while True:
        datasets = function(**params, _sort='title', _pageSize=100, _page=page)
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
                'page': page,
                'id': i,
                'title': dataset['title'],
                'url': url,
                'keyword': dataset.get('keyword', ''),
                'status': status,
                'type_download': type_download,
            }
            data.append(row)
            print(f"Page: {page} {i+1}/100", flush=True)

        page += 1
        if num_data == len(data):
            return
        else:
            num_data = len(data)

        print()
        print('*'*100)
        print(f"Downloaded info from {len(data)} datasets ")
        dataf = pd.DataFrame(data)
        dataf.to_csv(filename)
        print('*'*100)


def main():
    mapi = MadridOpenData()
    downdata = DownloadDataset()

    params = {'begin': "1000-01-01T00:00Z", 'end': "3000-01-01T00:00Z"}
    get_info_datasets(mapi.catalogo.modified.get_by_date,
                      params, "datasets_madrid.csv")


if __name__ == "__main__":
    main()
