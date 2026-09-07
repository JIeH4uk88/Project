from typing import List, Dict, Any
from datetime import datetime
import uuid

class MockDB:
    _users = {}
    _news = {}
    _comments = {}
    _tokens = {}

    @classmethod
    def register_user(cls, email: str, password: str):
        if email in cls._users:
            return None
        user_id = len(cls._users) + 1
        cls._users[email] = {"id": user_id, "email": email, "password": password}
        return user_id

    @classmethod
    def login_user(cls, email: str, password: str):
        user = cls._users.get(email)
        if user and user["password"] == password:
            token = str(uuid.uuid4())
            cls._tokens[token] = user["id"]
            return token
        return None

    @classmethod
    def create_news(cls, title: str, content: str, tags: List[str], image_url: str = None):
        news_id = len(cls._news) + 1
        cls._news[news_id] = {
            "id": news_id,
            "title": title,
            "content": content,
            "image_url": image_url,
            "tags": tags,
            "created_at": datetime.now().isoformat(),
            "comments_count": 0,
        }
        return cls._news[news_id]

    @classmethod
    def get_news(cls, page=1, per_page=10, tag=None, search=None):
        items = list(cls._news.values())
        if tag:
            items = [n for n in items if tag in n["tags"]]
        if search:
            items = [n for n in items if search.lower() in n["title"].lower()]
        total = len(items)
        start = (page - 1) * per_page
        end = start + per_page
        return {"items": items[start:end], "total": total, "page": page, "per_page": per_page}

    @classmethod
    def get_news_by_id(cls, news_id: int):
        return cls._news.get(news_id)

    @classmethod
    def get_all_tags(cls):
        tags = set()
        for item in cls._news.values():
            tags.update(item["tags"])
        return list(tags)

    @classmethod
    def create_comment(cls, news_id: int, author_id: int, content: str):
        if news_id not in cls._news:
            return None
        comment_id = len(cls._comments) + 1
        cls._comments[comment_id] = {
            "id": comment_id,
            "news_id": news_id,
            "author_id": author_id,
            "content": content,
            "created_at": datetime.now().isoformat(),
        }
        cls._news[news_id]["comments_count"] += 1
        return cls._comments[comment_id]

    @classmethod
    def get_comments(cls, news_id: int):
        return [c for c in cls._comments.values() if c["news_id"] == news_id]