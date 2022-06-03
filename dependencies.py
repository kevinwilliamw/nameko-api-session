from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

import uuid

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection
        
    def add_user(self, username, password):
        # check user existence
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM user 
        WHERE username = %s;
        """, (username,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username': row['username']
            })
        # user existed - return msg 
        if result:
            cursor.close()
            return "User existed"
        
        # user doesn't exist - register new user, return msg 
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            cursor.execute("""
            INSERT INTO user (id, username, password)
            VALUES (%s, %s, %s);
            """, (generateUUID, username, password))
            cursor.close()
            self.connection.commit()
            return "User does not exist. Registered as new user."
    
    # get user for login
    def get_user(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM user 
        WHERE username = %s AND password = %s;
        """, (username, password))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username': row['username']
            })
        cursor.close()
        return result

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='soa',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())