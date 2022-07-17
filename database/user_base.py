import pymysql

from auxiliary_files import validation

users_dictionary = {}

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
            CREATE TABLE IF NOT EXISTS users_data (
                id          INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                user_id     INTEGER NOT NULL,
                name        TEXT NOT NULL,
                surname     TEXT NOT NULL,
                age         INTEGER NOT NULL,
                gender      TEXT NOT NULL,
                city        TEXT NOT NULL
            )
        ''')
    c.close()
    conn.commit()


def add_user(val:tuple):
    conn = get_connection()
    c = conn.cursor()

    sql = 'INSERT INTO users_data (user_id, name, surname, age, gender, city) VALUES(%s,%s,%s,%s,%s,%s)'

    c.execute(sql,val)
    c.close()

    conn.commit()

def delete_user(user_id: int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'DELETE FROM users_data WHERE user_id = %s'
    val = user_id

    c.execute(sql,val)

    sql = 'DELETE FROM places_data WHERE user_id = %s'
    val = user_id

    c.execute(sql,val)

    c.close()

    conn.commit()
   

def print_all():
    conn = get_connection()
    c = conn.cursor()
    
    sql = 'SELECT * FROM users_data'
    
    c.execute(sql)
    res = c.fetchall()
    c.close()
    
    us = []
    for row in res:
        us.append(row[1])
        
    return us

def check_user(user_id: int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT user_id FROM users_data WHERE user_id=%s'
    val = user_id

    try:
        c.execute(sql, val)
        res = c.fetchone()
    except:
        return check_user(user_id)
        
    c.close()

    conn.commit()
    
    if res == None:
        return False
    else:
        return True
    


def count_users():
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT COUNT(*) FROM users_data'

    c.execute(sql)
    (res,) = c.fetchone()
    print(res)
    c.close()

    conn.commit()
    return res

def del_table():
    conn = get_connection()
    c = conn.cursor()

    sql = 'DROP TABLE IF EXISTS users_data'

    c.execute(sql)

    c.close()
    conn.commit()


def get_name(user_id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT * FROM users_data WHERE user_id=%s'
    val = (user_id,)

    c.execute(sql, val)
    res = c.fetchone()
    c.close()

    conn.commit()
    return res[2] + " " + res[3] + "\nГород: " + res[6]

def get_myinfo(user_id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'SELECT * FROM users_data WHERE user_id=%s'
    val = (user_id,)

    c.execute(sql, val)
    res = c.fetchone()
    c.close()

    conn.commit()
    your = None

    if res != None:
        your = "Вы: " + res[2] + " " + res[3] + "\n"
        your += "Вам: " +  validation.years(res[4]) + "\n" 
        your += "Пол: " + res[5] + "\n"
        your += "Ваш город: " + res[6] + "\n\n"

    return your

def update_name(name:str, id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'UPDATE users_data SET name = %s WHERE user_id = %s'
    val = (name, id)

    c.execute(sql, val)
    c.close()
    conn.commit()

def update_surname(surname:str, id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'UPDATE users_data SET surname = %s WHERE user_id = %s'
    val = (surname,id)
    
    c.execute(sql, val)
    c.close()
    conn.commit()  

def update_age(age:int, id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'UPDATE users_data SET age = %s WHERE user_id = %s'
    val = (age, id)

    c.execute(sql, val)
    c.close()
    conn.commit() 

def update_gender(gender:str, id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'UPDATE users_data SET gender = %s WHERE user_id = %s'
    val = (gender, id)

    c.execute(sql, val)
    c.close()
    conn.commit()   

def update_city(city:str, id:int):
    conn = get_connection()
    c = conn.cursor()

    sql = 'UPDATE users_data SET city = %s WHERE user_id = %s'
    val = (city, id)

    c.execute(sql, val)
    c.close()
    conn.commit()   

#if __name__ == '__main__':
