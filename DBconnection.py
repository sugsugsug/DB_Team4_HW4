import MySQLdb

host = "localhost"
user = "root"
pw = "root"
name = "university_info"
port = 3306

connect_pool = []

#start connection with the database
def connectDB():
    connect = MySQLdb.connect(host, user, pw, name, port)
    return connect

#get connection from connect_pool
def get_connect():
    global connect_pool
    if not connect_pool:
        connect_tmp = connectDB()
        connect_pool.append(connect_tmp)
    return connect_pool.pop()

#return connection to connect_pool
def return_connect(conn):
    global connect_pool
    connect_pool.append(conn)
    return

def close_db(db):
    db.close()
    return

