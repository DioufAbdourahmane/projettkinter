from database import connect_db

def add_contact(nom, prenom, telephone, email, adresse):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO contacts (nom, prenom, telephone, email, adresse) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (nom, prenom, telephone, email, adresse))
    conn.commit()
    conn.close()

def search_contact(nom):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM contacts WHERE nom LIKE %s"
    cursor.execute(query, ('%' + nom + '%',))
    results = cursor.fetchall()
    conn.close()
    return results
