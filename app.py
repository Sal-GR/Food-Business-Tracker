from flask import Flask, render_template, request, redirect, url_for
from models import db, Purchases, DailyLogs

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food_financials.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
  db.create_all()

@app.route('/')
def home():
  return "Hello"

if __name__ == '__main__':
  app.run(debug=True)
