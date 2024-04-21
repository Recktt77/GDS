import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderQueryError

# Telegram bot token
TOKEN = '7181446272:AAEpa0zRjH6C3nFbXQFOYz0aJSgraH_YgyI'

# Google Maps API Key
GOOGLE_MAPS_API_KEY = 'AIzaSyCvm9R7PaT8xTSLaRgPY-unEMnv2RVacC8'

# Create a bot instance
bot = telebot.TeleBot(TOKEN)

# Создание экземпляра геокодера
geolocator = GoogleV3(api_key=GOOGLE_MAPS_API_KEY)

# Словарь для хранения местоположений пользователей
user_locations = {}

# Список достопримечательностей
attractions = [
    {
        "name": "Байтерек",
        "address": "Бульвар Нуржол, 14",
        "contacts": "+7 (7172) 44‒64‒72",
        "working_hours": "10:00 – 21:00 (перерыв на обед с 13:00 до 13:30)",
        "ticket_price": "Взрослый: 700 KZT, Дети(5-15): 300 KZT",
        "accessibility": "Пандусы, обозначения для слабовидящих",
        "photo": "https://planetofhotels.com/guide/sites/default/files/styles/paragraph__hero_banner__hb_image__1880bp/public/hero_banner/Baiterek.jpg"
    },
    {
        "name": "Триумфальная арка Мангылык ел",
        "address": "Остановка Триумфальная арка Мангылык ел",
        "contacts": "8 (7172) 55 64 84",
        "working_hours": "Круглосуточно",
        "ticket_price": "Бесплатно",
        "accessibility": "Нет",
        "photo": "https://cdn.hisour.com/cdn-cgi/imagedelivery/PJiouRWxFR9baI5eaOAFCA/www.hisour.com/2022/02/Guide-Tour-of-Arc-de-Triomphe-Paris-France.jpg/w=1200,h=800"
    },
    {
        "name": "Бас мешыт",
        "address": "Проспект Мангилик Ел, 65",
        "contacts": "+7 (7172) 57‒72‒98",
        "working_hours": "06:00 до 21:00",
        "ticket_price": "Бесплатно",
        "accessibility": "Пандус вход для людей с инвалидностью",
        "photo": "https://adyrna.kz/content/uploads/2024/03/bas-meshit-960x500.jpg?token=9bd90858e74d8e87be36556773688d60"
    },
    {
        "name": "Хан-Шатыр",
        "address": "Проспект Туран 37",
        "contacts": "+7 (7172) 57-26-26",
        "working_hours": "10:00-22:00",
        "ticket_price": "Бесплатно",
        "accessibility": "Пандус, Уборная для маломобильных людей",
        "photo": "https://astana.citypass.kz/wp-content/uploads/%D1%85%D0%B0%D0%BD%D1%88%D0%B0%D1%82%D1%8B%D1%80.jpg"
    },
    {
        "name": "Свято-Успенский кафедральный собор",
        "address": "Улица Куйши Дина, 27",
        "contacts": "+7 708 425 14 90",
        "working_hours": "10:00-17:00",
        "ticket_price": "Бесплатно",
        "accessibility": "Пандус, Доступный вход для людей с инвалидностью",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/2/25/%D0%A3%D1%81%D0%BF%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D1%81%D0%BE%D0%B1%D0%BE%D1%80_%D0%90%D1%81%D1%82%D0%B0%D0%BD%D1%8B_%D1%84%D0%BE%D1%82%D0%BE3.jpg"
    },
    {
        "name": "Национальный музей Республики Казахстан",
        "address": "проспект Тауелсиздик, 54",
        "contacts": "+7 (7172) 91-32-93",
        "working_hours": "10:00-18:00",
        "ticket_price": "Взрослый - 2000 KZT, студенты и школьники - 500 KZT",
        "accessibility": "Пандусы, специальные экскурсии для людей с ограниченными возможностями",
        "photo": "https://khabar.kz/media/k2/items/src/066c5462473924b460774ad5c21d3152.jpg"
    },
    {
        "name": "Центральная городская библиотека им. М. Ауэзова",
        "address": "улица Абылай хана, 4/1",
        "contacts": "+7 (7172) 74-28-92",
        "working_hours": "09:00-20:00",
        "ticket_price": "Бесплатно",
        "accessibility": "Пандусы, доступные условия",
        "photo": "https://e-history.kz/media/upload/ckimages/%D0%9D%D0%B0%D0%B7%D0%B0%D1%80%D0%B1%D0%B0%D0%B5%D0%B2%20%D1%86%D0%B5%D0%BD%D1%82%D1%80(3).jpg"
    },
    {
        "name": "Казахстанский театр оперы и балета",
        "address": "улица Динмухамед Конаев 1",
        "contacts": "+7 (7172) 70-55-37",
        "working_hours": "09:00-20:00",
        "ticket_price": "Бесплатно",
        "accessibility": "Пандусы, специальные зоны для инвалидов",
        "photo": "https://cdn.kazgor.kz/project-gallery/1633928221.png"
    },
]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn = telebot.types.KeyboardButton('Поделиться местоположением', request_location=True)
    markup.add(btn)
    bot.reply_to(message, f"Привет, {message.from_user.first_name}! Я твой гид Shyraq по Астане. Пожалуйста, поделись своим местоположением.", reply_markup=markup)


def get_nearby_attractions(latitude, longitude):
    nearby_attractions = []
    try:
        location = (latitude, longitude)
        for attraction in attractions:
            attraction_location = geolocator.geocode(attraction["address"])
            attraction_point = (attraction_location.latitude, attraction_location.longitude)
            distance = geodesic(location, attraction_point).meters
            if distance <= 5000:
                nearby_attractions.append(attraction)
    except GeocoderTimedOut:
        pass
    except Exception as e:
        pass
    return nearby_attractions


@bot.message_handler(func=lambda message: True, content_types=['location'])
def location(message):
    try:
        if message.location is None:
            bot.reply_to(message, "Данные о местоположении не получены. Пожалуйста, попробуйте еще раз.")
            return
        latitude = message.location.latitude
        longitude = message.location.longitude
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        address = location.address
        user_locations[message.chat.id] = (latitude, longitude)  # Сохранение местоположения пользователя
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn_nearby = telebot.types.KeyboardButton('Найти ближайшие достопримечательности')
        btn_list = telebot.types.KeyboardButton('Список достопримечательностей')
        markup.add(btn_nearby, btn_list)
        bot.reply_to(message, f"Вы находитесь здесь: {address}. Выберите действие ниже.",
                     reply_markup=markup)
    except GeocoderTimedOut:
        bot.reply_to(message, "Запрос к геокодеру превысил лимит времени. Пожалуйста, попробуйте позже.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


def generate_inline_keyboard():
    keyboard = InlineKeyboardMarkup()
    for attraction in attractions:
        lat = 0
        lon = 0
        if attraction["address"]:
            try:
                loc = geolocator.geocode(attraction["address"])
                if loc:
                    lat = loc.latitude
                    lon = loc.longitude
            except GeocoderQueryError:
                continue  # Пропустить, если данные о местоположении недоступны
        callback_data = f"{lat},{lon}"
        keyboard.row(InlineKeyboardButton(f"{attraction['name']}", callback_data=callback_data))
    keyboard.row(
        InlineKeyboardButton('Найти ближайшие достопримечательности', callback_data='find_nearby'),
        InlineKeyboardButton('Список достопримечательностей', callback_data='list_attractions')
    )
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "find_nearby":
            latitude, longitude = user_locations[call.message.chat.id]
            bot.send_chat_action(call.message.chat.id, 'typing')
            bot.reply_to(call.message, f"Вот некоторые ближайшие достопримечательности:")
            attractions_nearby = get_nearby_attractions(latitude, longitude)
            if attractions_nearby:
                keyboard = InlineKeyboardMarkup()
                for attraction in attractions_nearby:
                    loc = geolocator.geocode(attraction["address"])
                    if loc:
                        lat = loc.latitude
                        lon = loc.longitude
                    callback_data = f"{lat},{lon}"
                    keyboard.row(InlineKeyboardButton(f"{attraction['name']}", callback_data=callback_data))

                bot.send_message(call.message.chat.id, "Вот ближайшие достопримечательности:", reply_markup=keyboard)
            else:
                bot.send_message(call.message.chat.id, "Рядом не найдено достопримечательностей.")
        elif call.data == "list_attractions":
            latitude, longitude = user_locations[call.message.chat.id]
            keyboard = generate_inline_keyboard()
            bot.send_message(call.message.chat.id, "Выберите достопримечательность:", reply_markup=keyboard)
        else:
            latitude, longitude = call.data.split(",")
            bot.send_location(call.message.chat.id, latitude, longitude)
            for attraction in attractions:
                lat = 0
                lon = 0
                if attraction["address"]:
                    loc = geolocator.geocode(attraction["address"])
                    if loc:
                        lat = loc.latitude
                        lon = loc.longitude
                if f"{lat},{lon}" == call.data:
                    photo = attraction.get("photo", None)
                    if photo:
                        bot.send_photo(call.message.chat.id, photo)
                    bot.send_message(call.message.chat.id, f"Название: {attraction['name']}\n"
                                                            f"Адрес: {attraction['address']}\n"
                                                            f"Контакты: {attraction['contacts']}\n"
                                                            f"Часы работы: {attraction['working_hours']}\n"
                                                            f"Стоимость билета: {attraction['ticket_price']}\n"
                                                            f"Доступность: {attraction['accessibility']}")
                    break
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text == 'Найти ближайшие достопримечательности':
        try:
            if message.chat.id not in user_locations:
                bot.reply_to(message, "Данные о местоположении не получены. Пожалуйста, сначала поделитесь своим местоположением.")
                return
            latitude, longitude = user_locations[message.chat.id]
            location = geolocator.reverse((latitude, longitude), exactly_one=True)
            address = location.address
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, f"Вот некоторые ближайшие достопримечательности по адресу: {address}")
            attractions_nearby = get_nearby_attractions(latitude, longitude)
            if attractions_nearby:
                keyboard = InlineKeyboardMarkup()
                for attraction in attractions_nearby:
                    loc = geolocator.geocode(attraction["address"])
                    if loc:
                        lat = loc.latitude
                        lon = loc.longitude
                    callback_data = f"{lat},{lon}"
                    keyboard.row(InlineKeyboardButton(f"{attraction['name']}", callback_data=callback_data))

                bot.send_message(message.chat.id, "Вот ближайшие достопримечательности:", reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, "Рядом не найдено достопримечательностей.")
        except GeocoderTimedOut:
            bot.reply_to(message, "Запрос к геокодеру превысил лимит времени. Пожалуйста, попробуйте позже.")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {str(e)}")
    elif message.text == 'Список достопримечательностей':
        latitude, longitude = user_locations[message.chat.id]
        keyboard = generate_inline_keyboard()
        bot.send_message(message.chat.id, "Выберите достопримечательность:", reply_markup=keyboard)


# Запуск бота
bot.polling()
