from flask import Flask, request, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute_python', methods=['POST'])
def run_python():
    file_location = request.json.get('file_location')

    if not os.path.isfile(file_location):
        return {"error": "El archivo no existe"}

    process = subprocess.Popen(["python3", file_location], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return {"output": stdout.decode("utf-8"), "error": stderr.decode("utf-8")}

if __name__ == '__main__':
    app.run(port=5000)
