import os
import re
import time
import ssl
from os.path import basename
from urllib.request import urlopen

import requests
import unipath
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm


class DownloadDataset:

    PATH = unipath.Path("SpainOpenData/data")
    RETRIES = 3,
    BACKOFF_FACTOR = 0.3,
    STATUS_FORCELIST = (500, 502, 504),

    def __init__(self):
        self.session =  requests.Session()
        retry = Retry(
            total=self.RETRIES,
            read=self.RETRIES,
            connect=self.RETRIES,
            backoff_factor=self.BACKOFF_FACTOR,
            status_forcelist=self.STATUS_FORCELIST,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)


    def is_downloadable(self, url):
        """ Does the url contain a downloadable resource

        Arguments:
            url {str} -- url string

        Returns:
            bool -- True if url has a downloadable file else False
        """

        head = self.request('HEAD', url, allow_redirects=True)
        if head:
            content_type = head.headers.get('content-type')
            if content_type and 'html' in content_type.lower():
                return False
            return True
        else:
            return False

    @staticmethod
    def get_filename(response):
        """Get download file name

        Arguments:
            response {Request response} -- requests response

        Returns:
            str -- file name
        """

        if 'content-disposition' in response.headers:
            d = response.headers['content-disposition']
            filename = re.findall(r'filename="(.+)"', d)[0]
        else:
            filename = basename(response.url)
            filename = re.findall(r'^([^\?]+)(\?.*)?', filename)[0][0]

        return filename


    def download(self, url):
        """Download file from url

        Arguments:
            url {str} -- url strinf

        Returns:
            str -- file name path
        """
        response = self.request('GET', url, stream=True)
        local_filename = self.PATH.child(self.get_filename(response))

        # Total size in bytes.
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        with open(local_filename, 'wb') as file:
            with tqdm(total=total_size, unit='iB', unit_scale=True) as process_bar:
                for data in response.iter_content(block_size):
                    process_bar.update(len(data))
                    file.write(data)

        return local_filename

    def request(self, method, url, **kwargs):
        try:
            response = self.session.request(method, url, **kwargs)
            
            return response
        
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)     
        except ssl.SSLError as err:
            print('SSL connection failed: ', err)
        except Exception as err:
            print('Unknown Error', err)
