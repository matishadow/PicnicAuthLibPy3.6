import requests
import json
import base64


class PicnicAuthClient(object):
    def __init__(self, base_endpoint, api_key):
        self.base_endpoint = base_endpoint
        self.api_key = api_key
        self.authorization_header = {
            'Authorization': 'Bearer {}'.format(api_key)
        }

    def create_request_url(self, endpoint_url):
        return self.base_endpoint + endpoint_url

    def login(self, username, password):
        request_url = self.create_request_url('tokens')
        request = requests.post(request_url, headers=self.authorization_header,
                                data={'grant_type': 'password', 'username': username, 'password': password})
        response = request.json()
        self.api_key = response['access_token']
        self.authorization_header = {
            'Authorization': 'Bearer {}'.format(self.api_key)
        }

        return request

    def get_auth_users(self, page=1, page_count=10):
        request_url = self.create_request_url('Companies/Me/AuthUsers')
        request = requests.get(request_url, headers=self.authorization_header,
                               params={'page': page, 'pageCount': page_count})

        return request

    def add_auth_user(self, external_id, username, email):
        request_url = self.create_request_url('AuthUsers')
        request = requests.post(request_url, headers=self.authorization_header,
                                data={'ExternalId': external_id, 'UserName': username, 'Email': email})

        return request

    def generate_new_secret(self, user_id):
        request_url = self.create_request_url('AuthUsers/{}/secret'.format(user_id))
        request = requests.patch(request_url, headers=self.authorization_header)

        return request

    def get_logged_company(self):
        request_url = self.create_request_url('Companies/Me')
        request = requests.get(request_url, headers=self.authorization_header)

        return request

    def add_company(self, email, username, password):
        request_url = self.create_request_url('Companies')
        request = requests.post(request_url, data={'Email': email, 'UserName': username, 'Password': password,
                                                   'ConfirmPassword': password})

        return request

    def get_hotp_for_authuser(self, user_id):
        request_url = self.create_request_url('AuthUsers/{}/hotp'.format(user_id))
        request = requests.get(request_url, headers=self.authorization_header)

        return request

    def get_totp_for_authuser(self, user_id):
        request_url = self.create_request_url('AuthUsers/{}/totp'.format(user_id))
        request = requests.get(request_url, headers=self.authorization_header)

        return request

    def validate_hotp(self, user_id, hotp):
        request_url = self.create_request_url('AuthUsers/{}/hotp/{}'.format(user_id, hotp))
        request = requests.get(request_url, headers=self.authorization_header)

        return request

    def validate_totp(self, user_id, totp):
        request_url = self.create_request_url('AuthUsers/{}/totp/{}'.format(user_id, totp))
        request = requests.get(request_url, headers=self.authorization_header)

        return request





