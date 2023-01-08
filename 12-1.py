from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

bot = Bot(token='5934547319:AAHs2zQ1MiBL1SdrApl-xwKnek_6xd219DU')
updater = Updater(token='5934547319:AAHs2zQ1MiBL1SdrApl-xwKnek_6xd219DU')
dispatcher = updater.dispatcher


def start(update, _):
    keyboard = [[
            InlineKeyboardButton('Как пользоваться❓', callback_data='1')
            ],
        [InlineKeyboardButton('Вычислить значение выражения➕➖✖➗', callback_data='2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите действие: ", reply_markup=reply_markup)
  

def button(update, context):
    query = update.callback_query
    variant = query.data
    query.answer()
    if variant == '1':
        context.bot.send_message(update.effective_chat.id,"Для вычисления значения арифметического выражения\
        введите его в сообщении. В качестве знаков знаков действий используйте '+' для сложения,\
        '-' для вычитания, '*' для умножения, '/' для деления и '^' для возведения в степень")
    else:
        context.bot.send_message(update.effective_chat.id, "Введите арифметическое выражение")


def calc(update, context):
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
    loger(string, answer, update)
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


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, calc))
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
updater.idle()