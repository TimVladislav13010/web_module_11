from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


"""
Asynchronous functions for interaction with the database with the contact table.
"""


async def get_contacts(limit: int, offset: int, user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip
    :param user: User: Get the user's id and pass it to the query
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    """
    The get_contact_by_id function takes in a contact_id and user, and returns the contact with that id.
        Args:
            contact_id (int): The id of the desired Contact object.
            user (User): The User object associated with this request.

    :param contact_id: int: Specify the id of the contact to be returned
    :param user: User: Get the user's id
    :param db: Session: Pass the database session to the function
    :return: A contact object from the database
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def create(body: ContactModel, user: User, db: Session):
    """
    The create function creates a new contact in the database.


    :param body: ContactModel: Pass the contact information to be added to the database
    :param user: User: Get the user id of the logged in user
    :param db: Session: Access the database
    :return: The contact object that was created
    :doc-author: Trelent
    """
    contact = Contact(**body.dict(), user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session):
    """
    The update function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified user.

    :param contact_id: int: Identify the contact to be deleted
    :param body: ContactModel: Get the data from the request body
    :param user: User: Ensure that the user is logged in and has access to this endpoint
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session):
    """
    The remove function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact.
            db (Session): A connection to our database, used for querying and updating data.

    :param contact_id: int: Specify the id of the contact to be removed
    :param user: User: Get the user's id
    :param db: Session: Connect to the database
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(user: User, db: Session, first_name: str = None, last_name: str = None, email: str = None):
    """
    The search_contacts function searches the database for contacts that match the search criteria.
        The function takes in a user, db session, and optional first_name, last_name and email parameters.
        If all three are provided it will return any contact with matching first name, last name and email address.
        If only two are provided it will return any contact with matching first or last names (depending on which two were
            passed) as well as an email address if one was passed.  It also checks to make sure that the user id of each
            returned contact matches the id of the logged in user.

    :param user: User: Get the user_id from the token
    :param db: Session: Pass the database session to the function
    :param first_name: str: Filter the contacts by first name
    :param last_name: str: Filter the contacts by last name
    :param email: str: Filter the contacts by email
    :return: A list of contacts that match the search criteria
    :doc-author: Trelent
    """
    if first_name and last_name and email:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize(),
                                        Contact.last_name == last_name.capitalize(),
                                        Contact.email == email.lower(),
                                        Contact.user_id == user.id
                                        ).all()
    elif first_name and last_name:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize(),
                                        Contact.last_name == last_name.capitalize(),
                                        Contact.user_id == user.id
                                        ).all()
    elif last_name and email:
        return db.query(Contact).filter(Contact.last_name == last_name.capitalize(),
                                        Contact.email == email.lower(),
                                        Contact.user_id == user.id
                                        ).all()
    elif first_name and email:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize(),
                                        Contact.email == email.lower(),
                                        Contact.user_id == user.id
                                        ).all()
    elif first_name:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize(), Contact.user_id == user.id).all()
    elif last_name:
        return db.query(Contact).filter(Contact.last_name == last_name.capitalize(), Contact.user_id == user.id).all()
    elif email:
        return db.query(Contact).filter(Contact.email == email.lower(), Contact.user_id == user.id).all()

    return None


async def birthday_contacts(user: User, db: Session):
    """
    The birthday_contacts function returns a list of contacts that have birthdays within the next 7 days.
        Args:
            user (User): The User object to get birthday contacts for.
            db (Session): A database session to use when querying the database.

    :param user: User: Pass in the user object
    :param db: Session: Access the database
    :return: A list of contacts that have a birthday in the next 7 days
    :doc-author: Trelent
    """
    result = list()
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()

    day_one = datetime.today().strftime("%m-%d")

    day_two = datetime.today() + timedelta(days=1)
    day_two = day_two.strftime("%m-%d")

    day_three = datetime.today() + timedelta(days=2)
    day_three = day_three.strftime("%m-%d")

    day_four = datetime.today() + timedelta(days=3)
    day_four = day_four.strftime("%m-%d")

    day_five = datetime.today() + timedelta(days=4)
    day_five = day_five.strftime("%m-%d")

    day_six = datetime.today() + timedelta(days=5)
    day_six = day_six.strftime("%m-%d")

    day_seven = datetime.today() + timedelta(days=6)
    day_seven = day_seven.strftime("%m-%d")

    for contact in contacts:
        if day_one in contact.birthday.strftime("%m-%d") or\
            day_two in contact.birthday.strftime("%m-%d") or\
            day_three in contact.birthday.strftime("%m-%d") or\
            day_four in contact.birthday.strftime("%m-%d") or\
            day_five in contact.birthday.strftime("%m-%d") or\
            day_six in contact.birthday.strftime("%m-%d") or\
                day_seven in contact.birthday.strftime("%m-%d"):

            result.append(contact)

    return result
