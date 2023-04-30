from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.services.roles import RoleAccess


"""
Routes contacts.
"""


router = APIRouter(prefix="/contacts", tags=['contacts'])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get("/search", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get),
                                                                           Depends(RateLimiter(times=2, seconds=5))])
async def search_contacts(first_name: str = Query(None),
                          last_name: str = Query(None),
                          email: str = Query(None),
                          current_user: User = Depends(auth_service.get_current_user),
                          db: Session = Depends(get_db)):
    """
    The search_contacts function searches for contacts in the database.

    :param first_name: str: Pass in the first name of a contact
    :param last_name: str: Filter the contacts by last name
    :param email: str: Search for a contact by email address
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_contacts(current_user, db, first_name, last_name, email)
    return contacts


@router.get("/birthday", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get),
                                                                             Depends(RateLimiter(times=2, seconds=5))])
async def birthday_contacts(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The birthday_contacts function returns a list of contacts that have birthdays in the current month.

    :param current_user: User: Get the current user
    :param db: Session: Pass the database session to the function
    :return: A list of contacts with their birthdays in the next 7 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.birthday_contacts(current_user, db)
    return contacts


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get),
                                                                     Depends(RateLimiter(times=2, seconds=5))])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0,
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts.

    :param limit: int: Specify the maximum number of contacts to return
    :param le: Limit the maximum number of contacts that can be returned
    :param offset: int: Set the offset of the query
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(limit, offset, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_get),
                                                                           Depends(RateLimiter(times=2, seconds=5))])
async def get_contact(contact_id: int = Path(ge=1),
                      current_user: User = Depends(auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    """
    The get_contact function is a GET request that returns the contact with the given ID.
    The function takes in an integer as a path parameter, and uses it to query for the contact.
    If no such contact exists, then an HTTP 404 error is returned.

    :param contact_id: int: Get the contact id from the url
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Get a database session
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_operation_create),
                           Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(body: ContactModel,
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.create(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_update),
                                                                           Depends(RateLimiter(times=2, seconds=5))])
async def update_contact(body: ContactModel,
                         contact_id: int = Path(ge=1),
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id, body and current_user as parameters.
        It returns the updated contact if successful.

    :param body: ContactModel: Pass the contact data to the function
    :param contact_id: int: Identify the contact to be deleted
    :param current_user: User: Get the user from the database
    :param db: Session: Pass the database session to the repository
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(allowed_operation_remove),
                             Depends(RateLimiter(times=2, seconds=5))])
async def remove_contact(contact_id: int = Path(ge=1),
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the id of the contact to be removed
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: The removed contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
