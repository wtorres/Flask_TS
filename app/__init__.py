from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
from models import UserAdmin, TradeAdmin, ScrapAdmin


# Create admin
admin = admin.Admin(app, name='CRUD USER TS', template_mode='bootstrap2')
admin.add_view(UserAdmin(models.User, db.session))
admin.add_view(TradeAdmin(models.Trade, db.session))
admin.add_view(ScrapAdmin(models.Scrap, db.session))




