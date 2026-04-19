import streamlit as st
from datetime import datetime
import urllib.parse

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="📚 राजहंस पुस्तक पेठ",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f6f8fb;
}

/* Header */
.header {
    background: linear-gradient(135deg,#ff7e5f,#feb47b);
    padding: 20px;
    border-radius: 15px;
    text-align:center;
    color:white;
}

/* Book Card */
.card {
    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0 4px 10px rgba(0,0,0,0.1);
    transition:0.3s;
}
.card:hover {
    transform:scale(1.03);
}

/* Price */
.price {
    color:#27ae60;
    font-weight:bold;
    font-size:18px;
}

/* Stock */
.stock-low { color:red; font-size:12px;}
.stock-ok { color:green; font-size:12px;}

/* Button */
.stButton button {
    border-radius:10px;
    background:#ff7e5f;
    color:white;
}

/* WhatsApp */
.whatsapp {
    background:#25D366;
    padding:12px;
    border-radius:30px;
    color:white;
    text-align:center;
    font-size:18px;
    text-decoration:none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
books = [
    {"id":1,"title":"लोक माझे संगती","author":"शरद पवार","price":650,"stock":10},
    {"id":2,"title":"छावा","author":"शिवाजी सावंत","price":750,"stock":3},
    {"id":3,"title":"मृत्युंजय","author":"शिवाजी सावंत","price":700,"stock":0},
    {"id":4,"title":"Atomic Habits","author":"James Clear","price":499,"stock":15},
]

# ---------------- CART ----------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
<h1>📚 राजहंस पुस्तक पेठ</h1>
<p>मराठी पुस्तकांचे विश्व</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SEARCH ----------------
search = st.text_input("🔍 पुस्तक शोधा")

# ---------------- FILTER ----------------
filtered = []
for b in books:
    if search.lower() in b["title"].lower() or search.lower() in b["author"].lower():
        filtered.append(b)
    elif search == "":
        filtered.append(b)

# ---------------- DISPLAY ----------------
cols = st.columns(3)

for i,book in enumerate(filtered):
    with cols[i % 3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.image("https://via.placeholder.com/150", use_container_width=True)

        st.subheader(book["title"])
        st.caption(book["author"])

        st.markdown(f'<p class="price">₹{book["price"]}</p>', unsafe_allow_html=True)

        if book["stock"] > 0:
            if book["stock"] <= 5:
                st.markdown(f'<p class="stock-low">⚠️ Only {book["stock"] left</p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p class="stock-ok">✅ Available</p>', unsafe_allow_html=True)

            qty = st.number_input("Qty",1,5,1,key=f"q{book['id']}")

            if st.button("🛒 Add", key=f"a{book['id']}"):
                st.session_state.cart[book["id"]] = {
                    "title":book["title"],
                    "price":book["price"],
                    "qty":qty
                }
                st.success("Added to cart")

        else:
            st.error("Out of stock")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CART ----------------
st.markdown("---")
st.subheader("🛒 Cart")

total = 0
for item in st.session_state.cart.values():
    st.write(f"{item['title']} x {item['qty']}")
    total += item["price"] * item["qty"]

st.write(f"### Total: ₹{total}")

# ---------------- WHATSAPP ORDER ----------------
name = st.text_input("Name")
phone = st.text_input("Phone")

if st.button("📲 WhatsApp Order"):
    msg = f"New Order\\nName:{name}\\nPhone:{phone}\\n"

    for item in st.session_state.cart.values():
        msg += f"{item['title']} x {item['qty']}\\n"

    msg += f"Total: ₹{total}"

    url = f"https://wa.me/919322630703?text={urllib.parse.quote(msg)}"

    st.markdown(f'<a href="{url}" class="whatsapp">Order on WhatsApp</a>', unsafe_allow_html=True)
