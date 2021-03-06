import unittest
import six
import requests
from tests.bandwidth.helpers import get_account_client as get_client
from tests.bandwidth.helpers import create_response, AUTH, headers
if six.PY3:
    from unittest.mock import patch, MagicMock
    builtins = 'builtins'
else:
    from mock import patch, MagicMock
    builtins = '__builtin__'

from bandwidth.voice import Client


class MediaTests(unittest.TestCase):

    def test_list_media_files(self):
        """
        list_media_files() should return media files
        """
        estimated_json = """
        [{
            "mediaName": "file1"
        }]
        """
        with patch('requests.request', return_value=create_response(200, estimated_json)) as p:
            client = get_client()
            data = list(client.list_media_files())
            p.assert_called_with(
                'get',
                'https://api.catapult.inetwork.com/v1/users/userId/media',
                headers=headers,
                auth=AUTH)
            self.assertEqual('file1', data[0]['media_name'])

    def test_upload_media_file(self):
        """
        upload_media_file() should upload file
        """
        with patch('requests.request', return_value=create_response(200)) as p:
            upload_headers = {
                'content-type': 'application/octet-stream',
                'User-Agent': headers['User-Agent']
            }
            client = get_client()
            client.upload_media_file('file1', '123')
            p.assert_called_with('put', 'https://api.catapult.inetwork.com/v1/users/userId/media/file1', auth=AUTH,
                                 data='123', headers=upload_headers)

    def test_upload_media_file_by_path(self):
        """
        upload_media_file() should upload file by file path
        """
        with patch('requests.request', return_value=create_response(200)) as p:
            upload_headers = {
                'content-type': 'application/octet-stream',
                'User-Agent': headers['User-Agent']
            }
            client = get_client()
            mock_file_object = MagicMock()
            mock_close = MagicMock()
            setattr(mock_file_object, 'close', mock_close)
            with patch('%s.open' % builtins, return_value=mock_file_object) as f:
                client.upload_media_file('file1', file_path='/path/to/file1')
                p.assert_called_with('put', 'https://api.catapult.inetwork.com/v1/users/userId/media/file1', auth=AUTH,
                                     data=mock_file_object, headers=upload_headers)
                f.assert_called_with('/path/to/file1', 'rb')
                self.assertTrue(mock_close.called)

    def test_download_media_file(self):
        """
        download_media_file() should download file
        """
        estimated_response = create_response(200, '123', 'text/plain')
        estimated_response.raw = MagicMock()
        with patch('requests.request', return_value=estimated_response) as p:
            client = get_client()
            content, content_type = client.download_media_file('file1')
            p.assert_called_with(
                'get',
                'https://api.catapult.inetwork.com/v1/users/userId/media/file1',
                auth=AUTH,
                headers=headers,
                stream=True)
            self.assertEqual('text/plain', content_type)
            self.assertIs(estimated_response.raw, content)

    def test_delete_media_file(self):
        """
        delete_media_file() should remove a media file
        """
        with patch('requests.request', return_value=create_response(200)) as p:
            client = get_client()
            client.delete_media_file('file1')
            p.assert_called_with(
                'delete',
                'https://api.catapult.inetwork.com/v1/users/userId/media/file1',
                headers=headers,
                auth=AUTH)
