import pymysql

category_dictionary = {}

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
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY not null AUTO_INCREMENT,
                category_type VARCHAR(50) NOT NULL
                )
        ''')
    c.close()
    conn.commit()



def add_category():
    conn = get_connection()
    c = conn.cursor()

    sql = 'INSERT INTO category (id,category_type) VALUE(%s,%s)'

    val = ((1,'Поесть'),(2,'Красота'),(3,'Цветы'),(4,'Медицина'),(5,'Развлечения'))

    try: 
        c.executemany(sql,val) 
        conn.commit() 
        print(c.rowcount,"Таблица заполнено! Количество записей = ",c.lastrowid) 
    
    except: 
        print("Таблица уже заполнена!")
        conn.rollback() 


if __name__ == '__main__':
    add_category()