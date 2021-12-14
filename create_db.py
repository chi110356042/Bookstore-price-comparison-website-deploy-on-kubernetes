import mysql
from mysql import connector
import mysql.connector

mydb=mysql.connector.conncet(
    host="localhost",
    user="root",
    passwd="vvv871202",
)
my_cursor=mydb.cursor()
my_cursor.execute("CREATE DATABASE our_users")
my_cursor.execute("SHOW DATABASE")
for db in my_cursor:
    print(db)