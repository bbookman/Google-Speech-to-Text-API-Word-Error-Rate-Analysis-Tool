import logging
from utilities.utilities import Utilities

class GCS(object):

    def _parse_uri(self, uri):
        from urllib.parse import urlparse
        data = urlparse(uri)
        bucket = data.netloc
        folder = data.path[1:]
        f = folder.replace('/', '')

        return bucket, f

    def get_file_list(self, uri):
        logger = logging.getLogger(__name__)
        from google.cloud import storage as storage
        storage_client = storage.Client()
        results = []
        bucket, folder = self._parse_uri(uri)

        try:
            blobs = storage_client.list_blobs(bucket, prefix=folder) #  prefix=folder, delimiter='/'
        except StopIteration as s:
            print(s)
        except IOError as e:
            print(f'Can not get file list from {uri}: {e}')

        for blob in blobs:
            string = f'Blob name: {blob.name}'
            logger.debug(string)
            slash_loc = blob.name.rfind('/')
            results.append(blob.name[slash_loc+1:])
        return results

    def read_ref(self, uri, txt_file):
        from google.cloud import storage as storage

        client = storage.Client()
        bucket, folder = self._parse_uri(uri)
        b = client.bucket(bucket)
        path = f"{folder}/{txt_file}"
        blob = b.get_blob(path)
        #result = blob.download_as_string().decode('utf-8')
        result = blob.download_as_string().decode('latin-1')
        r = result.replace('\n', '')
        r = str(r)
        r = r.lower()
        utilities = Utilities()
        r = utilities.strip_puc(text = r)
        return r
