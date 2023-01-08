from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
app.app_context().push()

from pos.menu.routes import menu
app.register_blueprint(menu)

db.create_all()
if __name__ == '__main__':
    app.run(debug=True)