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

# Create a geocoder instance
geolocator = GoogleV3(api_key=GOOGLE_MAPS_API_KEY)

# Dictionary to store user locations
user_locations = {}

# List of attractions
attractions = [
    {
        "name": "Байтерек",
        "address": "Бульвар Нуржол, 14",
        "contacts": "+7 (7172) 44‒64‒72",
        "working_hours": "10:00 – 21:00 (lunch time 13:00-13:30)",
        "ticket_price": "Adult: 700 KZT, child(5-15): 300 KZT",
        "accessibility": "Пандусы, обозначения для слабозрячих",
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
        "ticket_price": "бесплатно",
        "accessibility": "Пандус, Уборная для маломобильных людей",
        "photo": "https://astana.citypass.kz/wp-content/uploads/%D1%85%D0%B0%D0%BD%D1%88%D0%B0%D1%82%D1%8B%D1%80.jpg"
    },
    {
        "name": "Свято-Успенский кафедральный собор",
        "address": "Улица Куйши Дина, 27",
        "contacts": "+7 708 425 14 90",
        "working_hours": "10:00-17:00",
        "ticket_price": "бесплатно",
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
        "name": "Центральный государственный музей Республики Казахстан",
        "address": "мкр. Самал-1, 44",
        "contacts": "+7 (7172) 32-06-98",
        "working_hours": "10:00-18:00",
        "ticket_price": "Взрослый - 1000 KZT, студенты и школьники - 500 KZT",
        "accessibility": "Пандусы, специальные экскурсии",
        "photo": "https://almatymuseum.kz/wp-content/uploads/2023/08/cropped-gosmuzey_1.jpg"
    },
    {
        "name": "Экспо-2017",
        "address": "проспект Мангилик Ел, B1",
        "contacts": "+7 (7172) 54-15-66",
        "working_hours": "10:00-20:00",
        "ticket_price": "Взрослый - 2500 KZT, дети - 1500 KZT",
        "accessibility": "Пандусы, лифты",
        "photo": "https://expopark.kz/assets/image/news/na-zakrytie-expo-1529559343.jpg"
    },
    {
        "name": "Центральная городская библиотека им. М. Ауэзова",
        "address": "улица Абылай хана, 4\1",
        "contacts": "+7 (7172) 74-28-92",
        "working_hours": "09:00-20:00",
        "accessibility": "Пандусы, доступные условия",
        "photo": "https://e-history.kz/media/upload/ckimages/%D0%9D%D0%B0%D0%B7%D0%B0%D1%80%D0%B1%D0%B0%D0%B5%D0%B2%20%D1%86%D0%B5%D0%BD%D1%82%D1%80(3).jpg"
    },
    {
        "name": "Казахстанский театр оперы и балета",
        "address": "улица Динмухамед Конаев 1",
        "contacts": "+7 (7172) 70-55-37",
        "accessibility": "Пандусы, специальные зоны для инвалидов",
        "photo": "https://cdn.kazgor.kz/project-gallery/1633928221.png"
    },
]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn = telebot.types.KeyboardButton('Share location', request_location=True)
    markup.add(btn)
    bot.reply_to(message, "Welcome to My Location Bot. Please share your location.", reply_markup=markup)


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
            bot.reply_to(message, "No location data received. Please try again.")
            return
        latitude = message.location.latitude
        longitude = message.location.longitude
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        address = location.address
        user_locations[message.chat.id] = (latitude, longitude)  # Store user location
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn_nearby = telebot.types.KeyboardButton('Find nearby attractions')
        btn_list = telebot.types.KeyboardButton('List of attractions')
        markup.add(btn_nearby, btn_list)
        bot.reply_to(message, f"You are at: {address}. Choose an option below.",
                     reply_markup=markup)
    except GeocoderTimedOut:
        bot.reply_to(message, "The request to the geocoder has timed out. Please try again later.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


def generate_inline_keyboard(latitude, longitude):
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
                continue  # Skip if location data is not available
        callback_data = f"{lat},{lon}"
        keyboard.row(InlineKeyboardButton(f"{attraction['name']}", callback_data=callback_data))
    keyboard.row(
        InlineKeyboardButton('Find nearby attractions', callback_data='find_nearby'),
        InlineKeyboardButton('List of attractions', callback_data='list_attractions')
    )
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "find_nearby":
            latitude, longitude = user_locations[call.message.chat.id]
            bot.send_chat_action(call.message.chat.id, 'typing')
            bot.reply_to(call.message, f"Here are some nearby attractions:")
            attractions_nearby = get_nearby_attractions(latitude, longitude)
            for i, attraction in enumerate(attractions_nearby):
                bot.send_chat_action(call.message.chat.id, 'typing')
                bot.send_message(call.message.chat.id, f"{i + 1}. {attraction['address']}")
        elif call.data == "list_attractions":
            latitude, longitude = user_locations[call.message.chat.id]
            keyboard = generate_inline_keyboard(latitude, longitude)
            bot.send_message(call.message.chat.id, "Choose an attraction:", reply_markup=keyboard)
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
                    bot.send_photo(call.message.chat.id, attraction["photo"])
                    bot.send_message(call.message.chat.id, f"Name: {attraction['name']}\n"
                                                            f"Address: {attraction['address']}\n"
                                                            f"Contacts: {attraction['contacts']}\n"
                                                            f"Working Hours: {attraction['working_hours']}\n"
                                                            f"Ticket Price: {attraction['ticket_price']}\n"
                                                            f"Accessibility: {attraction['accessibility']}")
                    break
    except Exception as e:
        bot.send_message(call.message.chat.id, f"An error occurred: {str(e)}")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text == 'Find nearby attractions':
        try:
            if message.chat.id not in user_locations:
                bot.reply_to(message, "No location data received. Please share your location first.")
                return
            latitude, longitude = user_locations[message.chat.id]
            location = geolocator.reverse((latitude, longitude), exactly_one=True)
            address = location.address
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, f"Here are some nearby attractions at: {address}")
            attractions_nearby = get_nearby_attractions(latitude, longitude)
            for i, attraction in enumerate(attractions_nearby):
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, f"{i + 1}. {attraction['address']}")
        except GeocoderTimedOut:
            bot.reply_to(message, "The request to the geocoder has timed out. Please try again later.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {str(e)}")
    elif message.text == 'List of attractions':
        latitude, longitude = user_locations[message.chat.id]
        keyboard = generate_inline_keyboard(latitude, longitude)
        bot.send_message(message.chat.id, "Choose an attraction:", reply_markup=keyboard)


# Start the bot
bot.polling()