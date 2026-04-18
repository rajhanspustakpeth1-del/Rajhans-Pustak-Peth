from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    publisher = db.Column(db.String(200))
    isbn = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(300))
    rate = db.Column(db.Float)
    tot_in = db.Column(db.Integer, default=0)
    tot_out = db.Column(db.Integer, default=0)
    cl_bal = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'publisher': self.publisher,
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'rate': self.rate,
            'tot_in': self.tot_in,
            'tot_out': self.tot_out,
            'cl_bal': self.cl_bal,
            'available': self.cl_bal > 0
        }


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(200))
    total_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(50), default='pending')
    whatsapp_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def generate_order_number(self):
        return f"ORD-{self.id:06d}" if self.id else f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    title = db.Column(db.String(500))
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float)
    
    book = db.relationship('Book')
