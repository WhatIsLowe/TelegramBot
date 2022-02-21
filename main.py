import telebot
from telebot import types
import datetime
import calendar


TOKEN = ''

# Создаем класс пользователя. Здесь будем хранить временные данные
class User:
    name = ""                   # Имя пользователя
    selected_hospital = ''      # Выбранная больница
    registration_day = ''       # Выбранный день регистрации
    registration_time = ''      # Выбранное время регистрации
    phone_number = ''           # Номер телефона
    is_agreed = False           # Согласие на обработку данных


# Словарь больниц. <уникальный ключ>: <название больницы>
HOSPITALS = {
    '1': '1. Поликлиника №5 ГАУЗ "Городская больница №5"',
    '2': '2. ГАУЗ "Госпиталь для ветеранов воин"',
    '3': '3. ГАУЗ "Городская поликлиника №6"',
    '4': '4. ГАУЗ "Городская больница №2"',
    '5': '5. ГАУЗ "Городская поликлиника №7"',
    '6': '6. ГАУЗ "Городская поликлиника №3"',
    '7': '7. ГАУЗ "Городская поликлиника №4"',
}

bot = telebot.TeleBot(TOKEN, parse_mode=None)


# Обрабатывает команду "start"
# @bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == '/start' or message.text == 'Главное меню')
def start_message(message):
    # Создаем словарь с названием начальных кнопок
    labels = {"location": "Узнать, где находятся пункты вакцинации",
              "vaccine": "Записаться на вакцинацию",
              'rules_to': "Правила поведения до вакцинации",
              "rules_after": "Правила поведения после вакцинации"
              }
    # Создаем разметку (markup) для клавиатуры
    markup = types.InlineKeyboardMarkup()
    # При помощи генератора создаем список из кнопок
    # Названия для кнопок берем из словаря labels
    buttons = [types.InlineKeyboardButton(text=labels[id], callback_data=id) for id in labels]
    # При помощи цикла распаковываем список с кнопками и добавляем их в разметку markup
    for button in buttons:
        markup.add(button)
    # Функция отправляет сообщение и прикрепляет клавиатуру с кнопками
    # message.chat.id - получаем id чата, чтобы отправить туда сообщение (без этого работать не будет)
    # Потом идет наше сообщение
    # reply_markup - указываем клавиатуру, которая будет прикреплена к сообщению
    bot.send_message(message.chat.id, "Переход в главное меню...", reply_markup=create_main_menu_button())
    bot.send_message(message.chat.id, "Вы можете:", reply_markup=markup)


# Данная функция выводит информацию о больницах
def hospital_location(chat_id):
    # Создаем список info с данными по больницам
    info = ['''1. Поликлиника №5 ГАУЗ "Городская больница №5" г. Набережные Челны
            423821, г. Набережные Челны, Цветочный бульвар, дом 7/37, блок А
            Пн-Пт 07:00–19:30; Сб 08:00–18:00
            https://zdrav.tatar.ru/ws0204/section/about''',

            '''2. ГАУЗ «Госпиталь для ветеранов воин» г. Набережные Челны
            423802, Республика Татарстан, г. Набережные Челны, Набережная им. Габдуллы Тукая, дом 39
            Пн-Сб 07:00–19:00
            http://gospital-16.ru/''',

            '''3. ГАУЗ "Городская поликлиника №6" г. Набережные Челны
            423812, Республика Татарстан, г. Набережные Челны, пр. Мира, д. 8
            Пн-Пт 07:00–19:30; Сб 08:00–18:00
            http://gp6nabchelny.ru/''',

            '''4. ГАУЗ "Городская больница №2" г. Набережные Челны
            423810, Республика Татарстан, г. Набережные Челны, пр. Мусы Джалиля, д.19
            Пн-Пт 7:00-19:00 Сб 9:00-14:00
            https://zdrav.tatar.ru/gb2chelny''',

            '''5. ГАУЗ "Городская поликлиника №7"
            423827, Республика Татарстан, г. Набережные Челны, пр. Яшьлек, д. 13, корп. 26/13
            Пн-Пт 07:00-19:00 Сб 8:00-13:00
            https://zdrav.tatar.ru/pol7chelny/about''',

            '''6. ГАУЗ "Городская поликлиника №3" г. Набережные Челны
            423810 Республика Татарстан, г. Набережные Челны, проспект Московский, д.155
            Пн-Пт 07:00–19:00; Сб 08:00–16:00
            https://zdrav.tatar.ru/gp3/about''',

            '''7. ГАУЗ "Городская поликлиника №4" г. Набережные Челны
            423803, Республика Татарстан, г. Набережные Челны, проспект Набережночелнинский, дом 16А
            Пн-Пт 07:00–19:00; Сб 08:00–14:00; Вс 08:00–13:00
            https://zdrav.tatar.ru/pol4chelny/section/new''']

    # Перебираем список больниц и выводим на экран отдельными сообщениями
    for hospital in info:
        bot.send_message(chat_id, hospital)


def hospital_selection(message):
    """ Функция создает клавиатуру с больницами """
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text=HOSPITALS[id], callback_data=f"hospital;{id}") for id in HOSPITALS]
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите больницу: ", reply_markup=markup)


def send_mail(data: User, chat_id):
    """ Функция отпраления письма на почту """
    from modules.mail import EMail
    try:
        EMail(data.name, data.selected_hospital, data.registration_day, data.registration_time, data.phone_number,
              data.is_agreed).send_email()
        bot.send_message(chat_id, "Вы успешно зарегистрировались на вакцинацию")

    except Exception as e:
        bot.send_message(chat_id, "Что-то пошло не так :(")
        bot.send_message(chat_id, e)


def create_callback_data(action, year, month, day):
    """ Создает ассоциации callback для дней месяца """
    data = ";".join([action, str(day), str(month), str(year)])
    return data


def separate_callback_data(data):
    """ Разделяет callback на день, месяц, год """
    data = data.split(";")
    day, month, year = data[1], data[2], data[3]
    return (day, month, year)


def create_calendar(year=None, month=None):
    """
    Создает календарь для выбора даты записи
    """
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    # Первая строчка - Месяц и год
    row = []
    row.append(types.InlineKeyboardButton(calendar.month_name[month] + " " + str(year), callback_data=data_ignore))
    keyboard.append(row)
    # Вторая строчка - Дни недели
    row = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        row.append(types.InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.append(row)
    # Дни месяца
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if (day == 0):
                row.append(types.InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                row.append(
                    types.InlineKeyboardButton(str(day), callback_data=create_callback_data("DAY", year, month, day)))
        keyboard.append(row)
    # Кнопки переключения месяца
    row = []
    last_row_button_lables = ["ПРЕД. МЕСЯЦ", " ", "СЛЕД. МЕСЯЦ"]
    last_row_button_callback = ["PREV_MONTH", "IGNORE", "NEXT_MONTH"]
    for label, callback in zip(last_row_button_lables, last_row_button_callback):
        row.append(types.InlineKeyboardButton(text=label, callback_data=f"{callback}:{year}:{month}"))
    keyboard.append(row)

    return types.InlineKeyboardMarkup(keyboard)


def day_selection(chat_id):
    """ Вызывает функцию создания календаря """
    bot.send_message(chat_id, "Выберите день:", reply_markup=create_calendar())


def time_selection(chat_id):
    """ Позволяет выбрать время """
    time_list = ["10:00", '10:30', '11:00', '11:30', '12:00', '12:30', '15:00', '17:00']
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text=time, callback_data=f'TIME;{time}') for time in time_list]
    for button in buttons:
        markup.add(button)
    bot.send_message(chat_id, "Выберите время:", reply_markup=markup)


@bot.callback_query_handler(func=lambda update: True)  # функция лямбда просто должна здесь быть)))
def callback_handler(callback):
    """ Функция обрабатывает нажатия на кнопки """
    # Обработка нажатия на кнопку в главном меню
    if callback.data == 'location':
        hospital_location(callback.message.chat.id)  # Вызывает функцию, выводящую инфо по больницам
    if callback.data == 'vaccine':
        hospital_selection(callback.message)  # Вызывает функцию, позволяющую зарегистрироваться на вакцинацию
    if callback.data == 'rules_to':
        print_rules(callback.message.chat.id, 'rules_to.txt')
    if callback.data == 'rules_after':
        print_rules(callback.message.chat.id, 'rules_after.txt')

    # Выбор больницы для регистрации
    if "hospital" in callback.data:
        User.selected_hospital = HOSPITALS[callback.data.split(";")[1]]
        day_selection(callback.message.chat.id)

    # Выбор дня месяца
    if "DAY" in callback.data:
        day = callback.data.replace('DAY;', '')
        day = day.replace(';', '.')
        User.registration_day = day
        time_selection(callback.message.chat.id)

    # Выбор времени
    if "TIME" in callback.data:
        User.registration_time = callback.data.replace("TIME;", '')
        msg = bot.send_message(callback.message.chat.id, "Введите ваше имя и фамилию:")
        bot.register_next_step_handler(msg, get_name)

    # Переключение месяца
    if "PREV_MONTH" in callback.data:  # Если нажата кнопка "предыдущий месяц"
        _, year, month = callback.data.split(":")
        current_date = datetime.datetime(int(year), int(month), 1)
        previous_date = current_date - datetime.timedelta(days=1)
        bot.edit_message_text(text=callback.message.text,
                              chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              reply_markup=create_calendar(previous_date.year, previous_date.month))
    if "NEXT_MONTH" in callback.data:  # Если нажата кнопка "следующий месяц"
        _, year, month = callback.data.split(":")
        current_date = datetime.datetime(int(year), int(month), 1)
        next_date = current_date + datetime.timedelta(days=31)
        bot.edit_message_text(text=callback.message.text,
                              chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              reply_markup=create_calendar(next_date.year, next_date.month))


def get_name(message):
    """ Получает имя пользователя """
    if message.text == 'Главное меню':
        msg = bot.send_message(message.chat.id, "Отмена")
        bot.clear_step_handler(msg)
        start_message(message)
        return
    if message.text != '':  # Если пользователь отправил свое имя
        User.name = message.text    # Записываем имя в класс User
        msg = bot.send_message(message.chat.id, "Введите ваш номер телефона:")  # Составляем сообщение о вводе номера телефона
        bot.register_next_step_handler(msg, get_phone_number)   # Вызываем функцию, принимающую номер телефона
    else:       # Если строка пуста
        msg = bot.send_message(message.chat.id, "Строка имени пуста. Напишите ваше имя и фамилию")  # Создаем сообщение
        bot.register_next_step_handler(msg, get_name)   # Просим пользователя ввести имя


def get_phone_number(message):
    """ Принимает номер телефона """
    if message.text == 'Главное меню':
        msg = bot.send_message(message.chat.id, "Отмена")
        bot.clear_step_handler(msg)
        start_message(message)
        return
    if message.text != '':
        User.phone_number = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        agree_button = types.KeyboardButton("Да")
        reject_button = types.KeyboardButton("Нет")
        markup.add(agree_button)
        markup.add(reject_button)
        msg = bot.send_message(message.chat.id, """
            Примите условия соглашения на обработку персональных данных
            Напишите "да" - если согласны
            Или "нет" - если не согласны
        """, reply_markup=markup)
        bot.register_next_step_handler(msg, terms)
    else:
        # Если строка пуста - то, просим человека заново ввести номер телефона
        msg = bot.send_message(message.chat.id, "Строка номера телефона пуста. Пожалуйста, введите номер телефона.")
        bot.register_next_step_handler(msg, get_phone_number)


def terms(message):
    """ Принимает согласие на обработку данных """
    if message.text.lower() == "да":    # Если пользователь ответил "да"
        User.is_agreed = True           # Указываем что он согласен
        send_mail(User, message.chat.id)    # Отправляем письмо на почту
        start_message(message)

    elif message.text.lower() == "нет":     # Если пользователь ответил "нет"
        User.is_agreed = False              # Указываем что согласие не получено
        msg = bot.send_message(message.chat.id, "Согласие на обработку данных не было получено. Отмена")    # Создаем сообщение
        bot.clear_step_handler(msg)         # Отправляем это сообщение пользователю и отменяем
        start_message(message)

    else:                                   # Если ответ ни "да", ни "нет"
        msg = bot.send_message(message.chat.id, "Не понятно... Повторите еще раз")  # Просим пользователя повторить
        bot.register_next_step_handler(msg, terms)  # Отправляем сообщение


def print_rules(chat_id, file_name):
    """ Выводит на экран правила из файла """
    """ Название файла получает из обработчика нажатий на кнопку """
    with open(file_name, 'r', encoding='utf-8') as file:    # Открываем файл с атрибутом 'r' - значит, только на чтение
        rules = file.readlines()    # При помощи метода readlines (Считывает текст из файла построчно и возвращает список)
                                    # С элементами. Где элемент - одна строка. Например, [1 строка, 2 строка, ...]

    for rule in rules:              # Перебираем каждый элемент полученного списка rules
        bot.send_message(chat_id, rule)     # И отправляем по одной строке в сообщении


def create_main_menu_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.KeyboardButton(text="Главное меню")
    keyboard.add(main_menu_button)
    return keyboard

# Заставляет бот работать :)
bot.infinity_polling()
