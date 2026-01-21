import streamlit as st
import ccxt
import time
import pandas as pd

st.title("🚀 Real-time Arbitrage Scanner (Bybit vs OKX)")

# Bybit နဲ့ OKX ကို သုံးမယ် (Streamlit Cloud မှာ ပိုအဆင်ပြေတယ်)
exchange1 = ccxt.bybit()
exchange2 = ccxt.okx()

symbol = st.selectbox("Select Coin", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])

placeholder = st.empty()

if 'history' not in st.session_state:
    st.session_state.history = []

while True:
    try:
        # Public API ကနေ ဈေးနှုန်းယူခြင်း
        t1 = exchange1.fetch_ticker(symbol)
        t2 = exchange2.fetch_ticker(symbol)
        
        p1, p2 = t1['last'], t2['last']
        diff = abs(p1 - p2)
        diff_pct = (diff / min(p1, p2)) * 100

        with placeholder.container():
            c1, c2, c3 = st.columns(3)
            c1.metric("Bybit Price", f"${p1:,.2f}")
            c2.metric("OKX Price", f"${p2:,.2f}")
            c3.metric("Difference", f"${diff:,.2f}", f"{diff_pct:.4f}%")
            
            # Graph ပြဖို့
            st.session_state.history.append({"Time": time.strftime("%H:%M:%S"), "Diff": diff})
            df = pd.DataFrame(st.session_state.history[-20:])
            st.line_chart(df.set_index("Time"))

        time.sleep(5)
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
        time.sleep(10)
