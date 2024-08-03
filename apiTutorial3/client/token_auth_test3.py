import requests

def client():
    credentials = {
        'username': 'amk',
        'password1': 'testing321...',
        'password2': 'testing321...',
    }

    response = requests.post(
        url='http://127.0.0.1:8000/api/rest-auth/registration/',
        data=credentials,
    )

    print('Status Code:', response.status_code)
    print('Response Body:', response.text)

if __name__ == '__main__':
    client()
