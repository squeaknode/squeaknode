import pytest

from squeaknode.server.db import get_db
from squeaknode.server.blog import hi


def test_index(client, auth):
    response = client.get("/")
    assert b"test title" in response.data
    assert b"created on 2018-01-01" in response.data
    assert b"test\nbody" in response.data
    assert b'href="/post/1"' in response.data


@pytest.mark.parametrize("path", ("/2/update", "/2/delete"))
def test_exists_required(client, auth, path):
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "body": ""})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 2


def test_show(client, auth, app):
    assert client.get("/post/1").status_code == 200


@pytest.mark.parametrize("path", ("/create",))
def test_create_update_validate(client, auth, path):
    response = client.post(path, data={"title": "", "body": ""})
    assert b"Title is required." in response.data


def test_hi():
    response = hi()
    assert 'hello' == response
