# https://dev.to/bobbyiliev/how-to-use-server-sent-events-sse-with-fastapi-52fo?ysclid=mffmhabjyh569174755
from parser import getAllItemsInfo
import websocketManager
import asyncEventHandler
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

events = ['infoUpdated']
updateInterval = 30
infoUpdationTask = None
cachedInfo = {}

# Updates info every UpdationInterval seconds
async def infoUpdater():
    global cachedInfo
    while True:
        cachedInfo = getAllItemsInfo()  # bottleneck
        await asyncEventHandler.emitEvent('infoUpdated', cachedInfo)
        print(cachedInfo)
        await asyncio.sleep(updateInterval)

# Sets code, that should be executed before the application starts up and shuts down
@asynccontextmanager
async def lifespan(app: FastAPI):
    global infoUpdationTask
    global cachedInfo
    for event in events:
        asyncEventHandler.addEvent(event)
    asyncEventHandler.subscribeToEvent('infoUpdated', websocketManager.sendInfoToAllConnections)
    cachedInfo = getAllItemsInfo()
    infoUpdationTask = asyncio.create_task(infoUpdater())
    yield
    if infoUpdationTask:
        infoUpdationTask.cancel()

app = FastAPI(lifespan=lifespan)

@app.get('/itemsinfo')
async def sendItemsInfo(url: str = None):
    if url:
        return cachedInfo[url]
    return cachedInfo

@app.websocket('/updatessubcription')
async def subscription(websocket: WebSocket):
    await websocketManager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await websocketManager.disconnect(websocket)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
