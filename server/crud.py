from sqlalchemy.orm import Session

import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def create_message(db: Session, message: schemas.Message, sender_id: int):
    print('i dey reach here')
    db_message = models.Message(text=message.text, sender_id=sender_id)
    print('I dey reach here')
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

def get_user_by_name(db: Session, name:str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_messages(db: Session):
    return db.query(models.Message).all()