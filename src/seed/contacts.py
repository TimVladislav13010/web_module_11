from faker import Faker
from random import choice

from src.services.auth import Auth
from src.database.db import DBSession
from src.database.models import Contact, User

auth = Auth()
fake = Faker()
session = DBSession()
quantity_user = 10
user_password = "123456"
quantity_contact = 10000


def create_contact_person(quantity):
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
    for _ in range(quantity):
        contact = User(
            username=fake.first_name(),
            email=fake.ascii_free_email(),
            password=auth.get_password_hash(user_password)
        )
        session.add(contact)
    session.commit()


def main():
    create_user(quantity_user)
    create_contact_person(quantity_contact)


if __name__ == '__main__':
    main()
