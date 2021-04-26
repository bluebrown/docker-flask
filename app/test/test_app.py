from app import create_app
from json import dumps


def test_get_messages():
    app = create_app()
    with app.test_client() as tc:
        res = tc.get("/msg")
        assert res.status_code == 200
        assert res.content_type == "application/json"


def test_post_message():
    app = create_app()
    with app.test_client() as tc:
        res = tc.post(
            "/msg", data=dumps(dict(foo="bar")), content_type="application/json"
        )
        assert res.status_code == 201
        assert res.content_type == "application/json"


def test_get_pdf():
    app = create_app()
    with app.test_client() as tc:
        res = tc.get("/pdf")
        assert res.status_code == 200
        assert res.content_type == "application/pdf"


def test_alive():
    app = create_app()
    with app.test_client() as tc:
        res = tc.get("/alive")
        assert res.status_code == 200


def test_ready():
    app = create_app()
    with app.test_client() as tc:
        res = tc.get("/ready")
        assert res.status_code == 200
