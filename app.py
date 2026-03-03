from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ローカルはSQLite（デプロイ時は環境変数で差し替え可能にする）
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)

with app.app_context():
    db.create_all()

@app.get("/")
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("index.html", tasks=tasks)

@app.post("/add")
def add():
    text = request.form.get("task", "").strip()
    if text:
        db.session.add(Task(text=text))
        db.session.commit()
    return redirect(url_for("index"))

@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    t = Task.query.get_or_404(task_id)
    t.done = not t.done
    db.session.commit()
    return redirect(url_for("index"))

@app.post("/edit/<int:task_id>")
def edit(task_id):
    t = Task.query.get_or_404(task_id)
    new_text = request.form.get("task", "").strip()
    if new_text:
        t.text = new_text
        db.session.commit()
    return redirect(url_for("index"))

@app.post("/delete/<int:task_id>")
def delete(task_id):
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)