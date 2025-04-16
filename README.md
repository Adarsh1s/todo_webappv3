# 📝 Flask To-Do List Web App

A simple and functional to-do list web application built using **Flask**. It enables users to manage their daily tasks through a clean and responsive UI, with features like categorization, priority levels, due dates, and completion tracking.

---

## 💡 About the Project

This project is a minimalist task management tool that runs on the web. It uses **Flask** for the backend logic, **HTML/CSS** for the frontend, and stores tasks in a **CSV file** instead of a traditional database.

Ideal for learners exploring Flask, web routing, and basic data persistence — as well as for anyone looking to manage their to-dos simply and effectively.

---

## ⚙️ How It Works

1. **Tasks are stored as rows in a `todo.csv` file**. Each row represents a task with the following fields:
   - Title
   - Priority (High / Medium / Low)
   - Completion status (`done`: 0 or 1)
   - Category (e.g., Work, Home)
   - Due Date

2. **Routes in Flask handle**:
   - `GET /` – Displays the list of tasks (optionally filtered).
   - `POST /add` – Adds a new task from the form submission.
   - `GET /delete/<title>` – Deletes a task by title.
   - `GET /done/<title>` – Marks a task as completed.

3. **Filtering** is supported through query parameters like:
   - `/?field=priority&value=High`
   - `/?field=category&value=Work`

4. The **frontend uses `render_template_string`** to dynamically generate HTML based on task data.

5. **Sidebar and forms** provide fast interaction for common operations.

---

## ✨ Features

- ✅ Add tasks with title, priority, category, and due date
- ✅ Mark tasks as done
- 🗑️ Delete tasks
- 🔍 Filter tasks by category, priority, status, and due date
- 🎨 User-friendly UI with sidebar navigation
- 💾 CSV-based storage (no database required)

---

## 🧠 Technologies Used

- **Python 3**
- **Flask**
- **HTML + CSS**
- **CSV for file-based storage**

---

## 🧩 Project Structure

```plaintext
flask-todo-app/
│
├── app.py              # Main Flask application with routes and logic
├── todo.csv            # Stores all tasks (each task is a row)
├── requirements.txt    # List of required Python packages
└── README.md           # Project documentation

---

## 🧠 Example Task (CSV Format)

```csv
Buy groceries,High,0,Home,2025-04-20
Finish Flask project,Medium,1,Work,2025-04-16
Call mom,Low,0,Personal,

---

## 📌 Use Cases
- **🧪 Learning how Flask works**
- **🛠️ Building a minimal productivity tool**
- **📚 Teaching beginner web development concepts**
- **🔖 Quick prototyping without a database**

---

