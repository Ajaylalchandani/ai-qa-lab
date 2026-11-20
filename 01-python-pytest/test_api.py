import csv
from pathlib import Path
import pytest

def load_post_cases():
    path = Path(__file__).parent / "data" / "posts.csv"
    with open(path, newline="", encoding="utf-8") as f:
        return [
            (int(row["post_id"]), int(row["expected_status"]), row["expected_user_id"])
            for row in csv.DictReader(f)
        ]

@pytest.mark.parametrize("post_id, expected_status, expected_user_id",load_post_cases())
def test_post_from_csv(client, post_id, expected_status, expected_user_id):
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == expected_status
    if expected_user_id:
        assert response.json()["userId"] == int(expected_user_id)

@pytest.mark.parametrize("post_id, expected_user_id", [
    (1, 1),
    (11, 2),
    (50, 5),
    (100, 10),
])   
def test_post_belongs_to_expected_user(client, post_id, expected_user_id):
    post = client.get(f"/posts/{post_id}").json()
    assert post["userId"] == expected_user_id

def test_get_single_post_returns_200(client):
    response = client.get("/posts/1")
    assert response.status_code == 200  

def test_single_post_has_expected_fields(client):
    post = client.get("/posts/1").json()
    assert post["userId"] == 1
    assert post["id"] == 1  
    assert post["title"] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    assert post["body"] == "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"

def test_users_endpoint_returns_10_users(client):
    users = client.get("/users").json()
    assert len(users) == 10

def test_missing_post_returns_404(client):
    response = client.get("posts/9999")
    assert response.status_code == 404

def test_create_post_return_201(client, new_post):
   
    response = client.post("posts", json=new_post)
    assert response.status_code == 201
    created_post = response.json()
    assert created_post["title"] == new_post["title"]
    assert created_post["body"] == new_post["body"]
    assert created_post["userId"] == new_post["userId"]
    assert created_post["id"] == 101

def test_delete_post_returns_200(client):
    response = client.delete("posts/1")
    assert response.status_code == 200
