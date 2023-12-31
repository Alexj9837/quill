from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'your-secret-key-goes-here'

db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)