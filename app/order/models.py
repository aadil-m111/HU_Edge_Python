from app import db

# without discount
# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     total_price = db.Column(db.Float, nullable=False)
#     status = db.Column(db.String(50), nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# discount added.
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())    # last order time detail.