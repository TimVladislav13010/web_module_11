from datetime import datetime, timedelta

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
                                        ).all()
    elif first_name and last_name:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize(),
                                        Contact.last_name == last_name.capitalize()
                                        ).all()
    elif last_name and email:
        return db.query(Contact).filter(Contact.last_name == last_name.capitalize(),
                                        Contact.email == email.lower()
                                        ).all()
    elif first_name and email:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize(),
                                        Contact.email == email.lower()
                                        ).all()
    elif first_name:
        return db.query(Contact).filter(Contact.first_name == first_name.capitalize()).all()
    elif last_name:
        return db.query(Contact).filter(Contact.last_name == last_name.capitalize()).all()
    elif email:
        return db.query(Contact).filter(Contact.email == email.lower()).all()

    return None


async def birthday_contacts(db: Session):
    result = list()
    contacts = db.query(Contact).all()

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
