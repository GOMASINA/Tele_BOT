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

    def AddToWaitList(self, name):
        if self.connection:
            try:
                self.cursor.execute("""INSERT INTO registerlist (name)
                                    VALUES (%s);""",
                                    (name,))
                self.connection.commit()
                print('Execution complete!')
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                self.connection.rollback()

    def AddToUsersList(self, id):
        if self.connection:
            try:
                self.cursor.execute("""INSERT INTO userlist (id, name)
                                    SELECT id, name
                                    FROM registerlist
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
                    cursor.execute("""SELECT * FROM userlist;""")
                    rows = cursor.fetchall()
                    return rows
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                return None

    #user_id - это СТРОКА, а не int!
    def UserInformation(self, user_id):
        if self.connection:
            try:
                self.cursor.execute("""SELECT * FROM userlist
                                    WHERE id = %s;""", (user_id))
                user = self.cursor.fetchone()
                return user
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                return None

    #Если что ещё понадобится, то пиши. Я разобрался в теме, так что быстро насочиняю, что 
    def NewbieInformation(self, newbie_id):
        if self.connection:
            try:
                self.cursor.execute("""SELECT * FROM registerlist 
                                    WHERE id = %s;""", (newbie_id))
                user = self.cursor.fetchone()
                return user
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                return None

    def ChangeUserRole(self, user_id, new_ststus):
        if self.connection:
            try:
                self.cursor.execute("""UPDATE userlist
                                       SET role = %s
                                       WHERE id = %s;""", (new_ststus, user_id))
                self.connection.commit()
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                self.connection.rollback()

    def ChangeUserAccess(self, user_id, access_level):
        if self.connection:
            try:
                self.cursor.execute("""UPDATE userlist
                                       SET access_level = %s
                                       WHERE id = %s;""", (access_level, user_id))
                self.connection.commit()
            except psycopg2.Error as e:
                print(f"Error!: {e}")
                self.connection.rollback()