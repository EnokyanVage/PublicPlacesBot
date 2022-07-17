import pymysql


pc_dictionary = {}
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
            CREATE TABLE IF NOT EXISTS placescategory (
                id INTEGER PRIMARY KEY not null AUTO_INCREMENT,
                user_id INTEGER NOT NULL,
                id_places INTEGER NOT NULL,
                id_category INTEGER not null,
                FOREIGN KEY (id_places) REFERENCES places_data(id) ON DELETE CASCADE,
                FOREIGN KEY (id_category) REFERENCES category(id) ON DELETE CASCADE
                )
        ''')
    c.close()
    conn.commit()


def add_category(val:tuple):
    conn = get_connection()
    c = conn.cursor()
    print(val)
    sql = 'INSERT INTO placescategory (user_id,id_places, id_category) VALUE(%s,(SELECT max(pd.id) FROM places_data as pd WHERE pd.user_id = %s),%s)'
    c.execute(sql,val)
    c.close()

    conn.commit()
