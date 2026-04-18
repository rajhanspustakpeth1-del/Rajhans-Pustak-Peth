import streamlit as st
from datetime import datetime
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="राजहंस पुस्तक पेठ - पुणे 038",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Book card styling */
    .book-card {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        height: 100%;
    }
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    /* Header styling */
    .shop-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    /* WhatsApp button */
    .whatsapp-btn {
        background-color: #25D366;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-weight: bold;
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
        color: white;
    }
    
    /* Price styling */
    .price {
        color: #2ecc71;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* Stock badge */
    .in-stock {
        color: #2ecc71;
        font-size: 0.8rem;
    }
    .out-of-stock {
        color: #ff4757;
        font-size: 0.8rem;
    }
    
    /* Address card */
    .address-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Timing card */
    .timing-card {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        background-color: #2c3e50;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Success message */
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Shop Information
SHOP_NAME = "राजहंस पुस्तक पेठ , पुणे 038"
WHATSAPP_NUMBER = "9322630703"
SHOP_ADDRESS = """
**पत्ता :** राजहंस पुस्तक पेठ  
साई सरस्वती ,शिक्षक नगर ,  
गल्ली क्र.०७ च्या सुरुवातीस ,परमहंस नगर ,  
वनाज जवळ , पौड रोड, वनाज मेट्रो स्टेशन जवळ ,  
कोथरूड , पुणे - ४११ ०३८  
**संपर्क :** 9322630703
"""
SHOP_TIMINGS = """
**वेळ :** मंगळवार ते रविवार  
**सकाळी १०:३० ते रात्री ०८:००**  
*(सोमवारी साप्ताहिक सुट्टी)*
"""

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'page' not in st.session_state:
    st.session_state.page = "books"


def load_books_data():
    """Load books from embedded data"""
    books = [
        {"id": 1, "publisher": "राजहंस प्रकाशन", "title": "लोक माझे संगती", "author": "शरद पवार", "price": 650, "stock": 65},
        {"id": 2, "publisher": "राजहंस प्रकाशन", "title": "शोध", "author": "मुरलीधर खैरनार", "price": 675, "stock": 776},
        {"id": 3, "publisher": "राजहंस प्रकाशन", "title": "महानायक", "author": "विश्वास पाटील", "price": 650, "stock": 79},
        {"id": 4, "publisher": "राजहंस प्रकाशन", "title": "बोक्या सातबांडे", "author": "दिलीप प्रभावळकर", "price": 150, "stock": 2019},
        {"id": 5, "publisher": "राजहंस प्रकाशन", "title": "सुबोध बायबल", "author": "डिब्रिटो फ्रान्सिस", "price": 1500, "stock": 1},
        {"id": 6, "publisher": "मेहता पब्लिशिंग हाऊस", "title": "छावा", "author": "शिवाजी सावंत", "price": 750, "stock": 4},
        {"id": 7, "publisher": "मेहता पब्लिशिंग हाऊस", "title": "शांताराम", "author": "अपर्णा वेलणकर", "price": 995, "stock": 23},
        {"id": 8, "publisher": "मेहता पब्लिशिंग हाऊस", "title": "मृत्युंजय", "author": "शिवाजी सावंत", "price": 700, "stock": 68},
        {"id": 9, "publisher": "कॉन्टिनेंटल प्रकाशन", "title": "युगंधर", "author": "शिवाजी सावंत", "price": 850, "stock": 0},
        {"id": 10, "publisher": "ग्रंथाली", "title": "मी बहुरूपी", "author": "अशोक सराफ", "price": 600, "stock": 47},
        {"id": 11, "publisher": "मंजुळ पब्लिशिंग", "title": "अ‍ॅटॉमिक हॅबिट्स", "author": "जेम्स क्लियर", "price": 499, "stock": 39},
        {"id": 12, "publisher": "आय बी डी", "title": "अ‍ॅटॉमिक हॅबिट्स", "author": "जेम्स क्लियर", "price": 899, "stock": 45},
        {"id": 13, "publisher": "आय बी डी", "title": "थिंकिंग फास्ट अँड स्लो", "author": "डॅनियेल काह्नेमन", "price": 799, "stock": 13},
        {"id": 14, "publisher": "देशमुख अँड कंपनी", "title": "युगप्रवर्तक छत्रपती", "author": "नरहर कुरुंदकर", "price": 600, "stock": 116},
        {"id": 15, "publisher": "देशमुख अँड कंपनी", "title": "युगांत", "author": "इरावती कर्वे", "price": 400, "stock": 400},
        {"id": 16, "publisher": "मौज प्रकाशन गृह", "title": "मौज दिवाळी अंक", "author": "संपादित", "price": 400, "stock": 1757},
        {"id": 17, "publisher": "सकाळ पेपर्स", "title": "आयुर्वेदीय गर्भसंस्कार", "author": "डॉ. बाळाजी तांबे", "price": 990, "stock": 27},
        {"id": 18, "publisher": "सकाळ पेपर्स", "title": "श्यामची आई", "author": "साने गुरुजी", "price": 180, "stock": 2},
        {"id": 19, "publisher": "ए लि.", "title": "सिंहयान", "author": "डॉ. प्रतापसिंह जाधव", "price": 800, "stock": 1},
        {"id": 20, "publisher": "ए लि.", "title": "महारौरंची कविता", "author": "देशमुख श्रीकांत", "price": 600, "stock": 3},
        {"id": 21, "publisher": "ए लि.", "title": "रहस्य मराठी संस्करण", "author": "अनु. डॉ. रामा मराठे", "price": 499, "stock": 0},
        {"id": 22, "publisher": "आरहान बुकस्मिथ्स", "title": "पक्षिकोश", "author": "मारुती चितमपल्ली", "price": 1800, "stock": 0},
        {"id": 23, "publisher": "राजहंस प्रकाशन", "title": "भारताची कुळकथा", "author": "मधुकर केशव धवलीकर", "price": 450, "stock": 83},
        {"id": 24, "publisher": "राजहंस प्रकाशन", "title": "मनोभावे देशदर्शन", "author": "शशिधर भावे", "price": 125, "stock": 23},
        {"id": 25, "publisher": "राजहंस प्रकाशन", "title": "बोक्या सातबांडे भाग २", "author": "दिलीप प्रभावळकर", "price": 140, "stock": 10},
    ]
    return books


def get_whatsapp_link(phone_number, message):
    """Generate WhatsApp link"""
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{phone_number}?text={encoded_message}"


def generate_order_message(cart_items, customer_name, customer_phone, total_amount):
    """Generate WhatsApp order message"""
    message = f"""*📚 नवीन ऑर्डर - राजहंस पुस्तक पेठ*

*ग्राहक माहिती:*
👤 नाव: {customer_name}
📞 फोन: {customer_phone}

*🛒 ऑर्डर तपशील:*
"""
    for item in cart_items:
        message += f"\n• *{item['title']}* \n  प्रमाण: {item['quantity']} | ₹{item['price']}/-"
    
    message += f"\n\n*💰 एकूण रक्कम:* ₹{total_amount}/-"
    message += f"\n\n*📍 दुकान:* {SHOP_NAME}"
    message += f"\n*📅 दिनांक:* {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    message += "\n\n*कृपया उपलब्धता आणि पेमेंट तपशील पाठवा.*"
    message += "\n\n🙏 धन्यवाद!"
    
    return message


def show_shop_header():
    """Display shop header"""
    st.markdown(f"""
    <div class="shop-header">
        <h1>📚 {SHOP_NAME}</h1>
        <p style="font-size: 1.2rem;">मराठी पुस्तकांचे विश्व - ४०+ वर्षांचा वारसा</p>
        <a href="https://wa.me/{WHATSAPP_NUMBER}" class="whatsapp-btn" target="_blank">
            💬 WhatsApp वर संपर्क साधा
        </a>
    </div>
    """, unsafe_allow_html=True)


def show_shop_info():
    """Display shop information in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("## 🏪 शॉप माहिती")
        
        st.markdown(f"""
        <div class="address-card">
            <h4>📍 पत्ता</h4>
            {SHOP_ADDRESS}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="timing-card">
            <h4>⏰ वेळ</h4>
            {SHOP_TIMINGS}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 1rem;">
            <a href="tel:{WHATSAPP_NUMBER}" style="text-decoration: none;">
                <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">
                    📞 कॉल करा: {WHATSAPP_NUMBER}
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Search Filter
        st.markdown("## 🔍 पुस्तक शोधा")
        search_term = st.text_input("शोधा (Title / Author)", placeholder="पुस्तकाचे नाव किंवा लेखक...", key="search_input")
        
        # Publisher Filter
        books_data = load_books_data()
        publishers = sorted(list(set([b['publisher'] for b in books_data])))
        selected_publisher = st.selectbox("प्रकाशक निवडा", ["सर्व"] + publishers, key="publisher_select")
        
        # Price Filter
        st.markdown("### 💰 किंमत श्रेणी")
        price_range = st.slider("किंमत (₹)", 0, 2000, (0, 2000), key="price_slider")
        
        # Stock Filter
        show_only_instock = st.checkbox("फक्त उपलब्ध पुस्तके दाखवा", value=True, key="stock_checkbox")
        
        st.markdown("---")
        
        # Cart Summary
        st.markdown("## 🛒 कार्ट")
        if st.session_state.cart:
            cart_total = 0
            cart_items_count = 0
            for item in st.session_state.cart.values():
                cart_total += item['price'] * item['quantity']
                cart_items_count += item['quantity']
            st.markdown(f"**एकूण वस्तू:** {cart_items_count}")
            st.markdown(f"**एकूण किंमत:** ₹{cart_total}/-")
            if st.button("🗑️ कार्ट साफ करा", key="clear_cart"):
                st.session_state.cart = {}
                st.rerun()
        else:
            st.info("कार्ट रिकामी आहे")
        
        return search_term, selected_publisher, price_range, show_only_instock


def display_books(books, search_term="", selected_publisher="सर्व", price_range=(0, 2000), show_only_instock=True):
    """Display books in grid layout"""
    
    # Apply filters
    filtered = books.copy()
    
    if search_term:
        search_lower = search_term.lower()
        filtered = [b for b in filtered if 
                   search_lower in b['title'].lower() or 
                   search_lower in b.get('author', '').lower()]
    
    if selected_publisher != "सर्व":
        filtered = [b for b in filtered if b['publisher'] == selected_publisher]
    
    filtered = [b for b in filtered if price_range[0] <= b['price'] <= price_range[1]]
    
    if show_only_instock:
        filtered = [b for b in filtered if b['stock'] > 0]
    
    # Display results count
    st.markdown(f"### 📖 पुस्तके ({len(filtered)} उपलब्ध)")
    
    if not filtered:
        st.warning("कोणतीही पुस्तके सापडली नाहीत. कृपया फिल्टर बदला.")
        return
    
    # Display books in grid
    cols_per_row = 3
    for i in range(0, len(filtered), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(filtered):
                book = filtered[idx]
                with col:
                    stock_status = "✅ उपलब्ध" if book['stock'] > 0 else "❌ स्टॉक संपला"
                    stock_class = "in-stock" if book['stock'] > 0 else "out-of-stock"
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="book-card">
                            <div style="text-align: center;">
                                <div style="font-size: 3rem;">📖</div>
                                <h4 style="font-size: 1rem; margin: 0.5rem 0;">{book['title'][:45]}{'...' if len(book['title']) > 45 else ''}</h4>
                                <p style="color: #666; font-size: 0.8rem; margin: 0;">{book.get('author', 'लेखक अज्ञात')[:35]}</p>
                                <p style="color: #888; font-size: 0.7rem;">{book['publisher'][:30]}</p>
                                <p class="price">₹{book['price']}/-</p>
                                <p class="{stock_class}">{stock_status} ({book['stock']} प्रती)</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if book['stock'] > 0:
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                quantity = st.number_input(f"प्रमाण", min_value=1, max_value=min(book['stock'], 10), value=1, key=f"qty_{book['id']}", label_visibility="collapsed")
                            with col2:
                                if st.button(f"🛒 घाला", key=f"add_{book['id']}"):
                                    if str(book['id']) in st.session_state.cart:
                                        st.session_state.cart[str(book['id'])]['quantity'] += quantity
                                    else:
                                        st.session_state.cart[str(book['id'])] = {
                                            'id': book['id'],
                                            'title': book['title'],
                                            'price': book['price'],
                                            'quantity': quantity,
                                            'author': book.get('author', ''),
                                            'publisher': book['publisher']
                                        }
                                    st.success(f"✅ {book['title'][:30]} कार्ट मध्ये घातले!")
                                    st.rerun()
                        else:
                            st.button(f"❌ स्टॉक संपला", disabled=True, key=f"disabled_{book['id']}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)


def show_cart_page():
    """Display cart page"""
    st.markdown("## 🛒 तुमचे कार्ट")
    
    if not st.session_state.cart:
        st.info("तुमचे कार्ट रिकामे आहे. कृपया पुस्तके जोडा.")
        if st.button("📚 पुस्तके बघा", key="back_to_books"):
            st.session_state.page = "books"
            st.rerun()
        return
    
    # Display cart items
    cart_items = []
    total = 0
    
    for item_id, item in st.session_state.cart.items():
        cart_items.append(item)
        total += item['price'] * item['quantity']
    
    # Cart display
    for idx, item in enumerate(cart_items):
        col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
        with col1:
            st.write(item['title'][:40])
        with col2:
            st.write(item.get('author', '-')[:25])
        with col3:
            st.write(f"₹{item['price']}")
        with col4:
            new_qty = st.number_input("", min_value=0, max_value=10, value=item['quantity'], key=f"edit_{item['id']}", label_visibility="collapsed")
            if new_qty != item['quantity']:
                if new_qty == 0:
                    del st.session_state.cart[str(item['id'])]
                else:
                    st.session_state.cart[str(item['id'])]['quantity'] = new_qty
                st.rerun()
        with col5:
            st.write(f"₹{item['price'] * item['quantity']}")
        st.divider()
    
    # Total and checkout
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        st.markdown(f"### एकूण: ₹{total}/-")
    
    with col3:
        if st.button("🗑️ कार्ट साफ करा", key="clear_cart_page"):
            st.session_state.cart = {}
            st.rerun()
    
    st.markdown("---")
    
    # Checkout Form
    st.markdown("## 📝 ऑर्डर फॉर्म")
    st.markdown("कृपया खालील माहिती भरा:")
    
    with st.form("order_form"):
        customer_name = st.text_input("तुमचे नाव *", placeholder="उदा. राजेश शर्मा")
        customer_phone = st.text_input("मोबाईल नंबर *", placeholder="उदा. 9876543210")
        customer_email = st.text_input("ईमेल (पर्यायी)", placeholder="example@email.com")
        
        submitted = st.form_submit_button("📱 WhatsApp वर ऑर्डर पाठवा", use_container_width=True)
        
        if submitted:
            if not customer_name or not customer_phone:
                st.error("कृपया तुमचे नाव आणि मोबाईल नंबर भरा.")
            else:
                order_message = generate_order_message(cart_items, customer_name, customer_phone, total)
                whatsapp_link = get_whatsapp_link(WHATSAPP_NUMBER, order_message)
                
                st.success("✅ ऑर्डर तयार आहे!")
                
                st.markdown(f"""
                <div style="background-color: #d4edda; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h4>📋 ऑर्डर सारांश</h4>
                    <p><strong>नाव:</strong> {customer_name}</p>
                    <p><strong>मोबाईल:</strong> {customer_phone}</p>
                    <p><strong>एकूण रक्कम:</strong> ₹{total}/-</p>
                    <p><strong>एकूण पुस्तके:</strong> {len(cart_items)}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: center; margin: 1rem 0;">
                    <a href="{whatsapp_link}" target="_blank">
                        <button style="background-color: #25D366; color: white; padding: 15px 40px; font-size: 1.2rem; border: none; border-radius: 50px; cursor: pointer;">
                            💬 WhatsApp वर ऑर्डर पाठवा
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("👆 वरील बटणावर क्लिक केल्यानंतर WhatsApp उघडेल. कृपया ऑर्डर पाठवा.")
                
                if st.button("🔄 नवीन ऑर्डरसाठी कार्ट साफ करा", key="clear_after_order"):
                    st.session_state.cart = {}
                    st.rerun()


def show_contact_page():
    """Display contact page"""
    st.markdown("## 📞 संपर्क माहिती")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="address-card">
            <h3>🏪 शॉप पत्ता</h3>
            {SHOP_ADDRESS}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="timing-card">
            <h3>⏰ दुकानाची वेळ</h3>
            {SHOP_TIMINGS}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📱 आमच्याशी संपर्क साधा")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <a href="tel:{WHATSAPP_NUMBER}" target="_blank">
            <button style="width: 100%; padding: 12px; background-color: #4CAF50; color: white; border: none; border-radius: 8px; cursor: pointer;">
                📞 कॉल करा
            </button>
        </a>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank">
            <button style="width: 100%; padding: 12px; background-color: #25D366; color: white; border: none; border-radius: 8px; cursor: pointer;">
                💬 WhatsApp
            </button>
        </a>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <a href="mailto:rajhansbooks@gmail.com" target="_blank">
            <button style="width: 100%; padding: 12px; background-color: #2196F3; color: white; border: none; border-radius: 8px; cursor: pointer;">
                📧 ईमेल
            </button>
        </a>
        """, unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Show shop header
    show_shop_header()
    
    # Sidebar filters
    search_term, selected_publisher, price_range, show_only_instock = show_shop_info()
    
    # Page navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📚 सर्व पुस्तके", use_container_width=True, key="nav_books"):
            st.session_state.page = "books"
    with col2:
        cart_count = sum(item['quantity'] for item in st.session_state.cart.values()) if st.session_state.cart else 0
        button_text = f"🛒 कार्ट ({cart_count})" if cart_count > 0 else "🛒 कार्ट"
        if st.button(button_text, use_container_width=True, key="nav_cart"):
            st.session_state.page = "cart"
    with col3:
        if st.button("📞 संपर्क", use_container_width=True, key="nav_contact"):
            st.session_state.page = "contact"
    
    st.markdown("---")
    
    # Load books
    books_data = load_books_data()
    
    # Display appropriate page
    if st.session_state.page == "books":
        display_books(books_data, search_term, selected_publisher, price_range, show_only_instock)
    elif st.session_state.page == "cart":
        show_cart_page()
    elif st.session_state.page == "contact":
        show_contact_page()
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <p><strong>© 2024 {SHOP_NAME}</strong> | मराठी पुस्तकांचे विश्व</p>
        <p>व्यवसायिक दुकान क्रमांक: Kothrud Pune 038 | स्थापना: 2016</p>
        <p style="font-size: 0.8rem;">सोमवारी साप्ताहिक सुट्टी</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
