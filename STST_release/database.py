# https://translated.turbopages.org/proxy_u/en-ru.ru.ed4ed3cb-68b6dc36-02d5b8c9-74722d776562/https/stackoverflow.com/questions/3070384/how-to-store-a-list-in-a-column-of-a-database-table
# Should rewrite this code using mongodm, document-oriented approach is much better here to save more disk space
import sqlite3
import types

databaseName = 'users.db'
databaseColumns = ('userId', 'itemsTableId', 'trackingActive', 'items')

def createMainDatabase(fileName: str):
    connection = sqlite3.connect(fileName)
    cursor = connection.cursor()
    try:
        cursor.execute('''
            CREATE TABLE users(userId TEXT UNIQUE, itemsTableId INTEGER UNIQUE, trackingActive INTEGER, PRIMARY KEY(userId))
        ''')
    except sqlite3.OperationalError:
        pass
    connection.close()

def userExists(userId: str) -> bool:
    result = False
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()
    cursor.execute(f'SELECT EXISTS(SELECT 1 FROM users WHERE userId == {userId})')
    if cursor.fetchone()[0] == 1:
        result = True
    connection.close()
    return result

def itemExists(itemTableId: int, itemName: str) -> bool:
    result = False
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()
    cursor.execute(f"SELECT EXISTS(SELECT 1 FROM items{itemTableId} WHERE name == '{itemName}')")
    if cursor.fetchone()[0] == 1:
        result = True
    connection.close()
    return result

def calculateItemsTableId() -> int:
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()
    cursor.execute('SELECT itemsTableId FROM users ORDER BY itemsTableId DESC')
    id_ = cursor.fetchone()[0]
    connection.close()
    return id_

def createItemsTable(itemsTableId: int):
    connection = sqlite3.connect(databaseName)
    connection.execute(f'CREATE TABLE items{itemsTableId}(name TEXT)')
    connection.close()

def addUser(userId: str):
    if not userExists(userId):
        newItemsTableId = calculateItemsTableId() + 1
        createItemsTable(newItemsTableId)
        connection = sqlite3.connect(databaseName)
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO users VALUES ({userId}, {newItemsTableId}, 1)')
        connection.commit()
        connection.close()
    else:
        pass

def getUserData(userId: str, *, columns: list = None) -> dict:
    validRequest = True
    partial = False
    userData = {}
    if columns is not None:
        partial = True
        for column in columns:
            if column not in databaseColumns:
                validRequest = False
                break
        if len(columns) == 0:
            validRequest = False
    if validRequest:
        connection = sqlite3.connect(databaseName)
        cursor = connection.cursor()
        if (not partial) or ('items' in columns):
            items = []
            cursor.execute(f'SELECT itemsTableId FROM users WHERE userId == {userId}')
            itemsTableId = cursor.fetchone()[0]
            cursor.execute(f'SELECT name FROM items{itemsTableId}')
            for item in cursor:
                items.append(item[0])
            userData['items'] = items
        if partial:
            for column in columns:
                if column == 'items':
                    continue
                cursor.execute(f'SELECT {column} FROM users WHERE userID == {userId}')
                userData[column] = cursor.fetchone()[0]
        else:
            cursor.execute(f'SELECT * FROM users WHERE userID == {userId}')
            i = 0
            for value in cursor.fetchone():
                columnName = cursor.description[i][0]
                userData[columnName] = value
                i = i + 1
        connection.close()
        return userData

def changeUserData(userId: str, *, itemsTableId: int = None, trackingActive: bool = None, items: list = None, itemsAction: str = None):
    validRequest = False
    args = locals()
    for arg in list(args.items())[1:-1]:
        if (not isinstance(arg[1], types.NoneType)) and ((args['items'] is not None or args['itemsAction'] is not None) == (not isinstance(args['items'], types.NoneType)) == (not isinstance(args['itemsAction'], types.NoneType))):
            validRequest = True
            break
    if validRequest:
        connection = sqlite3.connect(databaseName)
        cursor = connection.cursor()
        for value in list(args.items())[1:-1]:
            if value[0] == "itemsAction":
                continue
            elif value[0] == 'items' and value[1] is not None:
                itemsTableId = getUserData(userId, columns=['itemsTableId'])['itemsTableId']
                if itemsAction == "add":
                    for item in value[1]:
                        if not itemExists(itemsTableId, item):
                            print('not exists, adding')
                            cursor.execute(f"INSERT INTO items{itemsTableId} (name) VALUES ('{item}')")
                elif itemsAction == 'delete':
                    for item in value[1]:
                        if itemExists(itemsTableId, item):
                            print('exists, deleting')
                            cursor.execute(f"DELETE FROM items{itemsTableId} WHERE name == '{item}'")
            elif value[0] != 'items' and value[1] is not None:
                cursor.execute(f'UPDATE users SET {value[0]} = {value[1]} WHERE userId = {userId}')
                connection.commit()
        connection.commit()
        connection.close()

def applyFunctionToAllUsers():
    pass


