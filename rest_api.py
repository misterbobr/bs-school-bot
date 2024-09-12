import requests
import json

class RestApi:

    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
        self.session = requests.Session()

    def get_user_link(self, uid):
        url = self.api_url + f"/course/excel/page/link/{uid}"
        headers = {
            "Authorization": f"{self.api_key}"
        }
        try:
            response = self.session.get(url, params={}, headers=headers, timeout=10)
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
        
    def user_visited_lk(self, uid):
        url = self.api_url + f"/course/excel/users/{uid}"
        headers = {
            "Authorization": f"{self.api_key}"
        }
        try:
            response = self.session.get(url, params={}, headers=headers, timeout=10)
            response.raise_for_status()
            response = response.json()
            return {'result': 'true'} if ('visited' in response and response['visited'] is not None) else {'result': 'false'} 
        except requests.exceptions.HTTPError as errh:
            return errh
        except requests.exceptions.ConnectionError as errc:
            return errc
        except requests.exceptions.Timeout as errt:
            return errt
        except requests.exceptions.RequestException as err:
            return err
        
    def get_user_lessons(self, uid):
        url = self.api_url + f"/course/excel/users/{uid}/lessons"
        headers = {
            "Authorization": f"{self.api_key}"
        }
        try:
            response = self.session.get(url, params={}, headers=headers, timeout=10)
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
        url = self.api_url + '/course/excel/submissions'
        headers = {
            "Authorization": f"{self.api_key}"
        }
        payload = {
            'name': name,
            'phone': phone,
            'email': email
        }
        try:
            response = self.session.post(url, data=payload, headers=headers, timeout=10)
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
        url = self.api_url + '/course/excel/users'
        headers = {
            "Authorization": f"{self.api_key}"
        }
        payload = {
            "submission_id": submission_id,
            "tg_uid": tg_uid,
            "first_name": tg_first_name,
            "last_name": tg_last_name,
            "username": tg_username,
            "tg_picture": tg_picture
        }
        try:
            response = self.session.post(url, data=payload, headers=headers, timeout=20)
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
        
    def user_subscription(self, uid):
        url = self.api_url + f"/users/{uid}"
        headers = {
            "Authorization": f"{self.api_key}"
        }
        payload = {
            'subscribed': 1
        }
        try:
            response = self.session.patch(url, data=payload, headers=headers, timeout=20)
            response.raise_for_status()
            # check that response is number and greater than 0
            response = response.json()
            return {'result': 'success'} if (type(response) == int and response > 0) else {'result': 'failed'} 
        except requests.exceptions.HTTPError as errh:
            return errh
        except requests.exceptions.ConnectionError as errc:
            return errc
        except requests.exceptions.Timeout as errt:
            return errt
        except requests.exceptions.RequestException as err:
            return err