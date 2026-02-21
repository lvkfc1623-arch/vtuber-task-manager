import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return []


def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


@app.get("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.post("/add")
def add():
    text = (request.form.get("task") or "").strip()
    if text:
        tasks = load_tasks()
        tasks.append({"text": text, "done": False})
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.post("/toggle/<int:task_id>")
def toggle(task_id: int):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not bool(tasks[task_id].get("done", False))
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.post("/delete/<int:task_id>")
def delete(task_id: int):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.post("/edit/<int:task_id>")
def edit(task_id: int):
    new_text = (request.form.get("task") or "").strip()
    tasks = load_tasks()
    if 0 <= task_id < len(tasks) and new_text:
        tasks[task_id]["text"] = new_text
        save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)