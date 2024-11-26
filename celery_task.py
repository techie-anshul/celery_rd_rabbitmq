import nbformat
from celery import Celery

app = Celery('celery_task', broker='amqp://guest:guest@127.0.0.1:5672//', backend='rpc://')

@app.task
def process_notebook(file_path):
    try:
        # Read the notebook
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Example processing: Count cells
        cell_count = len(notebook['cells'])
        
        # Example output
        return f"Notebook processed. Total cells: {cell_count}"
    except Exception as e:
        return f"Error processing notebook: {str(e)}"