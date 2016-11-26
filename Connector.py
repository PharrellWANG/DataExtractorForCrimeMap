# this is for testing whether the mysql.connector works or not.
import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': '123456',
    'host': '127.0.0.1',
    'database': 'employees',
    'raise_on_warnings': True,
}

try:
    # cnx = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='crimemap')
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Hint: Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Hint: Database does not exist")
    else:
        print(err)
else:
    cnx.close()
