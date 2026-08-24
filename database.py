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

    print("✅ Database créée !")


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

        print("✅ 16 modules ajoutés !")

    else:
        print(f"ℹ️ La base contient déjà {count} modules.")

    conn.close()

def init_notes_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (module_id) REFERENCES modules(id)
        )
    """)

    conn.commit()
    conn.close()

    print("✅ Table notes créée !")

def init_resumes_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            filename TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (module_id) REFERENCES modules(id)
        )
    """)

    conn.commit()
    conn.close()

    print("✅ Table resumes créée !")

def init_efm_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS efm_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year TEXT NOT NULL,
            file_type TEXT NOT NULL, -- 'efm' ou 'correction'
            filename TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (module_id) REFERENCES modules(id)
        )
    """)

    conn.commit()
    conn.close()

    print("✅ Table efm_files créée !")

def update_notes_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE notes ADD COLUMN status TEXT DEFAULT 'Compris'")
        conn.commit()
        print("✅ Column status ajoutée avec succès !")
    except sqlite3.OperationalError:
        print("ℹ️ Column status existe déjà.")
    conn.close()

def init_users_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Table users créée !")

def update_tables_for_multiuser():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # 1. إضافة user_id لجدول notes (افتراضياً 1)
    try:
        cursor.execute("ALTER TABLE notes ADD COLUMN user_id INTEGER DEFAULT 1")
        print("✅ user_id ajouté à la table notes !")
    except sqlite3.OperationalError:
        print("ℹ️ user_id existe déjà dans notes.")

    # 2. إضافة user_id لجدول resumes (افتراضياً 1)
    try:
        cursor.execute("ALTER TABLE resumes ADD COLUMN user_id INTEGER DEFAULT 1")
        print("✅ user_id ajouté à la table resumes !")
    except sqlite3.OperationalError:
        print("ℹ️ user_id existe déjà dans resumes.")

    conn.commit()
    conn.close()

def update_users_table_for_roles():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
        print("✅ Column role ajoutée !")
    except sqlite3.OperationalError:
        pass
    conn.close()


if __name__ == "__main__":
    init_db()
    add_modules()
    init_notes_table()
    init_resumes_table()
    init_efm_table()
    init_users_table()
    update_tables_for_multiuser()
    update_users_table_for_roles()