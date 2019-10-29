
import pandas as pd
from spainopendata import SpainOpenData
from spainopendata import DownloadDataset


DOWNLOADABLE = 1
NOTDOWNLOADABLE = 0

def main():
    spapi = SpainOpenData()
    downdata = DownloadDataset()

    data = []

    for page in range(0, 1000):
        datasets = spapi.catalog.dataset(_sort='title', _pageSize=100, _page=page)
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

        print()
        print('*'*100)
        print(f"Downloaded info from {len(data)} datasets ")
        dataf = pd.DataFrame(data)
        dataf.to_csv("datasets.csv")
        print('*'*100)

if __name__ == "__main__":
    main()