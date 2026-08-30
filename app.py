import os
import sqlite3
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    g,
    jsonify,
    send_from_directory,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "ge_assistant_secret_key_2026"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pdf"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# مستخدم افتراضي حالياً
CURRENT_USER_ID = 1


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# --- DASHBOARD ---
@app.route("/")
def index():
    if not g.user:
        return redirect("/login")

    conn = get_db()
    courses = conn.execute(
        "SELECT * FROM modules WHERE type = 'Cours'"
    ).fetchall()
    efms = conn.execute(
        "SELECT * FROM modules WHERE type = 'EFM'"
    ).fetchall()

    # Notes تبقى خاصة بكل مستخدم بوحدو
    total_notes = conn.execute(
        "SELECT COUNT(*) FROM notes WHERE user_id = ?", (g.user["id"],)
    ).fetchone()[0]

    # 🌐 Résumés تولي تحسب كاع الملفات المرفوعة فـ المنصة باش تبان للطلاب كاملين
    total_resumes = conn.execute(
        "SELECT COUNT(*) FROM resumes"
    ).fetchone()[0]

    total_efm_files = conn.execute(
        "SELECT COUNT(*) FROM efm_files"
    ).fetchone()[0]

    conn.close()

    stats = {
        "notes": total_notes,
        "resumes": total_resumes,
        "efm_files": total_efm_files,
    }

    return render_template(
        "index.html", courses=courses, efms=efms, stats=stats
    )


# --- MODULE DETAILS, NOTES & RESUMES ---
@app.route("/module/<int:id>")
def module_detail(id):
    conn = get_db()

    module = conn.execute(
        "SELECT * FROM modules WHERE id = ?", (id,)
    ).fetchone()

    # Mots الشخصية كتبقى حصرية للمستخدم اللي كتبها
    notes = conn.execute(
        "SELECT * FROM notes WHERE module_id = ? AND user_id = ? ORDER BY created_at DESC",
        (id, g.user["id"]),
    ).fetchall()

    # 🌐 Résumés (PDFs) كيبانو لجميع الطلاب كدروس ملخصة
    resumes = conn.execute(
        "SELECT * FROM resumes WHERE module_id = ? ORDER BY created_at DESC",
        (id,),
    ).fetchall()

    conn.close()

    if module is None:
        return "Module introuvable", 404

    return render_template(
        "module_detail.html", module=module, notes=notes, resumes=resumes
    )


@app.route("/module/<int:id>/add-note", methods=["POST"])
def add_note(id):
    if not g.user:
        return redirect("/login")

    content = request.form.get("content", "").strip()
    title = request.form.get("title", "").strip() or "Note"
    status = request.form.get("status", "Compris")

    if content:
        conn = get_db()
        # 🔑 استبدال CURRENT_USER_ID بـ g.user["id"]
        conn.execute(
            "INSERT INTO notes (module_id, title, content, status, user_id) VALUES (?, ?, ?, ?, ?)",
            (id, title, content, status, g.user["id"]),
        )
        conn.commit()
        conn.close()

    return redirect(f"/module/{id}")


@app.route("/module/<int:id>/upload-resume", methods=["POST"])
def upload_resume(id):
    if not g.user:
        return redirect("/login")

    if "file" not in request.files:
        return "Aucun fichier", 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return "Fichier PDF invalide", 400

    title = request.form.get("title", "").strip() or file.filename
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    conn = get_db()
    # 🔑 استبدال CURRENT_USER_ID بـ g.user["id"]
    conn.execute(
        "INSERT INTO resumes (module_id, title, filename, user_id) VALUES (?, ?, ?, ?)",
        (id, title, filename, g.user["id"]),
    )
    conn.commit()
    conn.close()

    return redirect(f"/module/{id}")


# --- EFM CENTER ---
@app.route("/efm")
@app.route("/efm-center")  # 👈 ضفت هاد المسار باش يخدم مع الـ Navbar
def efm_center():
    conn = get_db()
    efm_modules = conn.execute(
        "SELECT * FROM modules WHERE type = 'EFM'"
    ).fetchall()
    conn.close()
    return render_template("efm_center.html", modules=efm_modules)


@app.route("/efm/<int:module_id>")
def efm_detail(module_id):
    conn = get_db()
    module = conn.execute(
        "SELECT * FROM modules WHERE id = ? AND type = 'EFM'", (module_id,)
    ).fetchone()
    files = conn.execute(
        "SELECT * FROM efm_files WHERE module_id = ? ORDER BY year DESC",
        (module_id,),
    ).fetchall()
    conn.close()

    if module is None:
        return "Module EFM introuvable", 404

    return render_template("efm_detail.html", module=module, files=files)


@app.route("/efm/<int:module_id>/upload", methods=["POST"])
def upload_efm(module_id):
    if "file" not in request.files:
        return "Aucun fichier", 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return "Fichier PDF invalide", 400

    title = request.form.get("title", "").strip() or file.filename
    year = request.form.get("year", "2026").strip()
    file_type = request.form.get("file_type", "efm")

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    conn = get_db()
    conn.execute(
        "INSERT INTO efm_files (module_id, title, year, file_type, filename) VALUES (?, ?, ?, ?, ?)",
        (module_id, title, year, file_type, filename),
    )
    conn.commit()
    conn.close()

    return redirect(f"/efm/{module_id}")


# --- CALCULATRICES ---
@app.route("/calculators")
@app.route("/calculatrices")  # 👈 ضفت هاد المسار باش يخدم مع الـ Navbar
def calculators():
    return render_template("calculators.html")


@app.route("/calculators/tva", methods=["POST"])
def calc_tva():
    amount = float(request.form.get("amount", 0))
    tva_rate = float(request.form.get("tva_rate", 20))
    calc_type = request.form.get("calc_type", "ht_to_ttc")

    if calc_type == "ht_to_ttc":
        ht = amount
        tva_amount = ht * (tva_rate / 100)
        ttc = ht + tva_amount
    else:
        ttc = amount
        ht = ttc / (1 + (tva_rate / 100))
        tva_amount = ttc - ht

    result = {
        "ht": round(ht, 2),
        "tva_rate": tva_rate,
        "tva_amount": round(tva_amount, 2),
        "ttc": round(ttc, 2),
    }

    return render_template("calculators.html", tva_result=result)


@app.route("/calculators/marge", methods=["POST"])
def calc_marge():
    pv_ht = float(request.form.get("pv_ht", 0))
    pa_ht = float(request.form.get("pa_ht", 0))

    marge_brute = pv_ht - pa_ht
    taux_marge = (marge_brute / pa_ht * 100) if pa_ht > 0 else 0
    taux_marque = (marge_brute / pv_ht * 100) if pv_ht > 0 else 0

    result = {
        "marge_brute": round(marge_brute, 2),
        "taux_marge": round(taux_marge, 2),
        "taux_marque": round(taux_marque, 2),
    }

    return render_template("calculators.html", marge_result=result)


@app.route("/calculators/interet", methods=["POST"])
def calc_interet():
    capital = float(request.form.get("capital", 0))
    taux = float(request.form.get("taux", 0))
    duree = float(request.form.get("duree", 0))
    unite = request.form.get("unite", "annees")

    if unite == "mois":
        interet = (capital * taux * duree) / (12 * 100)
    elif unite == "jours":
        interet = (capital * taux * duree) / (360 * 100)
    else:
        interet = (capital * taux * duree) / 100

    valeur_acquise = capital + interet

    result = {
        "interet": round(interet, 2),
        "valeur_acquise": round(valeur_acquise, 2),
    }

    return render_template("calculators.html", interet_result=result)


# --- DELETION ROUTES ---
@app.route("/note/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = get_db()
    note = conn.execute(
        "SELECT module_id FROM notes WHERE id = ?", (note_id,)
    ).fetchone()
    if note:
        module_id = note["module_id"]
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()
        return redirect(f"/module/{module_id}")
    conn.close()
    return redirect("/")


@app.route("/resume/delete/<int:resume_id>", methods=["POST"])
def delete_resume(resume_id):
    conn = get_db()
    file_data = conn.execute(
        "SELECT module_id, filename FROM resumes WHERE id = ?", (resume_id,)
    ).fetchone()

    if file_data:
        module_id = file_data["module_id"]
        filename = file_data["filename"]
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        conn.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
        conn.commit()
        conn.close()
        return redirect(f"/module/{module_id}")

    conn.close()
    return redirect("/")


@app.route("/efm/file/delete/<int:file_id>", methods=["POST"])
def delete_efm_file(file_id):
    conn = get_db()
    file_data = conn.execute(
        "SELECT module_id, filename FROM efm_files WHERE id = ?", (file_id,)
    ).fetchone()

    if file_data:
        module_id = file_data["module_id"]
        filename = file_data["filename"]
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        conn.execute("DELETE FROM efm_files WHERE id = ?", (file_id,))
        conn.commit()
        conn.close()
        return redirect(f"/efm/{module_id}")

    conn.close()
    return redirect("/efm")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        conn = get_db()
        g.user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()

# --- AUTHENTICATION ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if username and email and password:
            hashed_pw = generate_password_hash(password)
            conn = get_db()
            try:
                conn.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, hashed_pw)
                )
                conn.commit()
                conn.close()
                return redirect("/login")
            except sqlite3.IntegrityError:
                conn.close()
                return render_template("register.html", error="Nom d'utilisateur ou Email déjà utilisé !")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE LOWER(email) = ?", (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            # 🛑 التحقق مما إذا كان الحساب معطلاً (Inactif)
            if user["status"] == "Inactif":
                return render_template(
                    "login.html", error="Votre compte est désactivé. Veuillez contacter l'administrateur."
                )

            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")
        else:
            return render_template(
                "login.html", error="Email ou mot de passe incorrect !"
            )

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# --- ADMIN: RESET PASSWORD ---
@app.route("/admin/reset-password", methods=["GET", "POST"])
def admin_reset_password():
    # كود حماية بسيط: تقدر تبدلو برمز السر ديالك
    admin_secret = "admin2026"

    if request.method == "POST":
        secret_key = request.form.get("secret_key", "").strip()
        username = request.form.get("username", "").strip()
        new_password = request.form.get("new_password", "").strip()

        if secret_key != admin_secret:
            return render_template(
                "admin_reset.html", error="Clé Admin incorrecte !"
            )

        if username and new_password:
            hashed_pw = generate_password_hash(new_password)
            conn = get_db()
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()

            if user:
                conn.execute(
                    "UPDATE users SET password = ? WHERE id = ?",
                    (hashed_pw, user["id"]),
                )
                conn.commit()
                conn.close()
                return render_template(
                    "admin_reset.html",
                    success=f"✅ Mot de passe de '{username}' modifié avec succès !",
                )
            else:
                conn.close()
                return render_template(
                    "admin_reset.html", error="Utilisateur introuvable !"
                )

    return render_template("admin_reset.html")

@app.route('/admin')
def admin_panel():
    if not g.user or g.user['role'] != 'admin':
        return redirect('/')

    conn = get_db()
    users = conn.execute("SELECT id, username, email, role, status FROM users").fetchall()
    conn.close()

    system_info = {
        'python_version': '3.12',
        'status': 'Opérationnel',
        'server_time': '2026-08-28'
    }
    
    return render_template('admin.html', users=users, system_info=system_info)


# 1️⃣ تفعيل / تعطيل الحساب
@app.route('/admin/toggle-user/<int:user_id>', methods=['POST'])
def toggle_user(user_id):
    if not g.user or g.user['role'] != 'admin':
        return redirect('/')

    conn = get_db()
    user = conn.execute("SELECT status FROM users WHERE id = ?", (user_id,)).fetchone()
    
    if user:
        # تبديل الحالة بين Actif و Inactif
        new_status = 'Inactif' if user['status'] == 'Actif' else 'Actif'
        conn.execute("UPDATE users SET status = ? WHERE id = ?", (new_status, user_id))
        conn.commit()
    
    conn.close()
    return redirect('/admin')


# 2️⃣ إعادة تعيين كلمة السر لـ 123456
@app.route('/admin/reset-access/<int:user_id>', methods=['POST'])
def reset_access(user_id):
    if not g.user or g.user['role'] != 'admin':
        return redirect('/')

    # كلمة السر الافتراضية الجديدة هي: 123456
    default_password = generate_password_hash("123456")
    
    conn = get_db()
    conn.execute("UPDATE users SET password = ? WHERE id = ?", (default_password, user_id))
    conn.commit()
    conn.close()

    return redirect('/admin')

# --- ALL RESUMES PAGE ---
@app.route("/all-resumes")
def all_resumes():
    if not g.user:
        return redirect("/login")
    
    conn = get_db()
    # جلب جميع الـ PDFs مع اسم الموديول التابع ليها
    resumes = conn.execute("""
        SELECT resumes.*, modules.name as module_name 
        FROM resumes 
        LEFT JOIN modules ON resumes.module_id = modules.id 
        ORDER BY resumes.id DESC
    """).fetchall()
    conn.close()
    
    return render_template("all_resumes.html", resumes=resumes)


# --- ALL NOTES PAGE ---
@app.route("/all-notes")
def all_notes():
    if not g.user:
        return redirect("/login")
    
    conn = get_db()
    # جلب جميع الملاحظات الخاصة بالمستخدم الحالي
    notes = conn.execute("""
        SELECT notes.*, modules.name as module_name 
        FROM notes 
        LEFT JOIN modules ON notes.module_id = modules.id 
        WHERE notes.user_id = ? 
        ORDER BY notes.id DESC
    """, (g.user["id"],)).fetchall()
    conn.close()
    
    return render_template("all_notes.html", notes=notes)

# --- ALL EFM FILES PAGE ---
@app.route("/all-efms")
def all_efms():
    if not g.user:
        return redirect("/login")
    
    conn = get_db()
    # جلب جميع ملفات EFM مع اسم الموديول التابع ليها
    efm_files = conn.execute("""
        SELECT efm_files.*, modules.name as module_name 
        FROM efm_files 
        LEFT JOIN modules ON efm_files.module_id = modules.id 
        ORDER BY efm_files.id DESC
    """).fetchall()
    conn.close()
    
    return render_template("all_efms.html", efm_files=efm_files)


if __name__ == "__main__":
    app.run(debug=True)