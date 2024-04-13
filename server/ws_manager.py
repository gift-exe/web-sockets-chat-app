from fastapi import WebSocket
from typing import List
from sqlalchemy.orm import Session
import crud

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket, db: Session, user_id: int):
        await crud.create_message(db, message, user_id)
        await websocket.send_text(message)

    async def broadcast(self, message: str, websocket: WebSocket):

        for connection in self.active_connections:
            if (connection == websocket):
                continue
            await connection.send_text(message)
