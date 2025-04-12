from flask import Flask, request, render_template_string
import sqlite3
import os


app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Specimen Size Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #fff5f7; /* Very light pastel pink */
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        
        .calculator-container {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 400px;
        }
        
        h1 {
            color: #ff8fab; /* Pastel pink */
            text-align: center;
            margin-bottom: 25px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
        }
        
        input[type="text"],
        input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ffb3c6; /* Light pastel pink */
            border-radius: 8px;
            box-sizing: border-box;
        }
        
        button {
            background-color: #ff8fab; /* Pastel pink */
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px; /* Rounded edges */
            cursor: pointer;
            width: 100%;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        
        button:hover {
            background-color: #ff7096; /* Slightly darker pink on hover */
        }
        
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8e1e7; /* Very light pink */
            border-radius: 8px;
            text-align: center;
        }
        
        .result h2 {
            color: #ff8fab;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="calculator-container">
        <h1>Specimen Size Calculator</h1>
        
        <form method="POST">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            
            <div class="form-group">
                <label>Microscope Size (µm):</label>
                <input type="number" step="0.01" name="microscope_size" required>
            </div>
            
            <div class="form-group">
                <label>Magnification:</label>
                <input type="number" step="0.01" name="magnification" required>
            </div>
            
            <button type="submit">Calculate and Save</button>
        </form>
        
        {% if result %}
        <div class="result">
            <h2>Result</h2>
            <p>Actual size: {{ result }} µm</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Initialize database
def init_db():
    conn = sqlite3.connect('specimen_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS specimens
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT,
                      microscope_size REAL,
                      magnification REAL,
                      actual_size REAL)''')
    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    
    if request.method == 'POST':
    
        username = request.form['username']
        microscope_size = float(request.form['microscope_size'])
        magnification = float(request.form['magnification'])
        
        
        actual_size = microscope_size / magnification
        result = round(actual_size, 2)
        
        
        conn = sqlite3.connect('specimen_data.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO specimens 
                          (username, microscope_size, magnification, actual_size)
                          VALUES (?, ?, ?, ?)''',
                          (username, microscope_size, magnification, actual_size))
        conn.commit()
        conn.close()
    
    return render_template_string(HTML_TEMPLATE, result=result)


if __name__ == '__main__':
    try:
        app.run(
             host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
            debug=True
        )
    except Exception as e:
        print("Error starting Flask app:", e)
