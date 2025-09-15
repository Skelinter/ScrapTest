import sqlite3

databaseName = 'users.db'

def createDatabaseFile(fileName: str):
    connection = sqlite3.connect(fileName)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE data(id, userId, trackedItems, trackingActive)')

def connectToDatabase(fileName: str) -> sqlite3.Connection:
    return sqlite3.connect(fileName)

def addNewUser():
    pass

def getUserData():
    pass

def changeUserData():
    pass

