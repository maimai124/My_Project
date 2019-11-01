import pymysql


def con_mysql():
    return pymysql.connect(host='127.0.0.1',port=3306,
                           user='root',password='123456',
                           db='mall',charset='utf8')

def insert_into_mysql(user_name,pass_word):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("insert into user(user_level,user_name,user_password) values (0,'%s','%s')" % (user_name,pass_word))
    conn.commit()
    cursor.close()
    conn.close()

def username_exist(user_name):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_name from user where user_name ='%s'" % (user_name))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if len(data) == 0:
        return  True
    else:
        return False