# 🏃 CITS5505 Project: Exercise Tracker App

## 📌 Purpose of the Application

This web application allows users to track their exercise habits, view stats about their habits, and share information about their achievements with their friends on the system. The application is designed with the following key goals:

- **Engaging:** looks good and focuses the user on important elements of the application.
- **Effective:** produces value for the user, by providing information, entertainment or community.
- **Intuitive:** be easy to use.

### 🔧 Key Features

- **Introductory View:** Welcome page with login and registration options.
- **Upload Data:** Users can upload exercise data manually.
- **Visualise Data:** Interactive charts and summaries showing trends and achievements.
- **Share Data:** Allows users to share specific statistics or progress with friends.

The application uses a Flask backend with SQLite for data storage and a clean JavaScript-based frontend. Styling is handled with Bootstrap.

---

## 👥 Group Members

| UWA ID   | Name                     | GitHub Username |
| -------- | ------------------------ | --------------- |
| 24452786 | Nhat Vu Phan             | jerryfandev     |
| 24343452 | Muhammad Sulaiman Farooq | msf0005         |
| 24267814 | Yuxing Zhou              | zyxasd707       |
| 23218511 | Nuowei Li                | nuoweili        |

---
## 🚀 Setup & Run Instructions
### 1. Clone the repository
```bash
git clone https://github.com/jerryfandev/exercise-tracker-app.git
cd exercise-tracker-app
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
# For different aliases on your machine:
# python3 -m venv venv
```
#### Activate the Virtual Environment:
###### 🍏 On macOS/Linux:
```bash
source venv/bin/activate
```
###### 🪟 On Windows:
```bash
venv\Scripts\activate
```
### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```
### 4. Initialize / Migrate the Database
```bash
# Initialize migrations directory (only once)
flask db init

# Generate migration script based on current models
flask db migrate -m "Initial migration"

# Apply the migration to the database
flask db upgrade

# 💡 Note: Ensure to export FLASK_APP=run.py
# macOS/Linux: export FLASK_APP=run.py
# Windows CMD: set FLASK_APP=run.py
# Windows PowerShell: $env:FLASK_APP = "run.py"
```
### 5. Run the Flask Application
```bash
python run.py
```
#### Alternatively, run the app using Flask CLI:
```bash
# Set environment variables
export FLASK_APP=run.py
export FLASK_ENV=development

# Start the server
flask run
```
### 6. Result
```
http://127.0.0.1:5000
http://localhost:5000
```

## 📌 Notes
- `.venv/` and `.idea/` folders are excluded from version control via `.gitignore`.
- Always activate your virtual environment before running the app or installing dependencies.

## 📁 Sample Folder Structure (to be updated)
```
exercise-tracker-app/
│
├── backend/
│   ├── __init__.py
│   ├── functions.py
│   ├── models.py
│   └── routes.py
│
├── frontend/
│   ├── asset/
│   │   ├── avatar.png
│   │   ├── favicon.ico
│   │   ├── landing.png
│   │   └── welcome.png
│   │
│   ├── css/
│   │   ├── common.css
│   │   ├── index.css
│   │   ├── main.css
│   │   ├── mobile.css
│   │   └── presets.css
│   │
│   ├── script/
│   │   ├── common.js
│   │   ├── dashboard.js
│   │   ├── login.js
│   │   ├── main.js
│   │   └── register.js
│   │
│   ├── achievement.html
│   ├── base.html
│   ├── dashboard.html
│   ├── exercise_log.html
│   ├── index.html
│   ├── login.html
│   ├── main-base.html
│   ├── profile.html
│   ├── register.html
│   └── sharing.html
│
├── tests/
│   ├── selenium/
│   │   └── test_homepage.py
│   │
│   └── unit/
│       └── test_logic.py
│
├── run.py
├── README.md
└── requirements.txt

```

## 📃 License
MIT License — feel free to use, modify, and share.
