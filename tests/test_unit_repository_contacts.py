import unittest
import datetime

from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from sqlalchemy import and_

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
        self.session.query().filter().limit().offset().all.return_value = self.user.contacts
        result = await get_contacts(limit=10, offset=0, user=self.user, db=self.session)
        self.assertEqual(result, self.user.contacts)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    async def test_get_contact_by_id(self):
        self.session.query().filter().first.return_value = self.user.contacts[0]
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result, self.user.contacts[0])
        self.assertEqual(result.id, 1)

    async def test_create(self):
        new_cont = self.new_contact

        result = await create(body=new_cont, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(new_cont.first_name, "test_first")
        self.assertEqual(new_cont.last_name, "test_last")
        self.assertEqual(new_cont.email, "example@example.com")
        self.assertEqual(new_cont.phone_number, "+380687770001")
        self.assertEqual(new_cont.description, "12345678910")

    async def test_update(self):
        mock_contact = self.first_contact
        with patch("src.repository.contacts.get_contact_by_id", return_value=mock_contact):
            result = await update(contact_id=mock_contact, body=self.new_contact, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result, mock_contact)
        self.assertIsNotNone(result)