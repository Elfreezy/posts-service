import json
import pytest

from fastapi import status
from httpx import AsyncClient

from tests.integration.conftest import get_redis_instance


class TestPostsIntegration:
    async def test_create_post(
        self, 
        test_client: AsyncClient,
    ):
        new_post = {
            "title": "CREATE Test Post", 
            "body": "Test content"
        }

        response = await test_client.post(
            "/posts/create/",
            json=new_post,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data.get("title") == new_post.get("title")
        assert data.get("body") == new_post.get("body")
        assert "id" in data
    
    async def test_get_post_by_id(
        self,
        test_client: AsyncClient,
    ):
        new_post = {
            "title": "FIND Test Post", 
            "body": "Test content"
        }

        response = await test_client.post(
            "/posts/create/",
            json=new_post,
        )
        assert response.status_code == status.HTTP_201_CREATED
        post_id = response.json()["id"]
        response = await test_client.get(f"/posts/{post_id}/")
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get("title") == new_post.get("title")
        assert response_data.get("body") == new_post.get("body")

        async with get_redis_instance() as redis_client:
            cache_key = f"post:{post_id}"
            cached = await redis_client.get(cache_key) 
            cached_data = json.loads(cached)
            assert cached_data.get("title") == response_data.get("title")
            assert cached_data.get("body") == response_data.get("body")

    async def test_update_post(
        self,
        test_client: AsyncClient,
    ):
        new_post = {
            "title": "UPDATE Test Post", 
            "body": "Test content"
        }

        new_post_body = {
            "body": "New post body"
        }

        response = await test_client.post(
            "/posts/create/",
            json=new_post,
        )
        post_id = response.json()["id"]
        assert response.status_code == status.HTTP_201_CREATED

        response = await test_client.get(f"/posts/{post_id}/")
        assert response.status_code == status.HTTP_200_OK

        response = await test_client.put(f"/posts/update/{post_id}/", json=new_post_body)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data.get("title") == new_post.get("title")
        assert response_data.get("body") != new_post.get("body")
        assert response_data.get("body") == new_post_body.get("body")

        async with get_redis_instance() as redis_client:
            cache_key = f"post:{post_id}"
            cached = await redis_client.get(cache_key) 
            assert cached is None

    async def test_delete_post(
        self,
        test_client: AsyncClient,
    ):
        new_post = {
            "title": "DELETE Test Post", 
            "body": "Test content"
        }

        response = await test_client.post(
            "/posts/create/",
            json=new_post,
        )
        post_id = response.json()["id"]
        assert response.status_code == status.HTTP_201_CREATED
        
        response = await test_client.get(f"/posts/{post_id}/")
        assert response.status_code == status.HTTP_200_OK

        response = await test_client.delete(f"/posts/delete/{post_id}/")
        assert response.status_code == status.HTTP_200_OK

        async with get_redis_instance() as redis_client:
            cache_key = f"post:{post_id}"
            cached = await redis_client.get(cache_key) 
            assert cached is None
