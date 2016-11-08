import unittest
import six
import requests
import helpers
if six.PY3:
    from unittest.mock import patch
else:
    from mock import patch

from bandwidth.catapult import Client

class TranscriptionTests(unittest.TestCase):
    def test_get_transcriptions(self):
        """
        get_transcriptions() should return transcriptions
        """
        estimated_json="""
        [{
            "chargeableDuration": 60,
            "id": "{transcription-id}",
            "state": "completed",
            "time": "2014-10-09T12:09:16Z",
            "text": "{transcription-text}",
            "textSize": 3627,
            "textUrl": "{url-to-full-text}"
        }]
        """
        with patch('requests.request', return_value = helpers.create_response(200, estimated_json)) as p:
            client = helpers.get_client()
            data = list(client.get_transcriptions('recordingId'))
            p.assert_called_with('get', 'https://api.catapult.inetwork.com/v1/users/userId/recordings/recordingId/transcriptions', auth=helpers.AUTH, params=None)
            self.assertEqual('{transcription-id}', data[0]['id'])

    def test_create_transcription(self):
        """
        create_transcription() should create a transcription and return id
        """
        estimated_response = helpers.create_response(201)
        estimated_response.headers['Location'] = 'http://localhost/transcriptionId'
        with patch('requests.request', return_value = estimated_response) as p:
            client = helpers.get_client()
            id = client.create_transcription('recordingId')
            p.assert_called_with('post', 'https://api.catapult.inetwork.com/v1/users/userId/recordings/recordingId/transcriptions', auth=helpers.AUTH, json={})
            self.assertEqual('transcriptionId', id)


    def test_get_transcription(self):
        """
        get_transcription() should return a transcription
        """
        estimated_json="""
        {
            "chargeableDuration": 60,
            "id": "{transcription-id}",
            "state": "completed",
            "time": "2014-10-09T12:09:16Z",
            "text": "{transcription-text}",
            "textSize": 3627,
            "textUrl": "{url-to-full-text}"
        }
        """
        with patch('requests.request', return_value = helpers.create_response(200, estimated_json)) as p:
            client = helpers.get_client()
            data = client.get_transcription('recordingId', 'transcriptionId')
            p.assert_called_with('get', 'https://api.catapult.inetwork.com/v1/users/userId/recordings/recordingId/transcriptions/transcriptionId', auth=helpers.AUTH)
            self.assertEqual('{transcription-id}', data['id'])
