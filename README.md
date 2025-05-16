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
###### **🍏 On macOS/Linux:**
```bash
source venv/bin/activate
```
###### **🪟 On Windows:**
```bash
venv\Scripts\activate
```
### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```
#### 3.1 Test Processes

- ##### Unit Tests

  ```bash
  #Run all unit tests.
  
  python -m pytest tests/unit/
  
  # Run a specific test file.
  
  python -m pytest tests/unit/test_chart_data.py
  python -m pytest tests/unit/test_exercise_log.py
  python -m pytest tests/unit/test_exercise_routes.py
  python -m pytest tests/unit/test_user_model.py
  python -m pytest tests/unit/test_user_model.py
  
  # Run a specific test method.
  
  python -m pytest tests/unit/test_user_model.py::TestUserModel::test_password_hashing
  ```

- ##### Selenium Tests
```bash
# Make sure you are in the virtual environment

# Run all Selenium tests
python -m pytest tests/selenium/

# Run a specific Selenium test
python -m pytest tests/selenium/test_homepage.py
python -m pytest tests/selenium/test_register_success.py
python -m pytest tests/selenium/test_login_success.py
python -m pytest tests/selenium/test_login_failure.py



# Run with detailed output
python -m pytest tests/selenium/test_homepage.py -v
python -m pytest tests/selenium/test_register_success.py -v
python -m pytest tests/selenium/test_login_success.py -v
python -m pytest tests/selenium/test_login_failure.py -v
```
### 4. Database Setup (Only on First Time Setup or New Device)

If you're running the app for the first time **on a new machine** (i.e. `app.db` does not exist), you must apply the database schema using Flask-Migrate:

🍏 **On macOS/Linux:**

```bash
# Make sure your virtualenv is activated
source venv/bin/activate

# Set the Flask app context (if not already set)
export FLASK_APP=run.py

# Run migrations to create the database schema
flask db upgrade
```
**🪟 On windows:**

```
# Make sure your virtualenv is activated
venv\Scripts\activate

# Set the Flask app context (if not already set)
$env:FLASK_ENV="development"

# Run migrations to create the database schema
flask --app run.py db upgrade
```



### 5. Run the Flask Application

```bash
python run.py
```
### 6. Results

```
http://127.0.0.1:5000
http://localhost:5000
```

## 📌 Notes
- `.venv/` and `.idea/` folders are excluded from version control via `.gitignore`.
- Always activate your virtual environment before running the app or installing dependencies.

## 📁 Sample Folder Structure (to be updated)
```bash
exercise-tracker-app/
│
├── backend/
│   ├── __init__.py        # App initialization, configuration and context handling
│   ├── config.py          # Configuration settings
│   ├── functions.py       # Core business logic functions
│   ├── models.py          # Database model definitions
│   └── routes.py          # Route definitions and handlers
│
├── frontend/
│   ├── asset/
│   │   ├── avatar.png     # Default avatar
│   │   ├── favicon.ico    # Website icon
│   │   ├── landing.png    # Landing page image
│   │   └── welcome.png    # Welcome page image
│   │
│   ├── css/
│   │   ├── common.css     # Common styles
│   │   ├── dashboard.css  # Dashboard styles
│   │   ├── index.css      # Index page styles
│   │   ├── main.css       # Main styles
│   │   ├── mobile.css     # Mobile responsive styles
│   │   └── presets.css    # Preset styles
│   │
│   ├── script/
│   │   ├── common.js      # Common JavaScript functionality
│   │   ├── dashboard.js   # Dashboard page functionality
│   │   ├── login.js       # Login page functionality
│   │   ├── main.js        # Main JavaScript functionality
│   │   └── register.js    # Registration page functionality
│   │
│   ├── achievement.html   # Achievement page template
│   ├── base.html          # Base HTML template
│   ├── dashboard.html     # Dashboard page template
│   ├── exercise_log.html  # Exercise log page template
│   ├── index.html         # Index page template
│   ├── login.html         # Login page template
│   ├── main-base.html     # Main base template
│   ├── profile.html       # Profile page template
│   ├── register.html      # Registration page template
│   ├── sharing.html       # Sharing page template
│   └── view-profile.html  # View profile page template
│
├── migrations/
│   ├── versions/
│   │   └── 5bd54c75d185_add_last_login_and_is_active_fields_to_.py  # Migration script
│   │
│   ├── alembic.ini        # Alembic configuration
│   ├── env.py             # Environment setup for migrations
│   ├── README             # Migration documentation
│   └── script.py.mako     # Template for migration scripts
│
├── tests/
│   ├── selenium/
│   │   └── test_homepage.py  # Homepage Selenium tests
│   │
│   └── unit/
│       ├── test_chart_data.py      # Chart data unit tests
│       ├── test_exercise_log.py    # Exercise log unit tests
│       ├── test_exercise_routes.py # Exercise routes unit tests
│       ├── test_user_model.py      # User model unit tests
│       └── test_user_routes.py     # User routes unit tests
│
├── instance/              # Instance-specific data (SQLite database)
│   └── app.db             # SQLite database file
│
├── run.py                # Application entry point
├── run_tests.py          # Test runner script
├── README.md             # Project documentation
├── requirements.txt      # Project dependencies
├── .env.example          # Example environment variables
└── .gitignore            # Git ignore configuration
```

## 📃 License
MIT License — feel free to use, modify, and share.
