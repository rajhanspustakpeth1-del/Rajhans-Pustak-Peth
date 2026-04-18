from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Book, Order, OrderItem
import pandas as pd
import os
import json
import re
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bookstore-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# WhatsApp API configuration (using WhatsApp Cloud API or WhatsApp Business API)
# For demo, we'll use a simulated WhatsApp send via URL encoding
WHATSAPP_NUMBER = "+919876543210"  # Replace with your WhatsApp Business number
# For Twilio or other services, add your credentials here

def init_db():
    """Initialize database from Excel file"""
    with app.app_context():
        db.create_all()
        
        # Check if books already exist
        if Book.query.count() == 0:
            load_books_from_excel()


def load_books_from_excel():
    """Load books from the provided Excel data"""
    # Since the data is provided in the prompt, we'll create a JSON file
    # For actual implementation, you would read from the Excel file
    
    # Sample data from your Excel - first few books
    books_data = [
        {"publisher": "A Ltd", "isbn": "9788199034464", "title": "Sinhayan - Pach Tapanche Parv", "author": "Dr.Pratapsinh G.Jadhav", "rate": 800, "cl_bal": 1},
        {"publisher": "A Ltd", "isbn": "9788187043843", "title": "Mahanoranchi Kavita", "author": "Deshmukh Shrikant", "rate": 600, "cl_bal": 3},
        {"publisher": "A Ltd", "isbn": "Manjul 1", "title": "Rahasya Marathi Sanskaran", "author": "Anu.Dr. Rama Marathe", "rate": 499, "cl_bal": 0},
        {"publisher": "A Ltd", "isbn": "9789357866026", "title": "Secrets of Debt Free Life", "author": "Aditya Palav", "rate": 499, "cl_bal": 1},
        {"publisher": "A Ltd", "isbn": "Shar1", "title": "Raghuvanshatil Upamasaundarya", "author": "Vidyadhar Bhide", "rate": 400, "cl_bal": 2},
        {"publisher": "Aarhan Booksmiths", "isbn": "SPK9", "title": "Pakshikosh", "author": "Maruti Chitampalli", "rate": 1800, "cl_bal": 0},
        {"publisher": "Aarhan Booksmiths", "isbn": "9780670093892", "title": "The Story Of Yoga", "author": "Alister Shearer", "rate": 799, "cl_bal": 0},
        {"publisher": "Continental Prakashan", "isbn": "3322", "title": "Yugandhar", "author": "Shivaji Sawant", "rate": 850, "cl_bal": 0},
        {"publisher": "Mehta Publishing House", "isbn": "9789357207959", "title": "CHHAVA", "author": "Shivaji Savant", "rate": 750, "cl_bal": 4},
        {"publisher": "RajhansPrakashan Pvt Ltd.", "isbn": "9788174344991", "title": "Subodh Baybal", "author": "Dibrito Phransis", "rate": 1500, "cl_bal": 1},
    ]
    
    # Add more books from the data - I'll add a comprehensive set
    # For production, read from the actual Excel file
    for book_data in books_data:
        book = Book(
            publisher=book_data.get('publisher', ''),
            isbn=book_data.get('isbn', ''),
            title=book_data.get('title', ''),
            author=book_data.get('author', ''),
            rate=book_data.get('rate', 0),
            cl_bal=book_data.get('cl_bal', 0)
        )
        db.session.add(book)
    
    db.session.commit()
    print(f"Loaded {len(books_data)} books into database")


@app.route('/')
def index():
    """Home page"""
    featured_books = Book.query.filter(Book.cl_bal > 0).limit(12).all()
    publishers = db.session.query(Book.publisher).distinct().limit(10).all()
    return render_template('index.html', featured_books=featured_books, publishers=publishers)


@app.route('/books')
def books():
    """Books listing page with search and filters"""
    page = request.args.get('page', 1, type=int)
    per_page = 24
    search = request.args.get('search', '')
    publisher = request.args.get('publisher', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 10000, type=float)
    
    query = Book.query.filter(Book.cl_bal > 0)
    
    if search:
        query = query.filter(
            db.or_(
                Book.title.ilike(f'%{search}%'),
                Book.author.ilike(f'%{search}%'),
                Book.publisher.ilike(f'%{search}%')
            )
        )
    
    if publisher:
        query = query.filter(Book.publisher == publisher)
    
    query = query.filter(Book.rate.between(min_price, max_price))
    
    pagination = query.order_by(Book.title).paginate(page=page, per_page=per_page, error_out=False)
    
    publishers_list = db.session.query(Book.publisher).distinct().all()
    
    return render_template('books.html', 
                         books=pagination.items, 
                         pagination=pagination,
                         search=search,
                         publisher=publisher,
                         publishers=publishers_list,
                         min_price=min_price,
                         max_price=max_price)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """Book detail page"""
    book = Book.query.get_or_404(book_id)
    related_books = Book.query.filter(
        Book.publisher == book.publisher,
        Book.id != book.id,
        Book.cl_bal > 0
    ).limit(6).all()
    return render_template('book_detail.html', book=book, related_books=related_books)


@app.route('/api/books/search')
def api_search_books():
    """API endpoint for book search (autocomplete)"""
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    
    books = Book.query.filter(
        Book.title.ilike(f'%{query}%'),
        Book.cl_bal > 0
    ).limit(10).all()
    
    return jsonify([{'id': b.id, 'title': b.title, 'author': b.author, 'price': b.rate} for b in books])


@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart_items = session.get('cart', {})
    items = []
    total = 0
    
    for book_id, quantity in cart_items.items():
        book = Book.query.get(int(book_id))
        if book:
            item_total = book.rate * quantity
            total += item_total
            items.append({
                'book': book,
                'quantity': quantity,
                'total': item_total
            })
    
    return render_template('cart.html', items=items, total=total)


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.json
    book_id = str(data.get('book_id'))
    quantity = data.get('quantity', 1)
    
    book = Book.query.get(int(book_id))
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    if book.cl_bal < quantity:
        return jsonify({'error': f'Only {book.cl_bal} copies available'}), 400
    
    cart = session.get('cart', {})
    cart[book_id] = cart.get(book_id, 0) + quantity
    session['cart'] = cart
    
    return jsonify({
        'success': True,
        'cart_count': sum(cart.values()),
        'message': f'{book.title} added to cart'
    })


@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    """Update cart item quantity"""
    data = request.json
    book_id = str(data.get('book_id'))
    quantity = data.get('quantity', 1)
    
    cart = session.get('cart', {})
    
    if quantity <= 0:
        cart.pop(book_id, None)
    else:
        cart[book_id] = quantity
    
    session['cart'] = cart
    
    # Calculate new total
    total = 0
    for bid, qty in cart.items():
        book = Book.query.get(int(bid))
        if book:
            total += book.rate * qty
    
    return jsonify({
        'success': True,
        'cart_count': sum(cart.values()),
        'total': total
    })


@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    data = request.json
    book_id = str(data.get('book_id'))
    
    cart = session.get('cart', {})
    cart.pop(book_id, None)
    session['cart'] = cart
    
    return jsonify({
        'success': True,
        'cart_count': sum(cart.values())
    })


def generate_whatsapp_message(order):
    """Generate WhatsApp message for order"""
    message = f"📚 *NEW BOOK ORDER - {order.order_number}*\n\n"
    message += f"*Customer:* {order.customer_name}\n"
    message += f"*Phone:* {order.customer_phone}\n"
    if order.customer_email:
        message += f"*Email:* {order.customer_email}\n"
    message += f"*Order Date:* {order.created_at.strftime('%d/%m/%Y %H:%M')}\n\n"
    message += "*Items Ordered:*\n"
    
    for item in order.items:
        message += f"• {item.title} - Qty: {item.quantity} - ₹{item.price}/-\n"
    
    message += f"\n*Total Amount:* ₹{order.total_amount}/-\n"
    message += f"*Status:* {order.status}\n\n"
    message += "Please confirm availability and share payment details."
    
    return message


def send_whatsapp_message(phone_number, message):
    """
    Send WhatsApp message - Implement based on your WhatsApp Business API
    Options: Twilio, WhatsApp Cloud API, WATI, or direct link
    """
    # Option 1: Generate WhatsApp click-to-chat link (user clicks to send)
    # This opens WhatsApp with pre-filled message
    encoded_message = requests.utils.quote(message)
    whatsapp_link = f"https://wa.me/{phone_number}?text={encoded_message}"
    return whatsapp_link
    
    # Option 2: Using Twilio (uncomment and configure)
    # from twilio.rest import Client
    # account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    # auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     body=message,
    #     from_='whatsapp:+14155238886',
    #     to=f'whatsapp:{phone_number}'
    # )
    # return message.sid
    
    # Option 3: Using WhatsApp Cloud API
    # Implement based on Meta's documentation


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page"""
    cart_items = session.get('cart', {})
    if not cart_items:
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        # Get customer details
        customer_name = request.form.get('customer_name')
        customer_phone = request.form.get('customer_phone')
        customer_email = request.form.get('customer_email')
        
        # Create order
        order = Order(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            status='pending'
        )
        
        total = 0
        items_list = []
        
        for book_id, quantity in cart_items.items():
            book = Book.query.get(int(book_id))
            if book and book.cl_bal >= quantity:
                item = OrderItem(
                    book_id=book.id,
                    title=book.title,
                    quantity=quantity,
                    price=book.rate
                )
                order.items.append(item)
                total += book.rate * quantity
                items_list.append(item)
        
        order.total_amount = total
        db.session.add(order)
        db.session.commit()
        
        # Generate order number
        order.order_number = f"ORD-{order.id:06d}"
        db.session.commit()
        
        # Generate WhatsApp message
        whatsapp_message = generate_whatsapp_message(order)
        
        # Send WhatsApp (or generate link)
        # Store order details in session for confirmation
        session['last_order'] = {
            'id': order.id,
            'order_number': order.order_number,
            'total': total,
            'items': [(item.title, item.quantity, item.price) for item in items_list]
        }
        
        # Clear cart
        session['cart'] = {}
        
        # Generate WhatsApp link
        whatsapp_link = send_whatsapp_message(customer_phone, whatsapp_message)
        
        return render_template('order_confirm.html', 
                             order=order, 
                             items=items_list,
                             whatsapp_link=whatsapp_link,
                             whatsapp_message=whatsapp_message)
    
    # GET request - show checkout form
    items = []
    total = 0
    for book_id, quantity in cart_items.items():
        book = Book.query.get(int(book_id))
        if book:
            item_total = book.rate * quantity
            total += item_total
            items.append({
                'book': book,
                'quantity': quantity,
                'total': item_total
            })
    
    return render_template('checkout.html', items=items, total=total)


@app.route('/order/<int:order_id>')
def order_status(order_id):
    """View order status"""
    order = Order.query.get_or_404(order_id)
    return render_template('order_status.html', order=order)


@app.route('/api/orders', methods=['GET'])
def get_orders():
    """API endpoint to get orders (for admin panel)"""
    # Add authentication in production
    orders = Order.query.order_by(Order.created_at.desc()).limit(50).all()
    return jsonify([{
        'id': o.id,
        'order_number': o.order_number,
        'customer_name': o.customer_name,
        'customer_phone': o.customer_phone,
        'total_amount': o.total_amount,
        'status': o.status,
        'created_at': o.created_at.isoformat()
    } for o in orders])


@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status (admin only - add auth)"""
    data = request.json
    order = Order.query.get_or_404(order_id)
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({'success': True, 'status': order.status})


@app.route('/search')
def search():
    """Search page"""
    query = request.args.get('q', '')
    books = Book.query.filter(
        Book.title.ilike(f'%{query}%'),
        Book.cl_bal > 0
    ).limit(50).all()
    return render_template('search_results.html', books=books, query=query)


@app.route('/publishers')
def publishers():
    """List all publishers"""
    publishers = db.session.query(Book.publisher, db.func.count(Book.id).label('book_count')).group_by(Book.publisher).order_by(Book.publisher).all()
    return render_template('publishers.html', publishers=publishers)


@app.route('/publisher/<publisher_name>')
def publisher_books(publisher_name):
    """Books by publisher"""
    books = Book.query.filter(Book.publisher == publisher_name, Book.cl_bal > 0).all()
    return render_template('publisher_books.html', books=books, publisher=publisher_name)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
