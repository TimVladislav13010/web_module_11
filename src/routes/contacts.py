from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/contacts", tags=['contacts'])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get("/search", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get)])
async def search_contacts(first_name: str = Query(None),
                          last_name: str = Query(None),
                          email: str = Query(None),
                          current_user: User = Depends(auth_service.get_current_user),
                          db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(current_user, db, first_name, last_name, email)
    return contacts


@router.get("/birthday", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get)])
async def birthday_contacts(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.birthday_contacts(current_user, db)
    return contacts


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get)])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0,
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_get)])
async def get_contact(contact_id: int = Path(ge=1),
                      current_user: User = Depends(auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_operation_create)])
async def create_contact(body: ContactModel,
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    contact = await repository_contacts.create(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_update)])
async def update_contact(body: ContactModel,
                         contact_id: int = Path(ge=1),
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    contact = await repository_contacts.update(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_operation_remove)])
async def remove_contact(contact_id: int = Path(ge=1),
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
