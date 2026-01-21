import streamlit as st
import ccxt
import time
import pandas as pd

st.set_page_config(page_title="Crypto Arbitrage Monitor", layout="wide")

st.title("🚀 Real-time Arbitrage Scanner")
st.write("Exchange နှစ်ခုကြားက ဈေးနှုန်းကွာဟချက်ကို API မလိုဘဲ စောင့်ကြည့်ခြင်း")

# စမ်းသပ်မည့် Coin အမျိုးအစား
symbol = st.selectbox("Select Coin", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT"])

# Exchange များ ချိတ်ဆက်ခြင်း
binance = ccxt.binance()
okx = ccxt.okx()

# Data သိမ်းရန် table
if 'history' not in st.session_state:
    st.session_state.history = []

placeholder = st.empty()

while True:
    try:
        # ဈေးနှုန်းများ ဆွဲယူခြင်း
        b_ticker = binance.fetch_ticker(symbol)
        o_ticker = okx.fetch_ticker(symbol)
        
        b_price = b_ticker['last']
        o_price = o_ticker['last']
        diff = b_price - o_price
        diff_percent = (abs(diff) / min(b_price, o_price)) * 100

        # UI မှာ ပြသခြင်း
        with placeholder.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("Binance Price", f"${b_price:,.2f}")
            col2.metric("OKX Price", f"${o_price:,.2f}")
            col3.metric("Difference", f"${diff:,.2f}", f"{diff_percent:.4f}%")

            # History ထဲ ထည့်ခြင်း
            st.session_state.history.append({
                "Time": time.strftime("%H:%M:%S"),
                "Diff": diff
            })
            
            # နောက်ဆုံးအကြိမ် 20 ကိုပဲပြမယ်
            df = pd.DataFrame(st.session_state.history[-20:])
            st.line_chart(df.set_index("Time"))
            
            st.table(df.tail(5))

        time.sleep(5) # ၅ စက္ကန့်တစ်ခါ update လုပ်မယ်
        st.rerun()

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        time.sleep(10)
