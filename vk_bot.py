import bs4 as bs4
import requests
import time
import COVID19Py

class VkBot:

    def __init__(self, user_id):
        print("\nСоздан объект бота!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f'Привет-привет, {self._USERNAME}!\nЯ ещё развиваюсь, пока могу показать погоду.\nНапиши мне "Погода Тюмень", если хочешь узнать прогноз погоды на сегодня.\nДругие команды: Время, Коронавирус'
        # Погода по городу(ex. погода тюмень)
        elif ((message.upper()).split(' '))[0] == self._COMMANDS[1]:
            return self._get_weather(((message.upper()).split(' '))[1])

        # Время
        elif message.upper() == self._COMMANDS[2]:
            return self._get_time()

        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"

        elif message.upper() == 'КОРОНАВИРУС':
            covid19 = COVID19Py.COVID19()
            location = covid19.getLatest()
            return f"Данные по всему миру:\nЗаболевших: {location['confirmed']:,}\nСметрей: {location['deaths']:,}"
        else:
            return "Не понимаю о чем вы..."

    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

    @staticmethod
    def _get_weather(city):

        url = f'http://wttr.in/{city}?format=2'
        response = requests.get(url)  # выполните HTTP-запрос
        return response.text

    def _covid():
        return f'korona'