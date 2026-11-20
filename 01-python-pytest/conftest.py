import httpx
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def client():
    print("\n[setup] opening HTTP client")   
    with httpx.Client(base_url=BASE_URL, timeout=10) as c:
        yield c
    print("\n[teardown] closing HTTP client")

@pytest.fixture
def new_post():
    return {"title": "QA", "body": "Testing", "userId": 1}