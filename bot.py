# https://qna.habr.com/q/1109886?ysclid=mezvbq8wb5746999833
import telebot

botToken = '8179914884:AAHqB-ZoN6unHW92RQVXN-FZsqKlcB8qG1s'
scrapBot = telebot.TeleBot(botToken)
botUsersId = ['5113044686']

def sendNotification(userId: str, trackedList: list):
    outputMessage = 'Tracked items are in stock: '
    for itemName in trackedList:
        outputMessage = outputMessage + '\n' + itemName
    scrapBot.send_message(userId, outputMessage)

def sendNotificationExtanded(userIf: str, extandedTrackedList: dict):
    pass