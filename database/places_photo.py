import pymysql

photo_dictionary = {}

# print(photo_dictionary)
config = {
    'host': "a0679737.xsph.ru",
    'user': "a0679737_publicplaces",
    'password': "12231718",
    'database': "a0679737_publicplaces"
}


__connection = None

def get_connection():
    global __connection
    if __connection == None:
        __connection = pymysql.connect(**config)
    return __connection

def init_db(forse: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if forse:
        c.execute('''
            CREATE TABLE IF NOT EXISTS places_photo (
                id INTEGER PRIMARY KEY not null AUTO_INCREMENT,
                id_places INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                photo BLOB NOT NULL,
                photo_link VARCHAR(256) NOT NULL,
                FOREIGN KEY (id_places) REFERENCES places_data(id) ON DELETE CASCADE
                )
        ''')
    c.close()
    conn.commit()

def add_photo(val:tuple):
    conn = get_connection()
    c = conn.cursor()

    sql = 'INSERT INTO places_photo (id_places,user_id, photo, photo_link) VALUE((SELECT max(pd.id) FROM places_data as pd WHERE pd.user_id = %s),%s,%s,%s)'
    c.execute(sql,val)
    c.close()
    conn.commit()

def print_photo(val:tuple):
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT photo_link FROM places_photo,places_data where places_data.id = places_photo.id_places and places_data.id = %s'
    
    c.execute(sql,val)
    res = c.fetchone()

    c.close()
    conn.commit()

    photo = False
    if res != None:
        photo = str(res[0])
    
    return photo

