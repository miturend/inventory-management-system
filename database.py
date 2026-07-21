import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Miturend@2008",      # Put your MySQL password here if you have one
        database="BusinessMs"
    )
    return connection