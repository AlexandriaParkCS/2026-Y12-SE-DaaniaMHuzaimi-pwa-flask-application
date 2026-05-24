# 🌙 SleepTracker

A Progressive Web Application (PWA) for tracking your sleep patterns, built with Python and Flask.

**Created by:** Daania
**Year 12 Software Engineering — Assessment Task 2, 2026**

---

## What it does

SleepTracker lets you:
- Log your sleep every night (bedtime, wake time, quality rating, notes)
- See your sleep history and how long you slept each night
- Set a nightly sleep goal and track your progress
- Get a daily wellness quote on your dashboard
- Switch between Dark, Light, and Purple themes
- Install it on your phone like a real app (PWA)

---

## How to set it up

### Step 1 — Download the project from Github

### Step 2 — Install dependencies


pip install -r requirements.txt


### Step 3 — Run the app


cd src \
python app.py


### Step 4 — Open in your browser

Go to:
http://127.0.0.1:5000


---

## How to use the app

### Creating an account
1. Click **Register** on the login page
2. Enter a username, email, and password (minimum 8 characters)
3. Click **Register** — you'll be taken to the login page
4. Sign in with your email and password

### Logging sleep
1. Click **Log Sleep** in the navigation bar
2. Pick your **bedtime** and **wake time** using the date/time picker
3. Rate how you slept (1 = Very poor → 5 = Excellent)
4. Add any optional notes (e.g. "had coffee late", "stressed")
5. Click **Save entry**
6. You'll see a green message showing how many hours you slept

### Viewing your dashboard
- After logging in you land on the **Dashboard**
- It shows your recent sleep entries in a table
- A daily wellness quote appears at the bottom

### Viewing your history
- Click **History** to see all your past sleep entries
- Use the Edit button to change an entry
- Use the Delete button to remove an entry
- Entries are sorted newest first, 10 per page

### Setting a sleep goal
1. Click **Sleep Goal** in the navigation bar
2. Enter your target hours per night (e.g. 8)
3. Click **Save Goal**
4. Your goal progress will appear on the dashboard

### Switching themes
- Click the **☾ / ☀ / ♥** button in the top right of the navbar
- Cycles between: Dark → Light → Purple → Dark
- Your choice is saved and remembered next time

### Deleting your account
1. Go to **Sleep Goal**
2. Scroll to the bottom — **Danger Zone**
3. Click **Delete my account**
4. Confirm the dialog
5. Your account and ALL data are permanently removed

---


## Tech stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Database | SQLite3 via SQLAlchemy |
| Forms | WTForms + Flask-WTF |
| Passwords | bcrypt |
| Frontend | Jinja2, Bootstrap 5.3, CSS |
| PWA | Web App Manifest + Service Worker |
| External API | ZenQuotes |

---
