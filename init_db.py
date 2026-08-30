import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            icon TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database created!")

def add_modules():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM modules")
    count = cursor.fetchone()[0]

    if count == 0:

        modules = [
            ("Français", "Cours", "🇫🇷"),
            ("Anglais technique", "Cours", "🇬🇧"),
            ("Pratique de la paie", "Cours", "💰"),
            ("Culture entrepreneuriale", "Cours", "💡"),
            ("Compétences comportementales", "Cours", "🧠"),
            ("Entrepreneuriat - PIE 2", "Cours", "🚀"),
            ("Culture et techniques avancées du numérique", "Cours", "💻"),
            ("Mathématiques financières", "Cours", "🧮"),
            ("Droit des affaires", "Cours", "⚖️"),
            ("Contrôle de gestion - budgets et tableau de bord", "Cours", "📊"),
            ("Analyse financière", "Cours", "📈"),
            ("Bureautique avancée", "Cours", "🖥️"),

            # EFM
            ("Comptabilité approfondie", "EFM", "📒"),
            ("Fiscalité de l'entreprise", "EFM", "🧾"),
            ("Contrôle de gestion", "EFM", "📊"),
            ("Comptabilité analytique d'exploitation", "EFM", "📑"),
        ]

        cursor.executemany(
            """
            INSERT INTO modules (name, type, icon)
            VALUES (?, ?, ?)
            """,
            modules
        )

        conn.commit()

        print("16 modules added!")

    else:
        print(f"The database already contains {count} modules.")

    conn.close()

if __name__ == "__main__":
    init_db()
    add_modules()