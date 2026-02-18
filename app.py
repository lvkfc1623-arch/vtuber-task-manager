import os
import json
from flask import Flask, render_template, request, redirect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
DATA_FILE = os.path.join(BASE_DIR, "tasks.json")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

tasks = load_tasks()  # 起動時ロード

@app.route("/", methods=["GET", "POST"])
def index():
    global tasks
    if request.method == "POST":
        text = request.form.get("task")
        if text:
            tasks.append({"text": text, "done": False})
            save_tasks(tasks)
        return redirect("/")
    return render_template("index.html", tasks=tasks)

@app.post("/delete/<int:task_id>")
def delete(task_id):
    global tasks
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect("/")

@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    global tasks
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
        save_tasks(tasks)
    return redirect("/")

@app.post("/edit/<int:task_id>")
def edit(task_id):
    global tasks
    new_text = request.form.get("task")
    if 0 <= task_id < len(tasks) and new_text:
        tasks[task_id]["text"] = new_text
        save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
