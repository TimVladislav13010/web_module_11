import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel, UserResponse
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    update_avatar,
    confirmed_email
)


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
        self.user = User(id=1, email="test@test.com")

    async def test_get_user_by_email(self):
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
