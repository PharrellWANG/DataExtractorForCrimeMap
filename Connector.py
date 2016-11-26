import mysql.connector

from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='crimemap')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Hint: Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Hint: Database does not exist")
    else:
        print(err)
else:
    cnx.close()
