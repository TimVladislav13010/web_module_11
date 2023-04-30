from faker import Faker
from random import choice

from src.services.auth import Auth
from src.database.db import DBSession
from src.database.models import Contact, User


"""
Seeds for test database.
"""


auth = Auth()
fake = Faker()
session = DBSession()
quantity_user = 10
user_password = "123456"
quantity_contact = 10000


def create_contact_person(quantity):
    """
    The create_contact_person function creates a random number of contact persons.
        The function takes one argument, quantity, which is the number of contacts to be created.
        The function uses the Faker library to generate fake data for each contact person.

    :param quantity: Create a number of contacts
    :return: The number of contacts created
    :doc-author: Trelent
    """
    for _ in range(quantity):
        contact = Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.ascii_free_email(),
            phone_number=fake.phone_number(),
            birthday=fake.date_of_birth(),
            description=fake.name(),
            user_id=choice(range(1, quantity_user + 1))
        )
        session.add(contact)
    session.commit()


def create_user(quantity):
    """
    The create_user function creates a user with the following attributes:
        username = fake.first_name()
        email = fake.ascii_free_email()
        password = auth.get_password_hash(user_password)

    :param quantity: Determine how many users to create
    :return: The number of users created
    :doc-author: Trelent
    """
    for _ in range(quantity):
        contact = User(
            username=fake.first_name(),
            email=fake.ascii_free_email(),
            password=auth.get_password_hash(user_password)
        )
        session.add(contact)
    session.commit()


def main():
    """
    The main function creates a user and contact person.


    :return: Nothing
    :doc-author: Trelent
    """
    create_user(quantity_user)
    create_contact_person(quantity_contact)


if __name__ == '__main__':
    main()
