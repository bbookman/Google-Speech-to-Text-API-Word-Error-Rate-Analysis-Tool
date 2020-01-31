class GCS(object):
    uri = str()

    def get_uri(self):
        return self.uri

    def set_uri(self, uri):
        self.uri = uri

    def _parse_uri(self, uri):
        from urllib.parse import urlparse
        data = urlparse(uri)
        bucket = data.netloc
        folder = data.path[1:]
        return bucket, folder

    def get_file_list(self, uri):
        from google.cloud import storage as storage
        storage_client = storage.Client()
        results = []
        bucket, folder = self._parse_uri(uri)

        blobs = storage_client.list_blobs(bucket, max_results=100000, prefix=folder)

        for blob in blobs:
            slash_loc = blob.name.rfind('/')
            results.append(blob.name[:slash_loc])
            import pdb; pdb.set_trace()
        return results