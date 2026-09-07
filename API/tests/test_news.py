import pytest
import allure
from models import NewsResponse, NewsListResponse, TokenResponse
from mocks import MockDB


class TestNews:

    @pytest.mark.positive
    def test_create_news_without_image(self, auth_client):
        resp = auth_client.post("/api/news/", json={
            "title": "Test News",
            "content": "Content",
            "tags": ["test"]
        }, expected_status=201)
        NewsResponse(**resp)

    @pytest.mark.positive
    def test_create_news_with_image(self, auth_client):
        resp = auth_client.post("/api/news/", json={
            "title": "News with image",
            "content": "Content",
            "tags": ["image"],
            "image_url": "http://example.com/img.jpg"
        }, expected_status=201)
        model = NewsResponse(**resp)
        assert model.image_url is not None

    @pytest.mark.positive
    def test_get_all_news(self, auth_client):
        MockDB.create_news("News1", "Content1", ["tag1"])
        MockDB.create_news("News2", "Content2", ["tag2"])
        resp = auth_client.get("/api/news/", expected_status=200)
        NewsListResponse(**resp)

    @pytest.mark.positive
    def test_get_news_with_filters(self, auth_client):
        resp = auth_client.get("/api/news/", params={
            "page": 1,
            "per_page": 5,
            "tag": "test",
            "search": "news"
        }, expected_status=200)
        model = NewsListResponse(**resp)
        assert model.page == 1
        assert model.per_page == 5

    @pytest.mark.positive
    def test_get_news_by_id(self, auth_client):
        news = MockDB.create_news("Detail News", "Detail", ["detail"])
        resp = auth_client.get(f"/api/news/{news['id']}", expected_status=200)
        NewsResponse(**resp)

    @pytest.mark.positive
    def test_get_all_tags(self, auth_client):
        resp = auth_client.get("/api/news/tags", expected_status=200)
        assert isinstance(resp, list)

    @pytest.mark.negative
    def test_get_news_invalid_id(self, auth_client):
        resp = auth_client.get("/api/news/99999", expected_status=404)
        TokenResponse(**resp)