import mysql.connector as mysqldb

def connection():
    conn = mysqldb.connect(user='root', password='password', host='localhost', database='flask_users')
    c = conn.cursor()
    return(c, conn)