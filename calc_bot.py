from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

bot = Bot(token='')
updater = Updater(token='')
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
        '-' для вычитания, '*' для умножения, '/' для деления и '^' для возведения в степень.\
        Дробную часть отделяйте точкой. Если в выражении есть скобки, следите, чтобы количество открывающих\
        и закрывающих скобок совпадало")
    else:
        context.bot.send_message(update.effective_chat.id, "Введите арифметическое выражение")

def parse_string(update, context):
    string = update.message.text
    if string.count('(') != string.count(')'):
        answer = 'Выражение записано с ошибкой, пропущена скобка или записана лишняя'
        context.bot.send_message(update.effective_chat.id, f'{update.message.text} {answer}')
        loger(update.message.text, answer, update)
    else:
        for symbol in string:
                substring = ''
                if symbol == ')':
                    ind_close = string.index(symbol)
                    ind_open = ind_close - 1
                    while string[ind_open] != '(':
                        substring = string[ind_open] + substring
                        ind_open -= 1
                    string = string[:ind_open] + str(calc(substring)) + string[ind_close + 1:]
        answer = calc(string)
        loger(update.message.text, answer, update)
        context.bot.send_message(update.effective_chat.id, f'{update.message.text} = {answer}')


def calc(string):
    result = []
    digit = ""
    for i in range(len(string)):
        if string[i].isdigit() or string[i] == '.':
            digit += string[i]
        elif string[i] == '-' and i == 0:
            digit += string[i]
        elif string[i] == ' ':
            continue
        else:
            result.append(float(digit))
            digit = ""
            result.append(string[i]) 
    else:
        if digit:
            result.append(float(digit))
    return calculate(result)
    

def calculate(lst):
    result = 0
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
dispatcher.add_handler(MessageHandler(Filters.text, parse_string))
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
updater.idle()