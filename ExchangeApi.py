import requests
import json
import urllib.parse


class Exchange:
    base_url: str = 'https://api.currencyapi.com/v3/'

    def __init__(self, token: str):
        self.token: str = token

    def latest(self):
        json_response: json = self.get_request(relative_path='./latest')
        return json_response


# метод которые отправляет GET запрос
    def get_request(self, relative_path: str = None) -> json:
        url: str = urllib.parse.urljoin(self.base_url, relative_path)
        headers: dict[str, str] = {'apikey': self.token}
        response: requests.Response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise f'Код {response.status_code} не соответствует 200.'
        return json.loads(response.content)
        # url_endpoint = 'https://www.duckduckgo.com'
        # mydict = {'q': 'whee! Stanford!!!', 'something': 'else'}
        # resp = requests.get(url_endpoint, params=mydict)

# метод который отправляет POST запрос
    def post_request(self, relative_path: str = None):
        url = urllib.parse.urljoin(self.base_url, relative_path)
        # payload: dict[str, str] = {'some': 'data'}
        headers: dict[str, str] = {'apikey': self.token}

        # r = requests.post(url, data=json.dumps(payload), headers=headers)
        r = requests.post(url, headers=headers)
