import httpx

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_single_post_returns_200():
    response = httpx.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200  

def test_single_post_has_expected_fields():
    post = httpx.get(f"{BASE_URL}/posts/1").json()
    assert post["userId"] == 1
    assert post["id"] == 1  
    assert post["title"] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    assert post["body"] == "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"

def test_users_endpoint_returns_10_users():
    users = httpx.get(f"{BASE_URL}/users").json()
    assert len(users) == 10

def test_missing_post_returns_404():
    response = httpx.get(f"{BASE_URL}/posts/9999")
    assert response.status_code == 404

def test_create_post_return_201():
    new_post = {"title": "QA", "body": "Testing", "userId": 1}

    response = httpx.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code == 201
    created_post = response.json()
    assert created_post["title"] == new_post["title"]
    assert created_post["body"] == new_post["body"]
    assert created_post["userId"] == new_post["userId"]
    assert created_post["id"] == 101

def test_delete_post_returns_200():
    response = httpx.delete(f"{BASE_URL}/posts/1")
    assert response.status_code == 200