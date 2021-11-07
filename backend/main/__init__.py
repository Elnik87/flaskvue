from flask import Flask
from backend.config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
db.create_all()  # может выключу создание БД, хотя для postgres пофиг

# подключаем CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#from backend.main import views
from backend.main.views import apps
app.register_blueprint(apps, url_prefix="/")


