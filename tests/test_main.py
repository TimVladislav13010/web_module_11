from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

'''
Functional tests main (healthchecker).
'''


def test_read_main():
    """
    The test_read_main function tests the /api/healthchecker endpoint.
    It does so by making a GET request to that endpoint and asserting that the response is 200 OK,
    and also asserts that the JSON response body is {&quot;message&quot;: &quot;Welcome to FastAPI!&quot;}.

    :return: A response object
    :doc-author: Trelent
    """
    response = client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}
