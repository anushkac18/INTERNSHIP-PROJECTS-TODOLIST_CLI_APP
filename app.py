from flask import Flask, render_template, request, redirect

app = Flask(__name__)
TASK_FILE = "tasks.txt"

def load_tasks():
    tasks = []
    try:
        with open(TASK_FILE, "r") as file:
            for line in file:
                status, text = line.strip().split(" | ", 1)
                tasks.append({"text": text, "done": status == "done"})
    except FileNotFoundError:
        pass
    return tasks

def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        for task in tasks:
            status = "done" if task["done"] else "todo"
            file.write(f"{status} | {task['text']}\n")

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()

    if request.method == "POST":
        if "add" in request.form:
            task_text = request.form.get("task")
            if task_text:
                tasks.append({"text": task_text, "done": False})
        elif "complete" in request.form:
            index = int(request.form.get("complete"))
            tasks[index]["done"] = not tasks[index]["done"]
        elif "delete" in request.form:
            index = int(request.form.get("delete"))
            tasks.pop(index)

        save_tasks(tasks)
        return redirect("/")

    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
