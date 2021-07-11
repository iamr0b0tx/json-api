import asyncio

from fastapi.testclient import TestClient
from unittest.mock import Mock

from main import app, BASE_URL, get_responses_func, redis_cache

client = TestClient(app)


async def get_responses_func_mock():
    async def get_responses(tags):
        await asyncio.sleep(.1)
        response = Mock()
        response.json = Mock(return_value={
            "posts": [{
                "id": 1,
                "author": "Rylee Paul",
                "authorId": 9,
                "likes": 960,
                "popularity": 0.13,
                "reads": 50361,
                "tags": ["tech", "health"]
            },
            ]
        })
        return [response]

    return get_responses


async def get_redis_cache_mock():
    async def dummy(*args, **kwargs):
        await asyncio.sleep(.1)

    cache = Mock()
    cache.get = dummy
    cache.set = dummy
    return cache

app.dependency_overrides[redis_cache] = get_redis_cache_mock
app.dependency_overrides[get_responses_func] = get_responses_func_mock


# generic test
def test_get_base_endpoint():
    response = client.get('/')
    assert response.status_code == 404


def test_get_ping():
    response = client.get(f'{BASE_URL}/ping')
    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_get_posts():
    response = client.get(f'{BASE_URL}/posts?tags=history,tech&sortBy=likes&direction=desc')
    assert response.status_code == 200

    response_data = response.json()
    assert "author" in response_data["posts"][0]


def test_get_posts_empty_tags():
    response = client.get(f'{BASE_URL}/posts?tags=')
    assert response.status_code == 400


def test_get_posts_no_tags():
    response = client.get(f'{BASE_URL}/posts')
    assert response.status_code == 400
    assert response.json()["error"] == "Tags parameter is required"


def test_get_posts_no_sortBy():
    response = client.get(f'{BASE_URL}/posts?tags=science')
    assert response.status_code == 200


def test_get_posts_no_direction():
    response = client.get(f'{BASE_URL}/posts?tags=science')
    assert response.status_code == 200


def test_get_posts_invalid_sortBy():
    response = client.get(f'{BASE_URL}/posts?tags=science&sortBy=name')
    assert response.status_code == 400
    assert response.json()["error"] == "sortBy parameter is invalid"


def test_get_posts_invalid_direction():
    response = client.get(f'{BASE_URL}/posts?tags=science&direction=up')
    assert response.status_code == 400
    assert response.json()["error"] == "direction parameter is invalid"
