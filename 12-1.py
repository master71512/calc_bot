from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot = Bot(token='5934547319:AAHs2zQ1MiBL1SdrApl-xwKnek_6xd219DU')
updater = Updater(token='5934547319:AAHs2zQ1MiBL1SdrApl-xwKnek_6xd219DU')
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(update.effective_chat.id,'Введите /calc и арифметическое выражение для вычисления значения')
    context.bot.send_message(update.effective_chat.id,'Введите /cancel если хотите закончить')


def cancel(update, context):
    context.bot.send_message(update.effective_chat.id,"До свидания!")


def calc(update, context):
    if context.args:
        string = ''.join(context.args)
        result = []
        digit = ""
        for symbol in string:
            if symbol.isdigit() or symbol == '.':
                digit += symbol
            elif symbol == ' ':
                continue
            else:
                result.append(float(digit))
                digit = ""
                result.append(symbol) 
        else:
            if digit:
                result.append(float(digit))
        answer = calculate(result)
        context.bot.send_message(update.effective_chat.id, f'{string} = {answer}')
        loger(result, answer, update)
    else:
        context.bot.send_message(update.effective_chat.id, 'Для вычисления введите /calc и арифметическое выражение в одном сообщении')

def calc2(update, context):
    string = update.message.text
    result = []
    digit = ""
    for symbol in string:
        if symbol.isdigit() or symbol == '.':
            digit += symbol
        elif symbol == ' ':
            continue
        else:
            result.append(float(digit))
            digit = ""
            result.append(symbol) 
    else:
        if digit:
            result.append(float(digit))
    answer = calculate(result)
    context.bot.send_message(update.effective_chat.id, f'{string} = {answer}')

def calculate(lst):
    result = 0.0
    for s in lst:  
        if s == '^':
            index = lst.index(s)
            result = lst[index - 1] ** lst[index + 1]
            lst = lst[:index - 1] + [result] + lst[index + 2:]
    for s in lst:  
        if s == '*' or s == '/':
            if s == '*':
                index = lst.index(s)
                result = lst[index - 1] * lst[index + 1]
                lst = lst[:index - 1] + [result] + lst[index + 2:]
            else:
                index = lst.index(s)
                result = lst[index - 1] / lst[index + 1]
                lst = lst[:index - 1] + [result] + lst[index + 2:]
    for s in lst:  
        if s == '+' or s == '-':
            if s == '+':
                index = lst.index(s)
                result = lst[index - 1] + lst[index + 1]
                lst = lst[:index - 1] + [result] + lst[index + 2:]
            else:
                index = lst.index(s)
                result = lst[index - 1] - lst[index + 1]
                lst = lst[:index - 1] + [result] + lst[index + 2:]
    return result

def loger(primer, result, update):
    with open('file.txt', 'a') as data:
        string = "".join(map(str, primer))
        string += " = "
        result = str(result) + ';\n'
        data.write(str(update.effective_chat.id) + ': ')
        data.write(string)
        data.write(str(result))

start_handler = CommandHandler('start', start)
calc_handler = CommandHandler('calc', calc)
cancel_handler = CommandHandler('cancel', cancel)
calc2_handler = MessageHandler(Filters.text, calc2)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(calc_handler)
dispatcher.add_handler(cancel_handler)
dispatcher.add_handler(calc2_handler)

updater.start_polling()
updater.idle()