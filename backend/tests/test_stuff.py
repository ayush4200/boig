from chatbots.api import chat


def test_first():
    response = chat(id=15)
    assert response["message"] == "Index found and connected"


def test_two():
    assert 1 == 2
