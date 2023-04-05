from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(db: Session, first_name: str = None, last_name: str = None, email: str = None):
    if first_name and last_name and email:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize(),
                                        Contact.last_name == last_name.capitalize(),
                                        Contact.email == email.lower()
                                        ).first()
    elif first_name and last_name:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize(),
                                        Contact.last_name == last_name.capitalize()
                                        ).first()
    elif last_name and email:
        return db.query(Contact).filter(Contact.last_name == last_name.capitalize(),
                                        Contact.email == email.lower()
                                        ).first()
    elif first_name and email:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize(),
                                        Contact.email == email.lower()
                                        ).first()
    elif first_name:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize()).first()
    elif last_name:
        return db.query(Contact).filter(Contact.last_name == last_name.capitalize()).first()
    elif email:
        return db.query(Contact).filter(Contact.email == email.lower()).first()

    return None
