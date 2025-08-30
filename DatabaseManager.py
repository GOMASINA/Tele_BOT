import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional, Union
import logging
from configparser import ConfigParser
import os


class DatabaseManager:
    def __init__(self, config_file='database.ini', section='postgresql'):
        self.config = self._LoadConfig(config_file, section)
        self.connection = None
        self.cursor = None

    def _LoadConfig(self, filename, section):
        parser = ConfigParser()
        parser.read(filename)
        if not parser.has_section(section):
            raise Exception(f'Section {section} not found in {filename}')
        return dict(parser.items(section))

    def Connect(self):
        try:
            self.connection = psycopg2.connect(**self.config)
            self.cursor = self.connection.cursor()
            print("Connected to database")
        except psycopg2.Error as e:
            print(f"Connection error: {e}")

    def Disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnetcted")

    def AddToWaitList(self, name, role, access_level):
        if self.connection:
            try:
                self.cursor.execute("""INSERT INTO registerrequests (name, role, access_level) VALUES (%s, %s, %s);""",
                                    (name, role, access_level))
                self.connection.commit()
                print('Execution complete!')
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                self.connection.rollback()

    def AddToUsersList(self, id):
        if self.connection:
            try:
                self.cursor.execute("""INSERT INTO userslist (id, name, role, access_level)
                                    SELECT id, name, role, access_level
                                    FROM registerrequests
                                    WHERE id=%s;""",
                                    (id,))
                self.connection.commit()
                print('Execution complete!')
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                self.connection.rollback()

    #Возвращает список словарём
    def ListOfUsers(self):
        if self.connection:
            try:
                with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""SELECT * FROM userslist""")
                    rows = cursor.fetchall()
                    return rows
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                return None

    #user_id - это СТРОКА, а не int!
    def UserInformation(self, user_id):
        if self.connection:
            try:
                self.cursor.execute("""SELECT * FROM userslist WHERE id = %s""", (user_id))
                user = self.cursor.fetchone()
                return user
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                return None

    #Если что ещё понадобится, то пиши. Я разобрался в теме, так что быстро насочиняю, что 
    def NewbieInformation(self, newbie_id):
        if self.connection:
            try:
                self.cursor.execute("""SELECT * FROM registerrequests WHERE id = %s""", (newbie_id))
                user = self.cursor.fetchone()
                return user
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                return None
