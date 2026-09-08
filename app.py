from flask import Flask, render_template, request, redirect, url_for
from datetime import date as date_type
from sqlalchemy import func
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

@app.route('/purchases/add', methods=['GET', 'POST'])
def add_purchase():
    if request.method == 'POST':
        purchase = Purchases(
            date=request.form.get('date', date_type.today()),
            category=request.form['category'],
            amount=request.form['amount'],
            unit=request.form['unit'],
            price=request.form['price'],
        )
        db.session.add(purchase)
        db.session.commit()
        return redirect(url_for('add_purchase'))

    return render_template('add_purchase.html')


@app.route('/daily-logs/add', methods=['GET', 'POST'])
def add_daily_log():
    if request.method == 'POST':
        log = DailyLogs(
            date=request.form.get('date', date_type.today()),
            total_sales=request.form['total_sales'],
            food_used=request.form.get('food_used') or None,
            notes=request.form.get('notes'),
        )
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('add_daily_log'))

    return render_template('add_daily_log.html')


@app.route('/daily-logs')
def view_daily_logs():
    logs = DailyLogs.query.order_by(DailyLogs.date.desc()).all()

    summaries = []
    for log in logs:
        totals = dict(
            db.session.query(Purchases.category, func.sum(Purchases.price * Purchases.amount))
            .filter(Purchases.date == log.date)
            .group_by(Purchases.category)
            .all()
        )
        food_bought = totals.get('food', 0) or 0
        supplies_bought = totals.get('supplies', 0) or 0
        total_expenses = food_bought + supplies_bought

        summaries.append({
            'date': log.date,
            'total_sales': log.total_sales,
            'food_used': log.food_used,
            'food_bought': food_bought,
            'supplies_bought': supplies_bought,
            'total_expenses': total_expenses,
            'net_income': log.total_sales - total_expenses,
            'notes': log.notes,
        })

    return render_template('daily_logs.html', summaries=summaries)

if __name__ == '__main__':
  app.run(debug=True)
