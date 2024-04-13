from fastapi import (FastAPI, 
                     Request, 
                     WebSocket,
                     HTTPException,
                     Depends)
from sqlalchemy.orm import Session

import crud, models, schemas
from ws_manager import ConnectionManager
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
cm = ConnectionManager()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def read_index():
    return {'message':'api online'}

@app.post('/signup')
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user.name)

    if db_user:
        raise HTTPException(status_code=400, detail="Name already exists")

    return crud.create_user(db, user)

@app.post('/login')
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user.name)

    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect Logins")
    
    if user.password != db_user.password:
        raise HTTPException(status_code=400, detail="Incorrect Logins")
    
    return db_user

@app.websocket('/ws/{user_id}')
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    #accept connections
    await cm.connect(websocket)

    user = crud.get_user(db, user_id)

    if user is None:
        cm.disconnect(websocket)
        return {'Error': 'User does not exist'}

    try:
        #send past messages
        send_past_messages(db, user.id)

        while True: 

            data = await websocket.receive_text()
            await crud.create_message(db, data, user_id)
            await cm.send_personal_message(f'You: {data}', websocket, db, user_id)
            await cm.broadcast(f'{user.name}: {data}', websocket)
    except:
        cm.disconnect(websocket)
        await cm.broadcast(f'{user.name} left the chat', websocket)

def send_past_messages(db: Session, user_id: int):
    messages = crud.get_messages(db)

    for message in messages:
        if message.sender_id == user_id:
            cm.send_personal_message(f'You: {message.text}')
        else:
            cm.send_personal_message(f'{crud.get_user(db, message.sender_id).name}: {message.text}')
            