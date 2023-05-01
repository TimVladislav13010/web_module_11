import unittest
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
        self.session = MagicMock(spec=Session)
        self.user = User(id=1,
                         username="test_username",
                         email="test@test.com",
                         password="test_password",
                         refresh_token=None,
                         avatar=None,
                         confirmed=False,
                         contacts=[Contact(), Contact(), Contact()]
                         )

    async def test_get_contacts(self):
        self.session.query().filter().limit().offset().all.return_value = self.user.contacts
        result = await get_contacts(limit=10, offset=0, user=self.user, db=self.session)
        self.assertEqual(result, self.user.contacts)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
