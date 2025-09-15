# https://qna.habr.com/q/1109886?ysclid=mezvbq8wb5746999833
import database
import telebot

botToken = '8179914884:AAHqB-ZoN6unHW92RQVXN-FZsqKlcB8qG1s'
scrapBot = telebot.TeleBot(botToken)

def sendNotification(userId: str, trackedList: list):
    outputMessage = 'Tracked items are in stock: '
    for itemName in trackedList:
        outputMessage = outputMessage + '\n' + itemName
    scrapBot.send_message(userId, outputMessage)

def sendNotificationExtanded(userIf: str, extandedTrackedList: dict):
    pass

if __name__ == "__main__":
    @scrapBot.message_handler(commands=['start'])
    def addUserToDatabase(message):
        userId = message.from_user.id
        if database.userExists(userId):
            database.addUser(userId)
            scrapBot.send_message(userId, "Bot was successfully activated. You'll get notifications!")
        else:
            scrapBot.send_message(userId, "Bot was activated already. You're still getting notifications!")

    scrapBot.polling(none_stop=True)