import streamlit as st
import qrcode
from io import BytesIO
import uuid

# ---------- QR CODE FUNCTION ----------
def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Metro Ticket Booking")
st.title(" Metro Ticket Booking System")

# ---------- STATIONS ----------
stations = ["AMEERPET", "MIYAPUR", "LB NAGAR", "KPHB", "JNTU"]

# ---------- USER INPUTS ----------
name = st.text_input("Passenger Name")

source = st.selectbox("From Station", stations)
destination = st.selectbox("To Station", stations)

tickets = st.number_input("Number of Tickets", min_value=1, value=1)

cab_required = st.radio("Do you need a cab?", ["Yes", "No"])

drop_location = ""
if cab_required == "Yes":
    drop_location = st.text_input("Enter Drop Location")

# ---------- FARE CALCULATION ----------
price_per_ticket = 30
metro_fare = tickets * price_per_ticket

cab_fare = 100 if cab_required == "Yes" else 0

total_amount = metro_fare + cab_fare

st.info(f" Total Amount: ₹{total_amount}")

# ---------- BOOK BUTTON ----------
if st.button("Book Ticket"):
    if name.strip() == "":
        st.error("Please enter passenger name.")
    elif source == destination:
        st.error("Source and destination cannot be the same.")
    elif cab_required == "Yes" and drop_location.strip() == "":
        st.error("Please enter drop location for cab.")
    else:
        booking_id = str(uuid.uuid4())[:8]

        # ---------- QR DATA ----------
        qr_data = (
            f"Booking ID: {booking_id}\n"
            f"Name: {name}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"Tickets: {tickets}\n"
            f"Metro Fare: ₹{metro_fare}\n"
            f"Cab: {cab_required}\n"
            f"Drop: {drop_location if cab_required=='Yes' else 'N/A'}\n"
            f"Total: ₹{total_amount}"
        )

        qr_img = generate_qr(qr_data)

        # Convert QR image to bytes
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        qr_bytes = buf.getvalue()

        # ---------- OUTPUT ----------
        st.success(" Ticket Booked Successfully")

        st.subheader(" Metro Ticket Details")
        st.write("**Booking ID:**", booking_id)
        st.write("**Passenger Name:**", name)
        st.write("**From Station:**", source)
        st.write("**To Station:**", destination)
        st.write("**Number of Tickets:**", tickets)
        st.write("**Metro Fare:** ₹", metro_fare)

        st.subheader(" Cab Details")
        st.write("**Cab Required:**", cab_required)
        st.write("**Drop Location:**", drop_location if cab_required == "Yes" else "N/A")
        st.write("**Cab Fare:** ₹", cab_fare)

        st.subheader(" Total Amount Paid")
        st.write("₹", total_amount)

        st.image(qr_bytes, width=250)
