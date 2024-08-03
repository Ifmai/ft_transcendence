import requests
from pprint import pprint

#{'key': 'f45332ac07bb2873db969511dd2e3359eba4c596'}
def client():
    credentials = {
        'username' : 'testuser',
        'password' : 'testing321...'
    }

    response = requests.post(
        url='http://127.0.0.1:8000/api/rest-auth/login/',
        data=credentials
    )

    print('Status Code: ', response.status_code)
    response_data = response.json()
    pprint(response_data)

if __name__ == '__main__':
    client()