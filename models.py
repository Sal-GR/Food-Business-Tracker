from datetime import date as date_type
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Purchases(db.Model):
  __tablename__ = "purchases"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  date = db.Column(db.Date, nullable=False, default=date_type.today, index=True)
  category = db.Column(db.String(50), nullable=False)
  amount = db.Column(db.Numeric(10, 2), nullable=False)
  unit = db.Column(db.String(20), nullable=False)
  price = db.Column(db.Numeric(10, 2), nullable=False)

  __table_args__ = (db.CheckConstraint("category IN ('food', 'supplies')", name="valid_category"),
                    db.CheckConstraint("amount > 0", name="valid_amount"),
                    db.CheckConstraint("price >= 0", name="valid_price"), 
                    db.CheckConstraint("unit IN ('single', 'pack', 'pounds', 'ounces', 'Gallons')", name="valid_unit")
  )

  def __repr__(self):
    return f"<Purchases {self.date} {self.category} ${self.amount}>"

class DailyLogs(db.Model):
  __tablename__ = "daily_logs"

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date, nullable=False, default=date_type.today, index=True,  unique=True)
  total_sales = db.Column(db.Numeric(10, 2), nullable=False)
  food_used = db.Column(db.Numeric(10, 2), nullable=True)
  notes = db.Column(db.String(200), nullable=True)

  __table_args__ = (db.CheckConstraint("total_sales >= 0", name="valid_total_sales"),
                    db.CheckConstraint("food_used >= 0", name="valid_food_used")
  )

  def __repr__(self):
    return f"<DailyLogs(date={self.date})>"
  