from flask import Flask, request, render_template_string, redirect, url_for
import csv
import os
from datetime import datetime

todo_webappv3 = Flask(__name__)

class Task:
    def __init__(self, title, priority='Medium', done='0', category='General', due_date=''):
        self.title = title
        self.priority = priority
        self.done = done
        self.category = category
        self.due_date = due_date

class TodoList:
    def __init__(self):
        self.file_name = 'todo.csv'
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        self.tasks = []
        if os.path.exists(self.file_name):
            with open(self.file_name) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) == 5:
                        self.tasks.append(Task(row[0], row[1], row[2], row[3], row[4]))

    def save_tasks(self):
        with open(self.file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for task in self.tasks:
                writer.writerow([task.title, task.priority, task.done, task.category, task.due_date])

    def create_task(self, title, priority='Medium', done='0', category='General', due_date=''):
        self.tasks.append(Task(title, priority, done, category, due_date))
        self.save_tasks()

    def delete_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.save_tasks()

    def update_task(self, title, field, new_value):
        for task in self.tasks:
            if task.title == title and hasattr(task, field):
                setattr(task, field, new_value)
        self.save_tasks()

    def filter_tasks(self, field=None, value=None):
        if not field or not value:
            return self.tasks
        return [task for task in self.tasks if value.lower() in getattr(task, field, '').lower()]

todo = TodoList()

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>To-Do List</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            background-color: #eef1f5;
        }
        .sidebar {
            width: 240px;
            background-color: #2c3e50;
            color: white;
            height: 100vh;
            padding: 20px;
            box-sizing: border-box;
        }
        .sidebar h2 {
            margin-bottom: 20px;
            font-size: 1.4em;
        }
        .sidebar ul {
            padding-top: 0;
            padding-bottom: 0;
            margin-top: 0;
            margin-bottom: 0;
        }
        .sidebar ul li {
            margin-bottom: 0;
            padding: 0;
        }
        .sidebar ul li a {
            text-decoration: none;
            color: white;
            display: flex;
            align-items: center;
            padding: 10px;
            background-color: #34495e;
            border-radius: 6px;
            transition: background-color 0.3s ease;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;
            height: auto;
            box-sizing: border-box;
            margin-bottom: 0;
        }
        .sidebar ul li a:hover {
            background-color: #3d566e;
        }
        .main {
            flex: 1;
            padding: 30px;
        }
        h1 {
            color: #34495e;
        }
        form {
            background: #fff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        input[type="text"], input[type="date"], select {
            padding: 8px;
            margin: 5px 10px 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            padding: 8px 15px;
            background-color: #2980b9;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background: #ffffff;
            padding: 12px;
            margin-bottom: 10px;
            border-left: 5px solid #2980b9;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        a {
            color: #e74c3c;
            text-decoration: none;
            float: right;
            margin-left: 10px;
        }
    </style>
</head>
<body>
<div class="sidebar">
    <h2>Menu</h2>
    <ul>
        <li><a href="/">🏠 All Tasks</a></li>
        <li><a href="/?field=category&value=Work">💼 Work</a></li>
        <li><a href="/?field=category&value=Home">🏡 Home</a></li>
        <li><a href="/?field=priority&value=High">⚠️ High Priority</a></li>
        <li><a href="/?field=done&value=0">🕒 Pending</a></li>
    </ul>
</div>
<div class="main">
    <h1>📝 To-Do List</h1>

    <form action="/add" method="post">
        <label>Title:</label> <input type="text" name="title" required>
        <label>Priority:</label> <select name="priority">
            <option>High</option>
            <option selected>Medium</option>
            <option>Low</option>
        </select>
        <label>Category:</label> <input type="text" name="category">
        <label>Due Date:</label> <input type="date" name="due_date">
        <input type="submit" value="Add Task">
    </form>

    <form method="get" action="/">
        <label>Filter by:</label>
        <select name="field">
            <option value="">None</option>
            <option value="priority">Priority</option>
            <option value="done">Done</option>
            <option value="category">Category</option>
            <option value="due_date">Due Date</option>
        </select>
        <input type="text" name="value">
        <input type="submit" value="Apply Filter">
    </form>

    <ul>
    {% for task in tasks %}
        <li style="opacity: {{ '0.5' if task.done == '1' else '1' }}">
            <strong>{{ task.title }}</strong> — {{ task.priority }} — Done: {{ task.done }} — {{ task.category }} — {{ task.due_date }}
            {% if task.done == '0' %}
                <a href="/done/{{ task.title }}" title="Mark as Done">✅</a>
            {% endif %}
            <a href="/delete/{{ task.title }}" title="Delete">🗑️</a>
        </li>
    {% endfor %}
    </ul>
</div>
</body>
</html>
"""

@todo_webappv3.route('/')
def index():
    todo.load_tasks()
    field = request.args.get('field')
    value = request.args.get('value')
    tasks = todo.filter_tasks(field, value)
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@todo_webappv3.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    priority = request.form.get('priority', 'Medium')
    category = request.form.get('category', 'General')
    due_date = request.form.get('due_date', '')
    todo.load_tasks()
    todo.create_task(title, priority, '0', category, due_date)
    return redirect(url_for('index'))

@todo_webappv3.route('/delete/<title>')
def delete(title):
    todo.load_tasks()
    todo.delete_task(title)
    return redirect(url_for('index'))

@todo_webappv3.route('/done/<title>')
def mark_done(title):
    todo.load_tasks()
    todo.update_task(title, 'done', '1')
    return redirect(url_for('index'))

if __name__ == '__main__':
    todo_webappv3.run(debug=True, host='0.0.0.0', port=5000)
