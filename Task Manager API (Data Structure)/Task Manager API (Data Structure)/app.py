from flask import Flask, jsonify, request

app = Flask(__name__)

# Using a list to simulate a database
tasks = []
task_id = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id
    data=request.json
    task = {
        'id': task_id,
        'title': data["title"],
        'description': data['description'],
        'completed': False
    }
    tasks.append(task)
    task_id += 1
    return jsonify(task), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return jsonify(task)
    return jsonify({"message": "Task not found"})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task["title"]=  request.json.get('title',task['title'])    
            task['description'] = request.json.get('description', task['description'])
            task['completed'] = request.json.get('completed', task['completed'])
            return jsonify(task)
    return jsonify({"message": "Task not found"})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted"})
    return jsonify({"message": "Task not found"})

if __name__ == '__main__':
    app.run(debug=True)
