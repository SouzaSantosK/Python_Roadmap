import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dependencies import handle_session
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    # Base.metadata.drop_all(bind=engine)


def override_handle_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[handle_session] = override_handle_session


@pytest_asyncio.fixture
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def generate_sample_post_id(ac: AsyncClient):
    sample_post = {
        "title": "Sample post",
        "content": "sample post content",
        "category": "Programming",
        "tags": ["sample", "post"],
    }

    response = await ac.post(
        "/blog/posts",
        json=sample_post,
    )

    assert response.status_code == 201
    return response.json()["id"]


@pytest.mark.asyncio
async def test_create_new_post(ac: AsyncClient):
    new_post_data = {
        "title": "Automatic test post",
        "content": "Content long enough for test",
        "category": "Programming",
        "tags": ["pytest", "fastapi"],
    }

    response = await ac.post("/blog/posts", json=new_post_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_post_empty_tags():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        new_post = {
            "title": "Post",
            "content": "Some text here.",
            "category": "Testing",
            "tags": [],
        }

        response = await ac.post("/blog/posts", json=new_post)
        assert response.status_code == 201
        assert response.json()["tags"] == []


@pytest.mark.asyncio
async def test_get_posts(ac: AsyncClient, generate_sample_post_id: int):
    post_id = generate_sample_post_id

    # getting posts by id
    get_response = await ac.get(f"/blog/posts/{post_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == post_id

    # getting all posts
    get_all = await ac.get("/blog/posts")
    assert get_all.status_code == 200


@pytest.mark.asyncio
async def test_get_posts_by_term(ac: AsyncClient):
    new_post = {
        "title": "Python",
        "content": "Testing getting post by term Python.",
        "category": "Testing",
        "tags": [],
    }

    response = await ac.post("/blog/posts", json=new_post)
    assert response.status_code == 201

    response = await ac.get("/blog/posts?term=Python")

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) > 0
    assert "Python" in posts[0]["title"]


@pytest.mark.asyncio
async def test_delete_post(ac: AsyncClient, generate_sample_post_id: int):
    post_id = generate_sample_post_id
    response = await ac.delete(f"/blog/posts/{post_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_update_post(ac: AsyncClient, generate_sample_post_id: int):

    post_id = generate_sample_post_id
    new_post = {
        "title": "UPDATED",
        "content": "UPDATED",
        "category": "UPDATED",
        "tags": ["UPDATED POST"],
    }

    put_response = await ac.put(f"/blog/posts/{post_id}", json=new_post)
    assert put_response.status_code == 200
    assert put_response.json()["title"] == new_post["title"]
