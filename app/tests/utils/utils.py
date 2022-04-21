import json
import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_text() -> str:
    text = ""
    for i in range(50):
        word = "".join(random.choices(string.ascii_lowercase, k=10))
        text = text + " " + word
    return text


def random_price() -> int:
    return random.randint(0, 1000000)


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


class Random_Item:
    def __init__(self):
        self.title = random_lower_string()
        self.description = random_text()
        self.price = random_price()


def wrap_to_jsonrpc(data: dict, method: str):
    to_encode = dict(jsonrpc="2.0", id=1, method=method, params=data)

    encoded = json.dumps(to_encode)

    return encoded


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    login_data = wrap_to_jsonrpc(login_data, "login_access_token")

    r = client.post("/api/v1/jsonrpc", data=login_data)
    tokens = r.json()
    a_token = tokens["result"]["access_token"]
    headers = {"Authorization": f"bearer {a_token}"}
    return headers
