import requests
import typing
import logging

logger = logging.getLogger()

class YandexClient():

    def __init__(self, public_key, secret_key):


        self._base_url = "https://cloud-api.yandex.net"

        self._public_key = public_key
        self._secret_key = secret_key

        self.authentication = "test"
        self._headers = {'Authorization': 'OAuth {}'.format(self.authentication)}


    def _make_request(self, method: str, endpoint: str, data: typing.Dict):

        if method == "GET":
            try:
                r = requests.get(self._base_url + endpoint, params=data, headers= self._headers)
            except Exception as e:  # Takes into account any possible error, most likely network errors
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "POST":
            try:
                r = requests.post(self._base_url + endpoint, params=data, headers= self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "DELETE":
            try:
                r = requests.delete(self._base_url + endpoint, params=data, headers= self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None
        else:
            raise ValueError()

        if r.status_code == 200:  # 200 is the response code of successful requests
            return r.json()
        else:
            logger.error("Error while making %s request to %s: %s (error code %s)",
                         method, endpoint, r.json(), r.status_code)
            return None


    def get_authentication(self):
        pass

    def get_disk_information(self):
        """
        https://yandex.com/dev/disk/api/reference/capacity.html


        :return:
        """


        info = self._make_request("GET", "/v1/disk", dict())

        return info

    def get_meta_information(self, path, fields= None, limit= None, offset= None, preview_crop= None, preview_size= None, sort= None):
        data = {
            "path": path,
            "fields": fields,
            "limit": limit,
            "offset": offset,
            "preview_crop": preview_crop,
            "preview_size": preview_size,
            "sort": sort
        }


        meta_info = self._make_request("GET", "/v1/disk/resources", data)

        return meta_info

    def get_list_of_files(self, limit= None, media_type= None, offset= None, fields= None, preview_size= None, preview_crop = None):

        data = {
            "limit": limit,
            "media_type": media_type,
            "offset": offset,
            "fields": fields,
            "preview_size": preview_size,
            "preview_crop": preview_crop,
        }

        list_of_files = self._make_request("GET", "/v1/disk/resources/files", data)

        return list_of_files


    def get_latest_uploaded_files(self, limit= None, media_type= None, fields= None, preview_size= None, preview_crop = None):

        data = {
            "limit": limit,
            "media_type": media_type,
            "fields": fields,
            "preview_size": preview_size,
            "preview_crop": preview_crop,
        }

        latest_uploaded_files = self._make_request("GET", "/v1/disk/resources/last-uploaded", data)

        return latest_uploaded_files

    # kontrol et
    def upload_file_to_yandex(self, path, overwrite= False, fields= None):

        data = {
            "path": path,
            "overwrite": overwrite,
            "fields": fields
        }


        self._make_request("GET", "/v1/disk/resources/upload", data)



    def download_file_from_yandex(self, path, fields= None):

        data = {
            "path": path,
            "fields": fields
        }


        url_response = self._make_request("GET", "/v1/disk/resources/download", data)

        if url_response is not None:
            url = url_response['href']

            return requests.get(url)



