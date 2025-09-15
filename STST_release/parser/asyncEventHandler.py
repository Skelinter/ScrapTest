import asyncio
import typing

handlers = {}

def addEvent(eventName: str):
    if eventName not in handlers:
        handlers[eventName] = []

def deleteEvent(eventName: str):
    if eventName in handlers:
        del handlers[eventName]

def subscribeToEvent(eventName: str, callback: typing.Callable):
    if eventName in handlers:
        handlers[eventName].append(callback)

async def emitEvent(eventName: str, *args, **kwargs):
    if eventName in handlers:
        for handler in handlers[eventName]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    print('Выполняю асинхронную задачу')
                    await handler(*args, **kwargs)
                else:
                    print('Выполняю синхронную задачу')
                    handler(*args, **kwargs)
            except:
                pass
