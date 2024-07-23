import requests
import json

class RestApi:

    def __init__(self, api_url):
        self.api_url = api_url

    def get_user_link(self, uid):
        url = self.api_url + '/user'
        payload = {
            'uid': uid
        }
        try:
            response = requests.get(url, params=payload, timeout=10)
            response.raise_for_status()
            response = response.json()
            return response
        except requests.exceptions.HTTPError as errh:
            return errh
        except requests.exceptions.ConnectionError as errc:
            return errc
        except requests.exceptions.Timeout as errt:
            return errt
        except requests.exceptions.RequestException as err:
            return err
        
    def new_submission(self, name, phone, email):
        url = self.api_url + '/new_submission'
        payload = {
            'name': name,
            'phone': phone,
            'email': email
        }
        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            response = response.json()
            return response
        except requests.exceptions.HTTPError as errh:
            return errh
        except requests.exceptions.ConnectionError as errc:
            return errc
        except requests.exceptions.Timeout as errt:
            return errt
        except requests.exceptions.RequestException as err:
            return err

    def register_user(self, submission_id, tg_uid, tg_first_name, tg_last_name, tg_username, tg_picture):
        url = self.api_url + '/user/register'
        payload = {
            'submission_id': submission_id,
            'tg_uid': tg_uid,
            'tg_first_name': tg_first_name,
            'tg_last_name': tg_last_name,
            'tg_username': tg_username,
            'tg_picture': tg_picture
        }
        try:
            response = requests.post(url, data=payload, timeout=20)
            response.raise_for_status()
            response = response.json()
            return response
        except requests.exceptions.HTTPError as errh:
            return errh
        except requests.exceptions.ConnectionError as errc:
            return errc
        except requests.exceptions.Timeout as errt:
            return errt
        except requests.exceptions.RequestException as err:
            return err
        
    def user_subscription(self, tg_uid):
        url = self.api_url + '/user/subscribed'
        payload = {
            'tg_uid': tg_uid
        }
        try:
            response = requests.post(url, data=payload, timeout=20)
            response.raise_for_status()
            response = response.json()
            return response
        except requests.exceptions.HTTPError as errh:
            return errh
        except requests.exceptions.ConnectionError as errc:
            return errc
        except requests.exceptions.Timeout as errt:
            return errt
        except requests.exceptions.RequestException as err:
            return err