import mysql.connector

from server.crypto import add_ciphers
from server.constants import HOST, USER, PASSWD, DATABASE


class ServerMiddleware:

    def __init__(self, public_key):
        self.db = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
        self.public_key = public_key

    def create_encrypted_variable(self, name, ope_cipher, he_cipher):
        sql = "INSERT INTO encrypted_variable (name, ope_cipher, he_cipher) VALUES (%s, %s, %s)"
        val = (name, ope_cipher, str(he_cipher))
        cursor = self.db.cursor()
        cursor.execute(sql, val)
        self.db.commit()

    def get_encrypted_variable(self, name):
        sql = "SELECT * FROM encrypted_variable WHERE name = %s"
        val = (name,)
        cursor = self.db.cursor()
        cursor.execute(sql, val)
        encrypted_variable = cursor.fetchone()
        ope_cipher = encrypted_variable[1]
        he_cipher = int(encrypted_variable[2])
        return name, ope_cipher, he_cipher

    def delete_encrypted_variable(self, name):
        sql = "DELETE FROM encrypted_variable WHERE name = %s"
        val = (name,)
        cursor = self.db.cursor()
        cursor.execute(sql, val)
        self.db.commit()

    def update_ope_cipher(self, name, cipher):
        sql = "UPDATE encrypted_variable SET ope_cipher = %s WHERE name = %s"
        val = (cipher, name)
        cursor = self.db.cursor()
        cursor.execute(sql, val)
        self.db.commit()

    def update_he_cipher(self, name, cipher):
        sql = "UPDATE encrypted_variable SET he_cipher = %s WHERE name = %s"
        val = (str(cipher), name)
        cursor = self.db.cursor()
        cursor.execute(sql, val)
        self.db.commit()

    def compare_ciphers(self, name1, name2):
        sql = "SELECT ope_cipher FROM encrypted_variable WHERE name = %s"
        val1 = (name1,)
        val2 = (name2,)
        cursor = self.db.cursor()
        cursor.execute(sql, val1)
        cipher1 = cursor.fetchone()[0]
        cursor.execute(sql, val2)
        cipher2 = cursor.fetchone()[0]
        return cipher1 <= cipher2

    def add_ciphers(self, name1, name2):
        sql = "SELECT he_cipher FROM encrypted_variable WHERE name = %s"
        val1 = (name1,)
        val2 = (name2,)
        cursor = self.db.cursor()
        cursor.execute(sql, val1)
        cipher1 = int(cursor.fetchone()[0])
        cursor.execute(sql, val2)
        cipher2 = int(cursor.fetchone()[0])
        return add_ciphers(self.public_key, cipher1, cipher2)
