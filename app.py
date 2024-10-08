from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import math
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder, allowed extensions, and secret key
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'log'}
app.secret_key = 'supersecretkey'

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Example log data
logs = [
    {"ip": "192.168.1.1", "date": "2024-10-08 12:00:00", "method": "GET", "url": "/api/data", "status": "200", "size": "512"},
    {"ip": "192.168.1.2", "date": "2024-10-08 12:05:00", "method": "POST", "url": "/api/data", "status": "201", "size": "256"},
    {"ip": "192.168.1.3", "date": "2024-10-08 12:10:00", "method": "GET", "url": "/api/error", "status": "404", "size": "0"},
    # Add more log entries as needed
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part", "error")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No selected file", "error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash("File uploaded successfully!", "success")
            return redirect(url_for('logs_page'))
        else:
            flash("Invalid file type. Only .txt and .log are allowed", "error")
            return redirect(request.url)
    return render_template('index.html')

@app.route('/logs', methods=['GET'])
def logs_page():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_logs = len(logs)
    total_pages = math.ceil(total_logs / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_logs = logs[start:end]

    return render_template('logs.html', logs=paginated_logs, total_pages=total_pages, current_page=page)

# Route to download logs
@app.route('/download_logs', methods=['GET'])
def download_logs():
    log_file_path = os.path.join(UPLOAD_FOLDER, 'log_data.txt')
    
    # Write log data to the file
    with open(log_file_path, 'w') as f:
        for log in logs:
            f.write(f"{log['ip']} - {log['date']} - {log['method']} - {log['url']} - {log['status']} - {log['size']}\n")
    
    flash("Logs downloaded successfully!", "success")  # Flash message for download
    return send_file(log_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
