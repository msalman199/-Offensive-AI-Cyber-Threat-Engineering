from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
    <body>
        <h2>Ping Utility (Vulnerable for Testing)</h2>
        <form method="POST" action="/ping">
            <input type="text" name="host" placeholder="Enter IP or hostname">
            <input type="submit" value="Ping">
        </form>
    </body>
    </html>
    '''

@app.route('/ping', methods=['POST'])
def ping():
    host = request.form.get('host', '')
    # Vulnerable command execution
    try:
        result = subprocess.check_output(f"ping -c 3 {host}", shell=True, text=True)
        return f"<pre>{result}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
