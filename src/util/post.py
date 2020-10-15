import requests
from requests import Response


class PostUtil:
    @staticmethod
    def post_form_data(url: str, data: dict) -> Response:
        return requests.post(url, data)
