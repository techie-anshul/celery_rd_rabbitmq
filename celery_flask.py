from flask import Flask, request, jsonify
from celery_task import process_notebook

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Celery-Enabled Flask App!"
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return no content for the favicon

@app.route('/process_file', methods=['POST'])
def process_file():
    data = request.get_json()
    file_path = data.get('file_path')  # Path to the notebook file
    if not file_path:
        return jsonify({'error': 'File path is required'}), 400
    
    # Trigger Celery task
    task = process_notebook.apply_async(args=[file_path])
    return jsonify({'task_id': task.id}), 202

@app.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = process_notebook.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state}
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'error': str(task.info)}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
