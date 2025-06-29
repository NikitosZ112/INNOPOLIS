import requests
from datetime import datetime, timedelta
from config.settings import YANDEX_API_KEY

class YandexAuth:
    _iam_token = None
    _expires_at = None

    @classmethod
    def get_iam_token(cls):
        """Получает IAM-токен через API-ключ"""
        if cls._iam_token and cls._expires_at > datetime.now():
            return cls._iam_token

        response = requests.post(
            "https://iam.api.cloud.yandex.net/iam/v1/tokens",
            headers={"Authorization": f"Api-Key {YANDEX_API_KEY}"}
        )
        response.raise_for_status()

        cls._iam_token = response.json()["iamToken"]
        cls._expires_at = datetime.now() + timedelta(hours=11)
        return cls._iam_token