


# app.py
from flask import Flask,render_template
from routes import setup_routes
from config import db_init

import os

app = Flask(__name__, template_folder=os.path.abspath("templates"))  # Ensure correct path

print("Template folder set to:", os.path.abspath("templates"))  # Debugging

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/medicine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_init(app)
setup_routes(app)  # Already registers the '/' route

if __name__ == "__main__":
    app.run(debug=True)
