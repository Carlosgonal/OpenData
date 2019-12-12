
import re
import ssl
from ftplib import FTP
from os.path import basename
from urllib.parse import parse_qs, urlparse

import requests
import unipath
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry


class DownloadDataset:

    PATH = unipath.Path("SpainOpenData/data")
    RETRIES = 3
    BACKOFF_FACTOR = 0.3
    STATUS_FORCELIST = (500, 502, 504)

    UNKNOWN = 'unknown'
    CIS = 'cis'
    DEFAULT = 'default'

    def __init__(self):
        self.session = requests.Session()
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

    def is_downloadable(self, url=None, type_download=None):
        """Check if url or type if downloadable

        Keyword Arguments:
            url {str} -- url to check (default: {None})
            type_download {str} -- type of download (default: {None})

        Raises:
            AttributeError: In case teh method dont take parameters

        Returns:
            bool -- True in case of downloadable else False
        """
        if url:
            type_download = self.get_type_download(url)
        elif not type_download:
            raise AttributeError

        downloable = [self.CIS, self.DEFAULT]

        if type_download in downloable:
            return True
        return False

    def get_type_download(self, url):
        """Get type of download

        Arguments:
            url {url} -- url from server with data

        Returns:
            str -- Type of download
        """
        if 'www.cis.es' in url:
            return self.CIS

        head = self.request('HEAD', url, allow_redirects=True)

        if head:
            content_type = head.headers.get('content-type')
            if content_type and 'html' in content_type.lower():
                return self.UNKNOWN
            return self.DEFAULT

        return self.UNKNOWN

    @staticmethod
    def get_filename(response):
        """Get download file name

        Arguments:
            response {Request response} -- requests response

        Returns:
            str -- file name
        """

        if 'content-disposition' in response.headers:
            head = response.headers['content-disposition']
            filename = re.findall(r'filename="(.+)"', head)[0]
        elif 'Location' in response.headers:
            head = response.headers['content-disposition']
            filename = re.findall(r'.+/(.+).zip', head)[0]
        else:
            filename = basename(response.url)
            filename = re.findall(r'^([^\?]+)(\?.*)?', filename)[0][0]

        return filename

    def download(self, url):
        type_download = self.get_type_download(url)

        if self.is_downloadable(type_download=type_download):
            if type_download == self.CIS:
                self.downlaod_cis(url)
            elif type_download == self.DEFAULT:
                self.download_default(url)
            else:
                print("Unknow file to download")
        else:
            print("NOT downloadable")

    def download_default(self, url):
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

    def downlaod_cis(self, url):
        """Download file from cis

        Arguments:
            url {str} -- url strinf

        Returns:
            str -- file name path
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        elements = soup.findAll("a", {"id": "fdatosoculto"})

        if elements:
            for element in elements:
                parsed = urlparse(element['href'])
                dwld = parse_qs(parsed.query)['dwld']

                params = {
                    'dwld': dwld,
                    'Nombre': '',
                    'Apellidos': '',
                    'profesion': '',
                    'Email': 'example@example.es',
                    'objetonombre0': 'Investigación/informe/libro',
                    'objetonombre1': 'Tesis/tesina/máster',
                    'objetonombre2': 'Proyectos/planes/campañas',
                    'objetonombre3': 'Trabajo de curso',
                    'objetonombre4': 'Medios de comunicación',
                    'objetonombre5': 'Conferencias/ponencias',
                    'objetonombre6': 'Docencia',
                    'objetonombre7': 'Otros',
                    'objetotxt': '',
                    'Terminos': 'on',
                    'descarga': 'Descargar'
                }

                response = self.request(
                    'GET', url, params=params, allow_redirects=False)
                ftp_conf = response.headers['Location']

                local_file = self.download_ftp(ftp_conf)

                return local_file
        else:
            print("Not dataset in to download in cis")
            return None

    def download_ftp(self, url):
        """Download file from FTP server

        Arguments:
            url {str} -- ftp server url ftp://{user}:{pass}@{server}/{path}/{file}

        Returns:
            str -- local file location
        """

        filename = re.search(r'.+\/(.+)', url).group(1)
        ftp_url = re.search(r'.+@(.+)\/.+\/.+', url).group(1)
        ftp_user = re.search(r'\/\/(.+)\:.+', url).group(1)
        ftp_pass = re.search(r'.+[:](.+)@.+', url).group(1)
        ftp_path = re.search(r'.+\/(.+)\/.+', url).group(1)

        local_filename = self.PATH.child(filename)

        ftp = FTP(ftp_url)
        ftp.login(ftp_user, ftp_pass)
        ftp.cwd(ftp_path)

        with open(local_filename, 'wb') as file:
            ftp.retrbinary('RETR ' + filename, file.write, 1024)

        ftp.close()

        return local_filename

    def request(self, method, url, **kwargs):
        """Method to catch request exception

        Arguments:
            method {str} -- type of request GET, POST, ...
            url {str} -- url

        Returns:
            Request.response -- response of request
        """
        try:
            response = self.session.request(method, url, **kwargs)

            return response

        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        except ssl.SSLError as err:
            print('SSL connection failed: ', err)
        except Exception as err:
            print('Unknown Error', err)
