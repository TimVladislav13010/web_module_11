import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    update_avatar,
    confirmed_email
)


"""
Unittest repository users.
"""


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new session object and user object for each test.

        :param self: Represent the instance of the object that is being created
        :return: A user object with an id of 1 and email address
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.user = User(id=1,
                         username="test_username",
                         email="test@test.com",
                         password="test_password",
                         refresh_token=None,
                         avatar=None,
                         confirmed=False
                         )

    async def test_get_user_by_email_found(self):
        """
        The test_get_user_by_email function tests the get_user_by_email function in the user.py file.
        It does this by mocking out a session object and returning a mocked User object when queried for
        a specific email address. The test then asserts that the returned value is not None, is an instance of User,
        and has an email and id equal to what was set on our mock.

        :param self: Refer to the instance of the class
        :return: A user object that is not none
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = self.user
        result = await get_user_by_email(email="test@test.com", db=self.session)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, User)
        self.assertEqual(result.email, "test@test.com")
        self.assertEqual(result.id, 1)

    async def test_get_user_by_email_not_found(self):
        """
        The test_get_user_by_email_not_found function tests the get_user_by_email function when a user is not found.
            It does this by mocking the session object and setting its query().filter().first() method to return None.
            Then it calls get_user_by_email with an email address that should not be in the database, and asserts that
            None is returned.

        :param self: Represent the instance of the object that is passed to the method when it is called
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email="test@test.com", db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        """
        The test_create_user function tests the create_user function in the users repository.
        It does this by creating a new user, mocking out Gravatar's get_image method to return a test URL, and then calling
        create_user with that user as an argument. It then asserts that the result is not None (i.e., it exists), is an instance of User, has all of its attributes set correctly.

        :param self: Access the class variables and methods
        :return: A user object
        :doc-author: Trelent
        """
        self.new_user = UserModel(username="test_user", email="test@test.com", password="123456")

        mock_gravatar = MagicMock()
        mock_gravatar.get_image.return_value = "https://www.gravatar.com/avatar/test"

        with patch("src.repository.users.Gravatar", return_value=mock_gravatar):
            result = await create_user(body=self.new_user, db=self.session)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, User)
        self.assertEqual(result.email, "test@test.com")
        self.assertEqual(result.username, "test_user")
        self.assertEqual(result.password, "123456")
        mock_gravatar.get_image.assert_called_once()

    async def test_update_token(self):
        """
        The test_update_token function tests the update_token function in the database.py file.
        It creates a new user, and then updates that user's refresh token to be &quot;new_test_token&quot;.
        Then it asserts that the new token is equal to what was set.

        :param self: Represent the instance of a class
        :return: The new_token, which is equal to the user
        :doc-author: Trelent
        """
        self.new_token = "new_test_token"
        await update_token(user=self.user, token=self.new_token, db=self.session)
        self.assertEqual(self.new_token, self.user.refresh_token)
        self.assertIsNotNone(self.user.refresh_token)

    async def test_update_avatar(self):
        """
        The test_update_avatar function tests the update_avatar function in the users repository.
        It does this by first creating a mock user object, and then patching get_user_by_email to return that mock user.
        Then it calls update avatar with that mocked user, and checks if the result is not None (meaning it was successful).
        It also checks if the result's avatar attribute is not None (meaning an avatar was successfully added),
        and whether or not it equals our test url.

        :param self: Represent the instance of the class
        :return: The user object with the new avatar
        :doc-author: Trelent
        """
        mock_user = self.user
        self.avatar = "url//new_avatar"
        with patch("src.repository.users.get_user_by_email", return_value=mock_user):
            result = await update_avatar(mock_user, url=self.avatar, db=self.session)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.avatar)
        self.assertEqual(result, mock_user)
        self.assertEqual(self.avatar, result.avatar)

    async def test_confirmed_email(self):

        """
        The test_confirmed_email function tests the confirmed_email function in the users.py file.
        It does this by mocking a user and then patching get_user_by_email to return that mocked user,
        and then calling confirmed email with that mocked user as an argument.

        :param self: Access the attributes of the class
        :return: The value of the user's confirmed attribute
        :doc-author: Trelent
        """
        mock_user = self.user
        self.confirmed = True
        with patch("src.repository.users.get_user_by_email", return_value=mock_user):
            await confirmed_email(mock_user, db=self.session)
        self.assertIsNotNone(mock_user.confirmed)
        self.assertIs(mock_user.confirmed, True)
