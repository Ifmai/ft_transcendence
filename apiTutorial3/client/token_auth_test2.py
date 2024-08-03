import requests
from pprint import pprint

def client():
    token = 'Token f45332ac07bb2873db969511dd2e3359eba4c596'
    headers = {
        'Authorization' : token,
    }
    response = requests.get(
        url='http://127.0.0.1:8000/api/kullanici-profilleri/',
        headers=headers,
    )

    print('Status Code: ', response.status_code)
    response_data = response.json()
    pprint(response_data)

if __name__ == '__main__':
    client()