import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Utilisateur MySQL, à adapter si nécessaire
        password='',  # Mot de passe MySQL, à adapter si nécessaire
        database='gestion_contacts'
    )
    return conn
