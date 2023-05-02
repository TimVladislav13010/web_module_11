from unittest.mock import MagicMock

from src.database.models import User


'''
Functional tests route Auth.
'''


def test_create_user(client, user, monkeypatch):
    """
    The test_create_user function tests the /api/auth/signup endpoint.
    It does so by creating a user object, and then using the client to send a POST request to the endpoint with that user as JSON data.
    The response is then checked for status code 201 (created), and if it passes, we check that the email in our payload matches what we sent.

    :param client: Test the api
    :param user: Create a new user in the database
    :param monkeypatch: Mock the send_email function
    :return: A 201 status code and the email of the user
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["email"] == user.get('email')


def test_repeat_create_user(client, user, monkeypatch):
    """
    The test_repeat_create_user function tests that a user cannot be created twice.
    It does this by first creating a user, then attempting to create the same user again.
    The second attempt should fail with an HTTP 409 status code and an error message.

    :param client: Make requests to the api
    :param user: Create a user in the database before each test
    :param monkeypatch: Mock the send_email function
    :return: A 409 status code
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 409, response.text
    payload = response.json()
    assert payload["detail"] == "Account already exists"


def test_login_user_not_confirmed_email(client, user):
    """
    The test_login_user_not_confirmed_email function tests that a user cannot login if their email is not confirmed.
        The test_login_user_not_confirmed_email function takes in the client and user fixtures as parameters.
        The response variable stores the result of calling the post method on our client object, passing in &quot;/api/auth/login&quot; as an argument to get our /api/auth/login endpoint, and passing in data={&quot;username&quot;: user.get(&quot;email&quot;), &quot;password&quot;: user.get(&quot;password&quot;)} to send a POST request with JSON data containing username and password keys set to values from our fixture's dictionary.

    :param client: Make requests to the flask application
    :param user: Pass the user data to the test function
    :return: An error message
    :doc-author: Trelent
    """
    response = client.post("/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    assert response.status_code == 401, response.text
    payload = response.json()
    assert payload["detail"] == "Email not confirmed"


def test_login_user(client, user, session):
    """
    The test_login_user function tests the login endpoint.
    It first confirms the user, then logs in with their email and password.
    The response is checked for a 200 status code and a token_type of &quot;bearer&quot;.


    :param client: Make requests to the flask application
    :param user: Create a new user in the database
    :param session: Create a user in the database
    :return: A payload containing a token_type of bearer
    :doc-author: Trelent
    """
    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["token_type"] == "bearer"


def test_login_user_with_wrong_password(client, user, session):
    """
    The test_login_user_with_wrong_password function tests the login endpoint with a user that has been confirmed, but
    with an incorrect password. The test should return a 401 status code and an error message.

    :param client: Make requests to the application
    :param user: Create a new user in the database
    :param session: Create a new user in the database
    :return: The following:
    :doc-author: Trelent
    """
    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={"username": user.get("email"), "password": "password"})
    assert response.status_code == 401, response.text
    payload = response.json()
    assert payload["detail"] == "Invalid password"


def test_login_user_with_wrong_email(client, user, session):
    """
    The test_login_user_with_wrong_email function tests the login endpoint with a wrong email.
        It should return 401 and an error message.

    :param client: Make requests to the api
    :param user: Create a user in the database
    :param session: Create a new user in the database
    :return: A 401 status code and a payload with the detail &quot;invalid email&quot;
    :doc-author: Trelent
    """
    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={"username": "eaxample@test.com", "password": user.get("password")})
    assert response.status_code == 401, response.text
    payload = response.json()
    assert payload["detail"] == "Invalid email"
