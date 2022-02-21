import smtplib


class EMail:
    _HOST = 'smtp.gmail.com'    # Гугловский адрес хоста
    _TO = 'leisan02bk.ru@gmail.com'  # Адрес эл почты получателя
    _FROM = 'novikov.vlad1999@gmail.com'    # Адрес эл почты отправителя
    _SUBJECT = 'Test EMail'     # Заголовок письма
    text = ''   # Текст письма. Менять не нужно. Формируется при отправке запроса

    def __init__(self, name, hospital, date, time, phone_number, is_agreed):
        self.text = f"Регистрация пользователя {name} в {hospital} на {date} время: {time}\n" \
                    f"Номер телефона: {phone_number}\n" \
                    f"Согласие на обработку данных {is_agreed}"

    def send_email(self):
        # Формируем тело нашего письма
        body = "\r\n".join((
            "От: %s" % self._FROM,
            "Кому: %s" % self._TO,
            "Заголовок: %s" % self._SUBJECT,
            "",
            self.text
        )).encode('utf-8')

        try:
            server = smtplib.SMTP_SSL(self._HOST, 465)
            server.ehlo()
            server.login('novikov.vlad1999@gmail.com', "AAAHULKMAN2705071206hulkmanaaa")
            server.sendmail(self._FROM, [self._TO], body)
            server.close()

            print("Письмо отправлено!")

        except Exception as e:
            print("Что-то пошло по пизде")
            print(e)

