import unittest
import datetime

from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactResponse
from src.repository.contacts import (
    get_contacts,
    get_contact_by_id,
    create,
    update,
    remove,
    search_contacts,
    birthday_contacts
)


"""
Unittest repository contacts.
"""


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new session and adds three contacts to the user's contact list.

        :param self: Represent the instance of the class
        :return: The following:
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.first_contact = Contact(id=1,
                                     first_name="test_name_1",
                                     last_name="test_last_name_1",
                                     email="cont1@test.com",
                                     phone_number="+380687770001",
                                     birthday=datetime.datetime.now(),
                                     description="test_description1",
                                     user_id=1
                                     )

        self.second_contact = Contact(id=2,
                                      first_name="test_name_2",
                                      last_name="test_last_name_2",
                                      email="cont2@test.com",
                                      phone_number="+380687770002",
                                      birthday=datetime.datetime.now(),
                                      description="test_description2",
                                      user_id=1
                                      )

        self.third_contact = Contact(id=3,
                                     first_name="test_name_3",
                                     last_name="test_last_name_3",
                                     email="cont3@test.com",
                                     phone_number="+380687770003",
                                     birthday=datetime.datetime.now(),
                                     description="test_description3",
                                     user_id=1
                                     )

        self.user = User(id=1,
                         username="test_username",
                         email="test@test.com",
                         password="test_password",
                         refresh_token=None,
                         avatar=None,
                         confirmed=False,
                         contacts=[self.first_contact, self.second_contact, self.third_contact]
                         )

        self.new_contact = ContactModel(first_name="test_first",
                                        last_name="test_last",
                                        email="example@example.com",
                                        phone_number="+380687770001",
                                        birthday=datetime.datetime.now(),
                                        description="12345678910")

    async def test_get_contacts(self):
        """
        The test_get_contacts function tests the get_contacts function in the contacts.py file.
        It does this by creating a mock session object, and then mocking out its query method to return a mock query object.
        The filter method of that mock query object is then mocked out to return itself, so that it can be chained with limit and offset methods, which are also mocked out to return themselves so they can be chained with all(). The all() method is finally mocked out to return self.user's contacts attribute (a list of Contact objects). This allows us to test whether or not get_contacts returns what we expect it should: self

        :param self: Access the class attributes and methods
        :return: A list of contacts
        :doc-author: Trelent
        """
        self.session.query().filter().limit().offset().all.return_value = self.user.contacts
        result = await get_contacts(limit=10, offset=0, user=self.user, db=self.session)
        self.assertEqual(result, self.user.contacts)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    async def test_get_contact_by_id_found(self):
        """
        The test_get_contact_by_id_found function tests the get_contact_by_id function when a contact is found.
        It does this by mocking the session and user objects, then returning a Contact object from the mocked query.
        The test asserts that an instance of Contact is returned, that it matches what was returned from the mock query,
        and that its id attribute matches 1.

        :param self: Represent the instance of the class
        :return: The first contact in the user's contacts list
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = self.user.contacts[0]
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result, self.user.contacts[0])
        self.assertEqual(result.id, 1)

    async def test_get_contact_by_id_not_found(self):
        """
        The test_get_contact_by_id_not_found function tests the get_contact_by_id function when a contact is not found.
            The test uses mock to patch the session query method and return None, which simulates a database query that does not find any contacts.
            The test then calls the get_contact_by_id function with an id of 1 and passes in self.user as well as self.session for db access.

        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = None
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create(self):
        """
        The test_create function tests the create function.
            It creates a new contact and checks if it is an instance of Contact class,
            then compares all fields with expected values.

        :param self: Represent the instance of the class
        :return: An instance of the contact class
        :doc-author: Trelent
        """
        new_cont = self.new_contact

        result = await create(body=new_cont, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(new_cont.first_name, "test_first")
        self.assertEqual(new_cont.last_name, "test_last")
        self.assertEqual(new_cont.email, "example@example.com")
        self.assertEqual(new_cont.phone_number, "+380687770001")
        self.assertEqual(new_cont.description, "12345678910")

    async def test_update_found(self):
        """
        The test_update_found function tests the update function in the contacts repository.
        It does this by first mocking a contact object, and then patching get_contact_by_id to return that mock contact.
        Then it calls update with the mocked contact's id, a new Contact object (self.new_contact), and self.user as arguments,
        and stores its result in result variable.

        :param self: Access the attributes and methods of the class in python
        :return: An instance of the contact class
        :doc-author: Trelent
        """
        mock_contact = self.first_contact
        with patch("src.repository.contacts.get_contact_by_id", return_value=mock_contact):
            result = await update(contact_id=mock_contact.id, body=self.new_contact, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result, mock_contact)
        self.assertIsNotNone(result)

    async def test_update_not_found(self):
        """
        The test_update_not_found function tests the update function in the contacts repository.
        It does this by mocking a contact that doesn't exist, and then calling the update function with it.
        The test asserts that None is returned.

        :param self: Access the class attributes and methods
        :return: None
        :doc-author: Trelent
        """
        mock_contact = None
        with patch("src.repository.contacts.get_contact_by_id", return_value=mock_contact):
            result = await update(contact_id=0, body=self.new_contact, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_remove_found(self):
        """
        The test_remove_found function tests the remove function in the repository.contacts module.
        It does this by mocking a contact and then patching get_contact_by_id to return that mock contact.
        The result of calling remove is then checked against the mocked contact.

        :param self: Access the attributes and methods of the class
        :return: The contact that was removed
        :doc-author: Trelent
        """
        mock_contact = self.first_contact
        with patch("src.repository.contacts.get_contact_by_id", return_value=mock_contact):
            result = await remove(contact_id=mock_contact.id, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result, mock_contact)

    async def test_remove_not_found(self):
        """
        The test_remove_not_found function tests the remove function in the contacts.py file.
        The test_remove_not_found function is a coroutine that uses patch to mock get_contact_by_id,
        which returns None when called with contact id 0 and user self.user (a User object). The result of calling
        the remove function with contact id 0 and user self.user is then assigned to result, which is asserted to be None.

        :param self: Access the class attributes and methods
        :return: None
        :doc-author: Trelent
        """
        mock_contact = None
        with patch("src.repository.contacts.get_contact_by_id", return_value=mock_contact):
            result = await remove(contact_id=0, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_contacts_found_FirstName_LastName_Email(self):
        """
        The test_search_contacts_found_FirstName_LastName_Email function tests the search_contacts function.
            The test_search_contacts_found_FirstName_LastName function tests the search contacts functionality when all three parameters are passed in: first name, last name and email address.
            The test asserts that a contact is returned from the database, that there is at least one contact returned from the database and that a list of contacts was returned.

        :param self: Represent the instance of the class
        :return: A list of contacts that match the search criteria
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = [self.user.contacts[0]]
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       first_name="test_name_1",
                                       last_name="test_last_name_1",
                                       email="cont1@test.com")
        self.assertIn(self.user.contacts[0], result)
        self.assertGreater(len(result), 0)
        self.assertTrue(result)

    async def test_search_contacts_not_found_FirstName_LastName_Email(self):
        """
        The test_search_contacts_not_found_FirstName_LastName_Email function tests the search_contacts function with a first name, last name, and email that are not in the database.
        The test asserts that there is less than one contact returned from the search_contacts function and that no contacts were found.

        :param self: Represent the instance of the class
        :return: A list of contacts
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = list()
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       first_name="test_name_1",
                                       last_name="test_last_name_1",
                                       email="cont1@test.com")
        self.assertLess(len(result), 1)
        self.assertFalse(result)

    async def test_search_contacts_found_FirstName_LastName(self):
        """
        The test_search_contacts_found_FirstName_LastName function tests the search_contacts function with a first name and last name.
        The test_search_contacts_found_FirstName function is similar to the test above, but it uses a different contact in the user's contacts list.
        This time, we are testing that if we pass in both a first and last name to search for, then only one contact should be returned.

        :param self: Represent the instance of the class
        :return: A list of contacts
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = [self.user.contacts[0]]
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       first_name="test_name_1",
                                       last_name="test_last_name_1")
        self.assertIn(self.user.contacts[0], result)
        self.assertGreater(len(result), 0)
        self.assertTrue(result)

    async def test_search_contacts_not_found_FirstName_LastName(self):
        """
        The test_search_contacts_not_found_FirstName_LastName function tests the search_contacts function when a user searches for a contact that does not exist.
        The test_search_contacts_not_found function is called to ensure that the search results are empty.

        :param self: Represent the instance of the class
        :return: False
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = list()
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       first_name="test_name_1",
                                       last_name="test_last_name_1")
        self.assertLess(len(result), 1)
        self.assertFalse(result)

    async def test_search_contacts_found_LastName_Email(self):
        """
        The test_search_contacts_found_LastName_Email function tests the search_contacts function with a user,
        a database session, and a last name and email. The test asserts that the first contact in the user's contacts list is in
        the result of calling search_contacts with those parameters. It also asserts that there are more than 0 items in
        result (i.e., it is not empty) and that result itself evaluates to True.

        :param self: Refer to the current object
        :return: A list of contacts
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = [self.user.contacts[0]]
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       last_name="test_last_name_1",
                                       email="cont1@test.com")
        self.assertIn(self.user.contacts[0], result)
        self.assertGreater(len(result), 0)
        self.assertTrue(result)

    async def test_search_contacts_not_found_LastName_Email(self):
        """
        The test_search_contacts_not_found_LastName_Email function tests the search_contacts function with a last name and email that are not in the database.
        The test asserts that there is no result returned from the search_contacts function.

        :param self: Represent the instance of the class
        :return: An empty list
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = list()
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       last_name="test_last_name_1",
                                       email="cont1@test.com")
        self.assertLess(len(result), 1)
        self.assertFalse(result)

    async def test_search_contacts_found_FirstName_Email(self):
        """
        The test_search_contacts_found_FirstName_Email function tests the search_contacts function when a user is found by
        first name and email. The test passes if the contact is returned in a list, and that list has at least one item.

        :param self: Represent the instance of the class
        :return: A list of contacts
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = [self.user.contacts[0]]
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       first_name="test_name_1",
                                       email="cont1@test.com")
        self.assertIn(self.user.contacts[0], result)
        self.assertGreater(len(result), 0)
        self.assertTrue(result)

    async def test_search_contacts_not_found_FirstName_Email(self):
        """
        The test_search_contacts_not_found_FirstName_Email function tests the search_contacts function with a first name and email that do not exist in the database.
        The test asserts that no contacts are returned.

        :param self: Access the attributes and methods of the class in python
        :return: An empty list
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = list()
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       first_name="test_name_1",
                                       email="cont1@test.com")
        self.assertLess(len(result), 1)
        self.assertFalse(result)

    async def test_search_contacts_found_FirstName(self):
        """
        The test_search_contacts_found_FirstName function tests the search_contacts function to see if it can find a contact
        by first name. The test creates a user and adds two contacts to that user's list of contacts. Then, the test calls
        the search_contacts function with the first name of one of those contacts as an argument. If successful, this should
        return only that contact in a list.

        :param self: Represent the instance of the class
        :return: A list of contacts that match the search criteria
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = [self.user.contacts[0]]
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       first_name="test_name_1")
        self.assertIn(self.user.contacts[0], result)
        self.assertGreater(len(result), 0)
        self.assertTrue(result)

    async def test_search_contacts_not_found_FirstName(self):
        """
        The test_search_contacts_not_found_FirstName function tests the search_contacts function to ensure that it returns an empty list when a user searches for a contact with a first name that does not exist in the database.
            Args:
                self (TestSearchContacts): The test case class.

        :param self: Represent the instance of the object that is passed to the method when it is called
        :return: An empty list
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = list()
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       first_name="test_name_1")
        self.assertLess(len(result), 1)
        self.assertFalse(result)

    async def test_search_contacts_found_LastName(self):
        """
        The test_search_contacts_found_LastName function tests the search_contacts function to ensure that it returns a list of contacts
        that match the last name provided. The test is successful if the contact with a matching last name is returned in a list.

        :param self: Represent the instance of the class
        :return: A list of contacts that match the last name
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = [self.user.contacts[0]]
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       last_name="test_last_name_1")
        self.assertIn(self.user.contacts[0], result)
        self.assertGreater(len(result), 0)
        self.assertTrue(result)

    async def test_search_contacts_not_found_LastName(self):
        """
        The test_search_contacts_not_found_LastName function tests the search_contacts function to ensure that it returns an empty list when a user searches for a contact with a last name that does not exist in the database.


        :param self: Represent the instance of the class
        :return: A list of contacts with the last name &quot;test_last_name&quot;
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = list()
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       last_name="test_last_name_1")
        self.assertLess(len(result), 1)
        self.assertFalse(result)

    async def test_search_contacts_found_Email(self):
        """
        The test_search_contacts_found_Email function tests the search_contacts function with a valid email.
        The test_search_contacts_found_Email function is an asynchronous coroutine that uses the pytest-asyncio library to run asynchronously.
        The test asserts that the result of calling search contacts with a valid email returns one contact, and that it is in fact a contact.

        :param self: Represent the instance of the class
        :return: The user's contacts and the length of the result is greater than 0
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = [self.user.contacts[0]]
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       email="cont1@test.com")
        self.assertIn(self.user.contacts[0], result)
        self.assertGreater(len(result), 0)
        self.assertTrue(result)

    async def test_search_contacts_not_found_Email(self):
        """
        The test_search_contacts_not_found_Email function tests the search_contacts function with a non-existent email.
        The test_search_contacts_not_found function is called to create a user and contact list, then the search contacts
        is called with an email that does not exist in the database. The result should be an empty list.

        :param self: Represent the instance of the class
        :return: A list of contacts that match the search criteria
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = list()
        result = await search_contacts(user=self.user,
                                       db=self.session,
                                       email="cont1@test.com")
        self.assertLess(len(result), 1)
        self.assertFalse(result)

    async def test_birthday_contacts_found(self):
        """
        The test_birthday_contacts_found function tests the birthday_contacts function.
        It does this by mocking the session object and setting its query method to return a list of contacts.
        The result is then checked to see if it contains any of the mocked contacts.

        :param self: Access the instance of the class
        :return: True if the result is not empty
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = self.user.contacts
        result = await birthday_contacts(user=self.user, db=self.session)
        self.assertIn(result[0], self.user.contacts)
        self.assertIn(result[1], self.user.contacts)
        self.assertIn(result[2], self.user.contacts)
        self.assertTrue(result)

    async def test_birthday_contacts_not_found(self):
        """
        The test_birthday_contacts_not_found function tests the birthday_contacts function when there are no contacts
        in the database with a birthday on that day. It does this by mocking out the session object and returning an empty list
        when queried for all contacts in the database. The test then asserts that result is False, which it should be if there
        are no birthdays on that day.

        :param self: Represent the instance of the object that is passed to the method when it is called
        :return: False if the query returns an empty list
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = list()
        result = await birthday_contacts(user=self.user, db=self.session)
        self.assertFalse(result)
