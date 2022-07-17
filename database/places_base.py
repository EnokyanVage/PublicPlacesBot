from email import message
import pymysql

from data import config
from auxiliary_files import location
from auxiliary_files import validation
from database import user_base
from publicplaces_functionality import searchpp

pps_dictionary = {}
get_pages_cat = {}

config = {
    'host': "a0679737.xsph.ru",
    'user': "a0679737_publicplaces",
    'password': "12231718",
    'database': "a0679737_publicplaces"
}

__connection = None


def get_connection():
    global __connection
    try:
        if __connection == None:
            __connection = pymysql.connect(**config)

    except pymysql.Error as e:
        print(e)
    return __connection

def init_db(forse: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if forse:
        c.execute('''
            CREATE TABLE IF NOT EXISTS places_data (
                id INTEGER PRIMARY KEY not null AUTO_INCREMENT,
                user_id INTEGER not null,
                pp_name VARCHAR(40) not null,
                number_phone VARCHAR(12) not null,
                location VARCHAR(256) not null,
                description VARCHAR(512) not null,
                time_work VARCHAR(256) not null,
                social_network VARCHAR(50) not null
                )
        ''')

    c.close()
    conn.commit()


def add_places(val:tuple):
    conn = get_connection()
    c = conn.cursor()

    print(val)

    # sql = 'INSERT INTO places_data (user_id, type, about, location, user_phone, day, hour) VALUES(%s,%s,%s,%s,%s,%s,%s)'
    sql = 'INSERT INTO places_data (user_id, pp_name, number_phone, location, description, time_work, social_network) VALUE(%s,%s,%s,%s,%s,%s,%s)'


        # INSERT INTO public (user_id, pp_name, number_phone, location, description, time_work, social_network) 
        # VALUES('1','VageRom','89537975351','Новосибирск, Бориса Богаткова 125','Крутое место для чаепития','пн-cб:12:00 - 24:00','vagerom@good.ru')
    
    c.execute(sql,val)
    c.close()
    conn.commit()

def delete_places(user_id: int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'DELETE FROM places_data WHERE user_id = %s'
    val = user_id

    c.execute(sql, val)
    c.close()
    conn.commit()
    
def count_places():
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT COUNT(*) FROM places_data'

    c.execute(sql)
    (res,) = c.fetchone()
    c.close()
    conn.commit()

    return res


def print_all():
    conn = get_connection()
    c = conn.cursor()

    # sql = 'SELECT * FROM places_data,placescategory'
    sql = 'SELECT * FROM places_data join placescategory on places_data.id = placescategory.id_places join places_photo on  places_data.id = places_photo.id_places'
    # sql = 'SELECT * FROM places_data,placescategory WHERE places_data.id = placescategory.id_places and placescategory.id_category = %s'
    # sql = 'SELECT * FROM places_data,placescategory WHERE placescategory.id_category = %s'

    c.execute(sql)
    res = c.fetchall()
    # print(res)
    c.close()
    conn.commit()

    return res


def del_table():
    conn = get_connection()
    c = conn.cursor()
    
    sql = 'DROP TABLE IF EXISTS places_data'

    c.execute(sql)
    c.close()
    conn.commit()

def del_places(id:int, user_id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'DELETE FROM places_data WHERE id LIKE %s AND user_id LIKE %s'
    val = (id,user_id)

    c.execute(sql, val)
    c.close()
    conn.commit()

def get_my_id():
    conn = get_connection()
    c = conn.cursor()
    
    sql = 'SELECT id FROM places_data'

    c.execute(sql)
    res = c.fetchall()
    # print("Tut = ",res)
    c.close()
    conn.commit()

    return res

def get_pages():
    conn = get_connection()
    c = conn.cursor()
    
    sql = 'SELECT * FROM places_data'
    
    c.execute(sql)
    res = c.fetchall()
    c.close()
    conn.commit()
    print(res)
    allw_c = count_places()
    
    allw_first = "Всего в PublucPlaces " + validation.pps(allw_c) + "\n"
    pages = []
    for row in res:
        all_pp_str = allw_first
        all_pp_str +="Номер в базе - " + str(row[0]) + "\n"
        all_pp_str +="Название - " + str(row[2]) + "\n"
        all_pp_str +="Расположение: - " + location.get_address_from_coords(row[4]) + "\n\n"
        all_pp_str +="Описание: " + str(row[5]) + "\n"
        all_pp_str +="Время работы: " + str(row[6]) + "\n"
        all_pp_str +="Соц-сеть: " + str(row[7]) + "\n"
        all_pp_str +="Для получения контактов: введите команду /getpp"
        pages.append(all_pp_str)
        print("ALLPP 177:",all_pp_str)
    return pages

def get_pages_category(val:tuple):
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT * FROM places_data,placescategory WHERE places_data.id = placescategory.id_places and placescategory.id_category = %s'

    c.execute(sql,val)
    res = c.fetchall()
    c.close()
    conn.commit()

    spisok_pp = "Результат поиска: \n\n"

    count_pp = int(0)
    pages = []

    for w in res:
        radius = searchpp.location_radar(str(w[4]), str(searchpp.search_dictionary[message.from_user.id][1]))

        spisok_pp +="Номер - " + str(w[0]) + "\n"
        spisok_pp +="Название компании: " + str(w[2]) + "\n"
        spisok_pp +="Номер телефона: " + str(w[3]) + "\n"
        spisok_pp +="Расположение: - " + location.get_address_from_coords(w[4]) + "\n"
        spisok_pp +="Расстояние до вас: " + str(round(radius,3)) + " км\n"
        spisok_pp +="Описание: " + str(w[5]) + "\n"
        spisok_pp +="Время работы: " + str(w[6]) + "\n"
        spisok_pp +="Соц-сеть: " + str(w[7]) + "\n\n"
    

        count_pp += 1
        pages.append(spisok_pp)
    if( searchpp.search_dictionary.get(message.from_user.id) != None):
        searchpp.search_dictionary.pop(message.from_user.id)
    
    if count_pp == 0:
        spisok_pp += "В заданном радиусе, общественных мест не найдено.\n\nПопробуйте увеличить радиус поиска. /searchpp"

    return pages
   

def get_contact(number:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT * FROM places_data WHERE id = %s'
    val = (number,)

    c.execute(sql, val)
    res = c.fetchone()
    c.close()
    conn.commit()

    contact = False
    if res != None:
        contact = user_base.get_name(res[1]) + "\nНомер телефона: " + res[3]
    
    return contact

def get_mypp_c(user_id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT COUNT(*) FROM places_data WHERE user_id = %s'
    val = (user_id,)

    c.execute(sql, val)
    (res,) = c.fetchone()
    c.close()
    conn.commit()

    return res

def get_mypp_pages(user_id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT * FROM places_data where places_data.user_id = %s'
    val = (user_id,)

    c.execute(sql,val)
    res = c.fetchall()
    c.close()
    conn.commit()

    w_c = get_mypp_c(user_id)
    
    all_pp_str = "У вас всего " + validation.pps(w_c) + "\n\n"
    for row in res: 
        all_pp_str +="Номер в базе - " + str(row[0]) + "\n"
        all_pp_str +="Название - " + str(row[2]) + "\n"
        all_pp_str +="Расположение: - " + location.get_address_from_coords(row[4]) + "\n\n"
        all_pp_str +="Описание: " + str(row[5]) + "\n"
        all_pp_str +="Время работы: " + str(row[6]) + "\n"
        all_pp_str +="Соц-сеть: " + str(row[7]) + "\n\n"
       
    return all_pp_str

def get_my_pp_id(user_id:int,id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT * FROM places_data WHERE id LIKE %s AND user_id LIKE %s'
    val = (id,user_id,)

    c.execute(sql, val)
    res = c.fetchone()
    c.close()
    conn.commit()
    
    if res == None:
        return False
    else:
        allw_str ="Номер в базе - " + str(res[0]) + "\n"
        allw_str +="Название: " + str(res[2]) + "\n"
        allw_str +="Описание: " + str(res[5]) + "\n"
        allw_str +="Расположение: - " + location.get_address_from_coords(res[4]) + "\n\n"
        return allw_str

if __name__ == '__main__':
    del_table()