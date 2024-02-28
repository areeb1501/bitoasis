import streamlit as st
import requests

def fetch_crypto_price(pair):
    url = f"https://api.bitoasis.net/v1/exchange/ticker/{pair}"
    response = requests.get(url)
    data = response.json()
    return float(data['ticker']['last_price'])

def calculate_transaction(amount_aed, price, maker_fee=0.004, taker_fee=0.006, is_buy=True):
    fee_percentage = maker_fee if is_buy else taker_fee
    amount_after_fee = amount_aed / (1 + fee_percentage)
    crypto_amount = amount_after_fee / price
    fee_amount = amount_aed - amount_after_fee
    return crypto_amount, fee_amount

if 'investment_aed' not in st.session_state:
    st.session_state.investment_aed = 0

st.title("BitOasis Transaction Calculator")
pair_option = st.selectbox("Select Crypto Pair:", ["ETH-AED", "BTC-AED"])

pair_query = pair_option.replace("AED", "USD")
price = fetch_crypto_price(pair_query)

if "ETH" in pair_option:
    st.write(f"**ETH:** {price} USD (ETH-USD)")
elif "BTC" in pair_option:
    st.write(f"**BTC:** {price} USD (BTC-USD)")

investment_options = [1000, 5000, 10000]
def update_investment_amount():
    st.session_state.investment_aed = st.session_state.radio_investment_aed
st.radio("Select Investment Amount (AED):", investment_options, key="radio_investment_aed", on_change=update_investment_amount)

custom_investment_aed = st.number_input("Custom Investment Amount (AED):", min_value=10000.0, step=1000.0, format="%.2f", key="custom_investment_aed", on_change=lambda: setattr(st.session_state, 'investment_aed', st.session_state.custom_investment_aed))

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Buy (Green)")
    st.markdown(f"<span style='color:green; font-size:20px; font-weight:bold;'>Current Price: {price} AED</span>", unsafe_allow_html=True)
    crypto_buy, fee_buy = calculate_transaction(st.session_state.investment_aed, price, is_buy=True)
    st.write(f"Amount of Crypto: {crypto_buy}")
    st.write(f"Fee (Included): {fee_buy} AED")

with col2:
    st.markdown("### Sell (Red)")
    st.markdown(f"<span style='color:red; font-size:20px; font-weight:bold;'>Current Price: {price} AED</span>", unsafe_allow_html=True)
    crypto_sell, fee_sell = calculate_transaction(st.session_state.investment_aed, price, is_buy=False)
    st.write(f"Amount of Crypto: {crypto_sell}")
    st.write(f"Fee (Included): {fee_sell} AED")
