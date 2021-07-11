import asyncio
import json

import httpx
from decouple import config
from fastapi import FastAPI, Depends

from typing import Optional
from typing import List, Literal
from pydantic import BaseModel, constr

from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend


class PostSchema(BaseModel):
    id: int
    author: str
    authorId: int
    likes: int
    popularity: float
    reads: int
    tags: List[str]


class PostRequestSchema(BaseModel):
    posts: List[PostSchema]


class PostResponseSchema(BaseModel):
    posts: Optional[List[PostSchema]] = []


app = FastAPI()
BASE_URL = "/api"
API_URL = config('API_URL', default="https://api.hatchways.io/assessment/blog/posts")
REDIS_URL = config('REDIS_URL', default="redis://127.0.0.1:6379")
DIRECTION_OPTIONS = Literal['asc', 'desc']
SORT_BY_OPTIONS = Literal['id', 'reads', 'likes', 'popularity']


def collate_posts(responses):
    ids = set()
    posts = []

    for resp in responses:
        for post in resp.json()["posts"]:
            if post["id"] in ids:
                continue

            ids.add(post["id"])
            posts.append(post)
    return posts


def parse_error(error):
    """ re-write validation error to match test specification """
    error_dict = {
        "tags": "Tags parameter is required",
        "sortBy": "sortBy parameter is invalid",
        "direction": "direction parameter is invalid"
    }

    try:
        return error_dict.get(error["loc"][1])

    except (IndexError, KeyError) as e:
        print(e)


async def get_responses_func():
    async def get_responses(tags):
        async with httpx.AsyncClient() as client:
            tasks = (client.get(
                f"{API_URL}?tag={tag.strip()}")
                for tag in tags.split(',')
            )
            return await asyncio.gather(*tasks)

    return get_responses


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    response = {}
    for error in exc.errors():
        if parsed_error := parse_error(error):
            response["error"] = parsed_error
            break

    return JSONResponse(response, status_code=400)


def redis_cache():
    return caches.get(CACHE_KEY)


@app.get(f"{BASE_URL}/ping")
def create_and_get_all_uuid():
    return {"success": True}


@app.get(f"{BASE_URL}/posts", response_model=PostResponseSchema)
async def get_posts(tags: constr(strip_whitespace=True, min_length=1),
                    direction: DIRECTION_OPTIONS = "asc", sortBy: Optional[SORT_BY_OPTIONS] = "id",
                    get_responses=Depends(get_responses_func), cache: RedisCacheBackend = Depends(redis_cache)):

    key = f'{tags}{direction}{sortBy}'
    posts_json_str = await cache.get(key)
    print(f"{tags=}, {direction=}, {sortBy=}", bool(posts_json_str))

    if posts_json_str:
        posts = json.loads(posts_json_str)

    else:
        responses = await get_responses(tags)
        posts = collate_posts(responses)
        posts = sorted(posts, key=lambda x: x[sortBy], reverse=(direction == "desc"))
        await cache.set(key, json.dumps(posts))

    return {"posts": posts}


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend(REDIS_URL)
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()
