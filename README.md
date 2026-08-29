Markdown
# 🎓 GE Student Assistant

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-v5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Operational-brightgreen)](#)

**GE Student Assistant** is a full-featured web application designed for 2nd-year Business Management (**Gestion des Entreprises - GE**) students. It streamlines learning by offering centralized course management, personal note-taking, shared PDF summaries, national exam (EFM) archives, and integrated financial calculators.

🌐 **Live Demo:** [yassine1x.pythonanywhere.com](https://yassine1x.pythonanywhere.com/)

---

## ✨ Key Features

* **🔐 Authentication & User Roles:**
  * Secure student registration and login powered by `Werkzeug Security` password hashing.
  * Role-based control (Admin vs. Student) with account activation/deactivation toggles.
* **📊 Interactive Dashboard:**
  * Real-time counters for personal notes, uploaded PDF summaries, and EFM files.
  * Clickable stat cards leading directly to aggregated views for all study resources.
* **📚 Course & Module Management:**
  * Dedicated spaces for 12 core academic modules.
  * Isolated personal note-taking system per user.
* **🎯 EFM Exam Center:**
  * Archive for past regional and national exams (EFM) and answer keys in PDF format.
* **🧮 Financial & Business Calculators:**
  * **TVA Calculator:** Quick conversion between HT and TTC amounts.
  * **Margin Calculator:** Calculate Gross Margin, Margin Rate (*Taux de Marge*), and Mark-up Rate (*Taux de Marque*).
  * **Simple Interest Calculator:** Compute financial interest and acquired value across days, months, or years.
* **📱 Fully Responsive Interface:**
  * Mobile-optimized navigation bar with collapsible menu built on **Bootstrap 5**.

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, FontAwesome
* **Database:** SQLite3
* **Hosting:** PythonAnywhere
* **Version Control:** Git & GitHub

---

## 🚀 Local Installation & Setup

Follow these steps to run the application locally on your machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/yassine1x/GE-Student-Assistant.git](https://github.com/yassine1x/GE-Student-Assistant.git)
cd GE-Student-Assistant
2. Set Up a Virtual Environment
Windows (PowerShell):

PowerShell
python -m venv venv
.\venv\Scripts\activate
Linux / macOS:

Bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install flask werkzeug
4. Run the Application
Bash
python app.py
Open your browser and navigate to: http://127.0.0.1:5000/

📁 Project Structure
Plaintext
GE-Student-Assistant/
├── static/              # Stylesheets, Scripts, & Assets
├── templates/           # Jinja2 Templates (HTML views)
│   ├── base.html        # Main Layout & Responsive Navigation
│   ├── index.html       # Dashboard
│   ├── module_detail.html
│   ├── all_resumes.html
│   ├── all_notes.html
│   ├── all_efms.html
│   └── calculators.html
├── uploads/             # Stored PDF Files & Summaries
├── app.py               # Main Flask Routing & Logic
├── database.db          # SQLite Database File
└── README.md            # Project Documentation
⚡ Developer & Credits
Developed and engineered by Yassine Saadi

Powered by Sahdi ⚡


---

### خطوة الرفع المباشرة لـ GitHub:

افتح الـ Terminal في **VS Code** واكتب الأوامر التالية:

```powershell
git add README.md
git commit -m "Translate README to English"
git push origin main
