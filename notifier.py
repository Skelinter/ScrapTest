import parser
import bot
from time import sleep

timeBetweenNotifications = 180  # In seconds
trackedItems = [
    'Terrifying Trove Case',
]
usersId = bot.botUsersId
while True:
    availableItems = parser.checkCertainItems(trackedItems)
    if len(availableItems) != 0:
        for id_ in usersId:
            bot.sendNotification(id_, availableItems)
    sleep(timeBetweenNotifications)