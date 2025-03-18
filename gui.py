import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connexion à la base de données MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_contacts"
    )

# Fonction pour ajouter un contact
def add_contact():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    telephone = entry_telephone.get()
    email = entry_email.get()
    adresse = entry_adresse.get()

    if not nom or not prenom or not telephone:
        messagebox.showerror("Erreur", "Nom, Prénom et Téléphone sont obligatoires.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (nom, prenom, telephone, email, adresse) VALUES (%s, %s, %s, %s, %s)",
                   (nom, prenom, telephone, email, adresse))
    conn.commit()
    conn.close()

    messagebox.showinfo("Succès", "Contact ajouté avec succès.")
    clear_fields()
    display_contacts()

# Fonction pour rechercher un contact
def search_contact():
    search_term = entry_search.get()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE nom LIKE %s OR telephone LIKE %s", (f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    conn.close()

    tree.delete(*tree.get_children())  # Effacer les anciens résultats
    for row in results:
        tree.insert("", "end", values=row)

# Fonction pour afficher tous les contacts
def display_contacts():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()

    tree.delete(*tree.get_children())  # Nettoyer le tableau
    for row in rows:
        tree.insert("", "end", values=row)

# Fonction pour vider les champs après l'ajout
def clear_fields():
    entry_nom.delete(0, tk.END)
    entry_prenom.delete(0, tk.END)
    entry_telephone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_adresse.delete(0, tk.END)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion de Contacts")
root.geometry("600x500")
root.config(bg="#f4f4f4")

# Frame pour le formulaire
frame_form = tk.Frame(root, bg="#4CAF50", padx=20, pady=20, relief=tk.RIDGE, borderwidth=12)
frame_form.pack(pady=10)

label_style = {"bg": "#ffffff", "font": ("Arial", 22, "bold")}
entry_style = {"font": ("Arial", 22)}

tk.Label(frame_form, text="Nom", **label_style).grid(row=0, column=0, sticky="w", pady=29)
entry_nom = tk.Entry(frame_form, **entry_style)
entry_nom.grid(row=0, column=1, pady=29)

tk.Label(frame_form, text="Prénom", **label_style).grid(row=1, column=0, sticky="w", pady=29)
entry_prenom = tk.Entry(frame_form, **entry_style)
entry_prenom.grid(row=1, column=1, pady=29)

tk.Label(frame_form, text="Téléphone", **label_style).grid(row=2, column=0, sticky="w", pady=29)
entry_telephone = tk.Entry(frame_form, **entry_style)
entry_telephone.grid(row=2, column=1, pady=29)

tk.Label(frame_form, text="Email", **label_style).grid(row=3, column=0, sticky="w", pady=29)
entry_email = tk.Entry(frame_form, **entry_style)
entry_email.grid(row=3, column=1, pady=29)

tk.Label(frame_form, text="Adresse", **label_style).grid(row=4, column=0, sticky="w", pady=29)
entry_adresse = tk.Entry(frame_form, **entry_style)
entry_adresse.grid(row=4, column=1, pady=29)

# Bouton Ajouter Contact
button_add = tk.Button(root, text="Ajouter Contact", command=add_contact,
                       font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=29)
button_add.pack(pady=10)

# Frame pour la recherche
frame_search = tk.Frame(root, bg="#f4f4f4")
frame_search.pack(pady=10)

tk.Label(frame_search, text="Rechercher :", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(frame_search, font=("Arial", 12))
entry_search.pack(side=tk.LEFT, padx=5)
button_search = tk.Button(frame_search, text="Rechercher", command=search_contact, bg="#008CBA", fg="white", font=("Arial", 12))
button_search.pack(side=tk.LEFT, padx=5)

# Table pour afficher les contacts
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

columns = ("ID", "Nom", "Prénom", "Téléphone", "Email", "Adresse")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=50)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack()

# Afficher les contacts au démarrage
display_contacts()

# Lancer l'application
root.mainloop()
