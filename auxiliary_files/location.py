#https://vc.ru/dev/156853-telegram-bot-dlya-polucheniya-adresa-po-lokacii-ili-koordinatam-python
#импортируем библиотеку requests
import requests
from geopy.geocoders import Nominatim

#создаем функцию get_address_from_coords с параметром coords, куда мы будем посылать координаты и получать готовый адрес.
def get_address_from_coords(coords:str):
    #заполняем параметры, которые описывались выже. Впиши в поле apikey свой токен!
    PARAMS = {
        "apikey":"06607ecf-46ac-463a-88b1-08c25f1ace00",
        "format":"json",
        "lang":"ru_RU",
        "kind":"house",
        "geocode": coords
    }

    #отправляем запрос по адресу геокодера.
    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        #получаем данные
        json_data = r.json()
        #вытаскиваем из всего пришедшего json именно строку с полным адресом.
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        #возвращаем полученный адрес
        print(address_str)
        return address_str
    except Exception as e:
        #если не смогли, то возвращаем ошибку
        return "error"

