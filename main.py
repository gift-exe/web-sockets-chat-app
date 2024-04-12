from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, websocket: WebSocket):

        for connection in self.active_connections:
            if (connection == websocket):
                continue
            await connection.send_text(message)

cm = ConnectionManager()

@app.get('/')
def read_index():
    return {'message':'api online'}

@app.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    #accept connections
    await cm.connect(websocket)

    try:
        while True: 
            data = await websocket.receive_text()
            await cm.send_personal_message(f'You: {data}', websocket)
            await cm.broadcast(f'Client #{client_id}: {data}', websocket)
    except:
        cm.disconnect(websocket)
        await cm.broadcast(f'Client #{client_id} left the chat', websocket)
