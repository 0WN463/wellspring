#!/usr/bin/python3

import sqlite3
from sqlite3 import Error
import sys

class GateKeeper:
    def __init__(self):
        def create_connection(path):
            connection = sqlite3.connect(path)
        
            return connection
    
        self.connection = create_connection('./users.sqlite')

    def authenticate(self, name, secret_name):
        select_users = f"SELECT * FROM users WHERE name='{name}' AND secret_name='{secret_name}'"
        users = self._execute_read_query(select_users)
        
        if len(users) == 0:
            print("Name and secret name does not match. Villains are not allowed!")
        else:
            user = users[0]
            _, name, secret_name = user
            print(f"Name and secret name matches. Welcome to the club, {name} (alias {secret_name}).")

    def _execute_read_query(self, query):
        print(f"Executing query: {query}")
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
    
    
if len(sys.argv) != 3:
    print("Wrong number of arguments")
    exit()
    
_, input_name, input_secret_name, *_ = sys.argv
gate_keeper = GateKeeper()
gate_keeper.authenticate(input_name, input_secret_name)
