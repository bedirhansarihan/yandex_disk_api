import time

import requests
import typing
import logging
import json
import os
from pathlib import Path

logger = logging.getLogger()


class YandexClient():

    def __init__(self, client_id, client_secret, token):

        self._base_url = "https://cloud-api.yandex.net"

        self._client_id = client_id
        self._client_secret = client_secret
        self._token = token

        self._headers = {'Authorization': 'OAuth {}'.format(self._token)}


        logger.info("Yandex Client has been created successfuly")

    def _make_request(self, method: str, endpoint: str, data: typing.Dict, absolute_url= False, json = True):

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

            if json:
                return r.json()
            else:
                return r

        elif r.status_code == 201:  # Created,  The request succeeded, and a new resource was created as a result.
            if json:
                return r.json()
            else:
                return r

        elif r.status_code == 202:  # Accepted,
            if json:
                return r.json()
            else:
                return r

        else:
            if json:
                logger.error("Error while making %s request to %s: %s (error code %s)", method, endpoint, r.json(), r.status_code)
                return None
            else:
                logger.error("Error while making %s request to %s: %s (error code %s)", method, endpoint, r,
                             r.status_code)
                return None

    def get_disk_information(self):
        """
        The API returns general information about a user's Disk:

        https://yandex.com/dev/disk/api/reference/capacity.html

        :return:
        """

        info = self._make_request("GET", "/v1/disk", dict())

        return info

    def get_meta_information(self, path, fields=None, limit=20, offset=None, preview_crop=False, preview_size=None,
                             sort=None):
        """
        In order to request metainformation about files and folders

        https://yandex.com/dev/disk/api/reference/meta.html

        :param path: str <resource path>
        :param fields:
        :param limit: int <maximum number of returned resources>
        :param offset: int <offset from the top of the list>
        :param preview_crop: boolean <whether to crop the preview [True, False]>
        :param preview_size: str
        :param sort: str <The attribute used to sort the list of resources in the folder. [name, path, created, modified, size]>

        :return: json_file
        """
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

    def get_list_of_files(self, limit=20, media_type=None, offset=None, fields=None, preview_size=None,
                          preview_crop=False):
        """
        In order to  flat list of all files. (NOT FOLDERS!)

        https://yandex.com/dev/disk/api/reference/all-files.html

        :param limit: int <maximum number of returned resources>
        :param media_type: str <The type of files to include in the list. [audio, backup, image, video, etc.]>
        :param offset: int <offset from the top of the list>
        :param fields:
        :param preview_size:
        :param preview_crop: boolean <whether to crop the preview [True, False]>

        :return: json_file
        """
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

    def get_latest_uploaded_files(self, limit=20, media_type=None, fields=None, preview_size=None, preview_crop=None):
        """
        The API returns a list of the files most recently uploaded to Yandex.Disk.

        https://yandex.com/dev/disk/api/reference/recent-upload.html

        :param limit: int <maximum number of returned resources>
        :param media_type: str <The type of files to include in the list. [audio, backup, image, video, etc.]>
        :param fields:
        :param preview_size:
        :param preview_crop: boolean <whether to crop the preview [True, False]>
        :return json_file:
        """
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
        """
        To upload a file to Yandex.Disk

        https://yandex.com/dev/disk/api/reference/upload.html

        :param path: str <path for the file upload>
        :param overwrite: boolean <Whether to overwrite the file [True, False[>
        :param fields:
        :return:
        """
        data = {
            "path": path,
            "overwrite": overwrite,
            "fields": fields
        }

        upload_response = self._make_request("GET", "/v1/disk/resources/upload", data)

        if upload_response is not None:
            logger.info("file %s has uploaded to Yandex.Disk successfully", path)

    def download_file_from_yandex(self, path, fields=None):
        """
        To download a file from Yandex.Disk

        https://yandex.com/dev/disk/api/reference/content.html

        :param path: str <path to the file to download>
        :param fields:
        :return:
        """
        data = {
            "path": path,
            "fields": fields
        }

        url_response = self._make_request("GET", "/v1/disk/resources/download", data)

        if url_response is not None:
            logger.info("file %s has downloaded from Yandex.Disk successfully", path)

    def copy(self, from_, path, overwrite= False, fields = None ):
        """
        To copy files and folders on a user's Disk,

        https://yandex.com/dev/disk/api/reference/copy.html

        :param from_: str <path to the resource to copy>
        :param path: str <path to the resource to copy>
        :param overwrite: boolean <overwriting flag [True, False]>
        :param fields:
        :return:
        """
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
        """
        To move files and folders on Yandex.Disk,

        https://yandex.com/dev/disk/api/reference/move.html

        :param from_: str <path to the resource to move>
        :param path: str <path to the moved resource>
        :param overwrite: <overwriting flag [True, False]>
        :param fields:
        :return:
        """
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

    def delete(self, path, permanently=False, fields=None):
        """
        To delete files and folders on a user's Disk,

        https://yandex.com/dev/disk/api/reference/delete.html

        :param path: str <path to the resource to delete>
        :param permanently: <whether to permanently delete the resource [True, False]>
        :param fields:
        :return:
        """
        data = {
            "path": path,
            "permanently": permanently,
            "fields": fields
        }

        delete_response = self._make_request("DELETE", "/v1/disk/resources", data)
        url = delete_response["href"]

        if 'operation' in url:
            return self.waiting_for_successful_status(url, data)

    def mkdir(self, path, fields=None):
        """
        To create a folder on Yandex.Disk,

        https://yandex.com/dev/disk/api/reference/create-folder.html

        :param path: str <path to the created folder>
        :param fields:
        :return: json_file
        """
        data = {
            "path": path,
            "fields": fields
        }

        # check whether file is already exists or not
        if  self.is_dir_exists(path):
            logger.warning("directory: %s has been already created", path)
            return None

        create_response = self._make_request("PUT", "/v1/disk/resources", data)
        logger.info("directory: %s has been created successfully", path)

        return create_response

    def publish(self, path):
        """
        Files and folders on a user's Disk can be published by generating links that will allow them to be accessed by people other than the owner.

        https://yandex.com/dev/disk/api/reference/publish.html

        :param path: str <path to the resource to publish>
        :return: json_file
        """
        data ={

            "path": path
        }

        publish_response = self._make_request("PUT", "/v1/disk/resources/publish", data)

        if publish_response is not None:

            logger.info("file %s has published successfully", path)
            return publish_response


    def unpublish(self, path):
        """
        To close access to a resource,

        https://yandex.com/dev/disk/api/reference/publish.html

        :param path: str <path to the resource to close>
        :return:
        """
        data ={

            "path": path
        }

        unpublish_response = self._make_request("PUT", "/v1/disk/resources/unpublish", data)

        if unpublish_response is not None:

            logger.info("file %s has unpublished successfully", path)
            return unpublish_response

    ## check whether json= true or false
    def metainfo_about_public_resource(self, public_key, path=None, sort=None, limit=20, preview_size=None, preview_crop=False, offset=None):
        """
        If you know the key for a public resource or the public link to it, you can request metainformation about this resource

        https://yandex.com/dev/disk/api/reference/public.html

        :param public_key: str <Key to a public resource, or the public link to a resource.>
        :param path: str <resource path>
        :param sort: str <The attribute used to sort the list of resources in the folder. [name, path, created, modified, size]>
        :param limit: int <maximum number of returned resources>
        :param preview_size:
        :param preview_crop: boolean <whether to crop the preview [True, False]>
        :param offset: int <offset from the top of the list>
        :return: json_file
        """
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

        if info_response is not None:

            logger.info("Information from %s has collected successfully", path)
            return info_response

    def get_published_resources(self, limit= 20, offset= None, type= None, fields= None, preview_size= None):
        """
        The API returns a list of resources published on the user's Disk.

        https://yandex.com/dev/disk/api/reference/recent-public.html

        :param limit: int <maximum number of returned resources>
        :param offset: int <offset from the top of the list>
        :param type: str <type of requested files [dir, file]>
        :param fields:
        :param preview_size:
        :return: json_file
        """
        data = {


            "limit": limit,
            "offset": offset,
            "type": type,
            "fields": fields,
            "preview_size": preview_size
        }

        published_resources = self._make_request("GET", "/v1/disk/resources/public", data)

        return published_resources

    def is_dir_exists(self, path) -> bool:
        """
        Checks whether directory exists or not

        :param path:
        :return:
        """

        _relative_path = os.path.dirname(path)

        meta_info = self.get_meta_information(_relative_path)
        items = meta_info['_embedded']['items']

        for f in items:
            if f['path'] == 'disk:'+ path:
                return True

        else:
            return False




    def waiting_for_successful_status(self, url, data):

        while True:
            time.sleep(0.2)
            response = self._make_request("GET", url, data, absolute_url= True)
            if response["status"] == "success":
                return response


