import time

import requests
import typing
import logging

logger = logging.getLogger()


class YandexClient():

    def __init__(self, public_key, secret_key):

        self._base_url = "https://cloud-api.yandex.net"

        self._public_key = public_key
        self._secret_key = secret_key

        self.authentication = ""
        self._headers = {'Authorization': 'OAuth {}'.format(self.authentication)}

    def _make_request(self, method: str, endpoint: str, data: typing.Dict, absolute_url= False):

        if method == "GET":
            try:
                if absolute_url:
                    r = requests.get(endpoint, params=data, headers=self._headers)

                else:
                    r = requests.get(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:  # Takes into account any possible error, most likely network errors
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "POST":
            try:
                if absolute_url:
                    r = requests.post(endpoint, params=data, headers=self._headers)

                else:
                    r = requests.post(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "DELETE":
            try:
                if absolute_url:
                    r = requests.delete(endpoint, params=data, headers=self._headers)

                else:
                    r = requests.delete(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "PUT":
            try:
                if absolute_url:
                    r = requests.put(endpoint, params=data, headers=self._headers)

                else:
                    r = requests.put(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        else:
            raise ValueError()


        if r.status_code == 200:  # OK, 200 is the response code of successful requests
            return r.json()

        elif r.status_code == 201:  # Created,  The request succeeded, and a new resource was created as a result.
            return r.json()

        elif r.status_code == 202:  # Accepted,
            return r.json()

        else:
            logger.error("Error while making %s request to %s: %s (error code %s)", method, endpoint, r.json(), r.status_code)
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

    def get_meta_information(self, path, fields=None, limit=None, offset=None, preview_crop=None, preview_size=None,
                             sort=None):
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

    def get_list_of_files(self, limit=None, media_type=None, offset=None, fields=None, preview_size=None,
                          preview_crop=None):

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

    def get_latest_uploaded_files(self, limit=None, media_type=None, fields=None, preview_size=None, preview_crop=None):

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
    def upload_file_to_yandex(self, path, overwrite=False, fields=None):

        data = {
            "path": path,
            "overwrite": overwrite,
            "fields": fields
        }

        self._make_request("GET", "/v1/disk/resources/upload", data)

    def download_file_from_yandex(self, path, fields=None):

        data = {
            "path": path,
            "fields": fields
        }

        url_response = self._make_request("GET", "/v1/disk/resources/download", data)

        if url_response is not None:
            url = url_response['href']
            r = self._make_request("GET", url, absolute_url= True)

    def copy(self, from_, path, overwrite= False, fields = None ):

        data = {
            "from": from_,
            "path": path,
            "overwrite": overwrite,
            "fields": fields
        }


        copy_response = self._make_request("POST", "/v1/disk/resources/copy", data)
        url = copy_response["href"]


        if 'operations' in url:
            return self.waiting_for_successful_status(url, data)

        return copy_response


    def move(self, from_, path, overwrite= False, fields = None ):

        data = {
            "from": from_,
            "path": path,
            "overwrite": overwrite,
            "fields": fields
        }


        move_response = self._make_request("POST", "/v1/disk/resources/move", data)
        url = move_response["href"]


        if 'operations' in url:
            return self.waiting_for_successful_status(url, data)

        return move_response

    def delete(self, path, permanently= False, fields= None):
        data = {
            "path": path,
            "permanently": permanently,
            "fields": fields
        }

        delete_response = self._make_request("DELETE", "/v1/disk/resources", data)
        url = delete_response["href"]

        if 'operation' in url:
            return self.waiting_for_successful_status(url, data)

    def mkdir(self, path, fields= None):

        data = {
            "path": path,
            "fields": fields
        }

        create_response = self._make_request("PUT", "/v1/disk/resources", data)

        return create_response

    def publish(self, path):
        data ={

            "path": path
        }

        publish_response = self._make_request("PUT", "/v1/disk/resources/publish", data)

        return publish_response


    def unpublish(self, path):
        data ={

            "path": path
        }

        unpublish_response = self._make_request("PUT", "/v1/disk/resources/unpublish", data)

        return unpublish_response


    def metainfo_about_public_resource(self, public_key, path= None, sort= None, limit= 20, preview_size= None, preview_crop= False, offset= None):

        data = {
            "public_key": public_key,
            "path": path,
            "sort": sort,
            "limit": limit,
            "preview_size": preview_size,
            "preview_crop": preview_crop,
            "offset": offset
        }


        info_response = self._make_request("GET", "/v1/disk/public/resources", data)

        return info_response

    def get_published_resources(self, limit= 20, offset= None, type= None, fields= None, preview_size= None):

        data = {


            "limit": limit,
            "offset": offset,
            "type": type,
            "fields": fields,
            "preview_size": preview_size
        }

        published_resources = self._make_request("GET", "/v1/disk/resources/public", data)

        return published_resources










    def waiting_for_successful_status(self, url, data):

        while True:
            time.sleep(0.2)
            response = self._make_request("GET", url, data, absolute_url= True)
            if response["status"] == "success":
                return response