from fastapi import WebSocket, WebSocketException

connections = []

async def connect(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

async def disconnect(websocket: WebSocket):
    if websocket in connections:
        connections.remove(websocket)

async def sendInfoToAllConnections(info: dict):
    print('Кол-во подключений:', len(connections))
    if len(connections) > 0:
        for connection in connections:
            print(f'Sending info to {connection}')
            try:
                await connection.send_json(info)
            except WebSocketException:
                await disconnect(connection)
