import pytest
import allure
from models import CommentResponse, TokenResponse
from mocks import MockDB


class TestComments:

    @pytest.mark.positive
    def test_create_comment(self, auth_client):
        news = MockDB.create_news("Comment News", "Content", ["comment"])
        resp = auth_client.post(f"/api/news/{news['id']}/comments", json={
            "content": "Great news!"
        }, expected_status=201)
        CommentResponse(**resp)

    @pytest.mark.positive
    def test_get_comments(self, auth_client):
        news = MockDB.create_news("Comments News", "Content", ["comments"])
        MockDB.create_comment(news["id"], 1, "First")
        MockDB.create_comment(news["id"], 1, "Second")
        resp = auth_client.get(f"/api/news/{news['id']}/comments", expected_status=200)
        assert isinstance(resp, list)
        for item in resp:
            CommentResponse(**item)

    @pytest.mark.negative
    def test_create_comment_invalid_news(self, auth_client):
        resp = auth_client.post("/api/news/99999/comments", json={
            "content": "Invalid"
        }, expected_status=404)
        TokenResponse(**resp)