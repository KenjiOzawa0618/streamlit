import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st
from datetime import datetime

st.title("金価格可視化アプリ")

st.sidebar.write("""
こちらは金価格可視化ツールです．以下のオプションから表示期間を指定してください．
""")
st.sidebar.write("""
# 表示期間選択
""")
option = st.sidebar.radio(
    "表示期間を選択してください",
    ("day", "month", "year")
)
if option == "day":
    date = st.sidebar.slider("範囲を指定してください", 1, 5, 1)  # '10d' は無効なため、1dか5dに変更
    period = f"{date}d" if date == 1 else "5d"
    st.write(f"""### 過去 **{date}日間**の金価格""")
elif option == "month":
    date = st.sidebar.slider("範囲を指定してください", 1, 6, 1)  # '10mo' は無効なため、1moか3moに変更
    period = f"{date}mo" if date == 1 else "3mo"
    st.write(f"""### 過去 **{date}月間**の金価格""")
elif option == "year":
    date = st.sidebar.slider("範囲を指定してください", 1, 10, 1)  # '100y' は無効なため、1yか5yに変更
    period = f"{date}y" if date == 1 else "5y"
    st.write(f"""### 過去 **{date}年間**の金価格""")

def get_data(period, exchange_rate):
    df = pd.DataFrame()
    gold = yf.Ticker("GC=F")
    hist = gold.history(period=period)
    hist.index = hist.index.strftime("%Y-%m-%d")
    hist = hist[['Close']]
    hist = (hist / 31.1035) * exchange_rate
    hist = round(hist, 2)
    hist.columns = ["Gold"]
    hist = hist.T
    hist = hist.rename_axis("metals")
    return hist

def get_price_on_date(date):
    gold = yf.Ticker("GC=F")
    data = gold.history(period="max")
    date_str = pd.to_datetime(date).strftime('%Y-%m-%d')
    try:
        return data.loc[date_str]['Close']
    except KeyError:
        return None

def get_price_on_latest_date():
    gold = yf.Ticker("GC=F")
    data = gold.history(period="max")
    latest_date = data.index[-1]
    return latest_date.strftime('%Y-%m-%d'), data.loc[latest_date]['Close']

st.sidebar.write("""## 金価格の範囲指定""")
if option == "day":
    ymin, ymax = st.sidebar.slider("範囲を指定してください", 0, 20000, (9000, 12000))
elif option == "month":
    ymin, ymax = st.sidebar.slider("範囲を指定してください", 0, 20000, (7000, 15000))
elif option == "year":
    ymin, ymax = st.sidebar.slider("範囲を指定してください", 0, 20000, (0, 15000))

st.sidebar.write("### USD/JPYレートを入力してください")
exchange_rate = st.sidebar.number_input("数値を入力してください（半角）", value=150.0)

purchase_date = st.sidebar.date_input("購入日を入力してください", value=pd.to_datetime("2023-09-07"),
                                      min_value=pd.to_datetime("2000-01-01"), max_value=datetime.now())

st.write(f"購入日: {purchase_date}")

gold_price_purchase = get_price_on_date(purchase_date.strftime("%Y-%m-%d"))
gold_price_jpy_purchase = round((gold_price_purchase / 31.1035) * exchange_rate, 2) if gold_price_purchase else None

today = datetime.now()
latest_date, gold_price_latest = get_price_on_latest_date()
gold_price_jpy_latest = round((gold_price_latest / 31.1035) * exchange_rate, 2)
profit = round(gold_price_jpy_latest - gold_price_jpy_purchase, 2) if gold_price_jpy_purchase else None

df = get_data(period, exchange_rate)
if profit is not None:
    st.markdown(f"""
    <h3>1gあたりの利益：<span style='color: red;'>￥{profit:.2f}</span></h3>""", unsafe_allow_html=True)
else:
    st.markdown("<h3>購入日の日付が無効です</h3>", unsafe_allow_html=True)

st.write("### 金価格 ", df.T.sort_index(ascending=False))
st.write(f"###### 購入日は赤まるで囲まれます")
data = df.T.reset_index()
date_array = data['Date'].values
data = pd.melt(data, id_vars=["Date"]).rename(columns={"value": "Gold Prices(￥)"})
chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Gold Prices(￥):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax]))
    )
)

if purchase_date.strftime("%Y-%m-%d") in date_array:
    highlight = alt.Chart(pd.DataFrame({'Date': [purchase_date], 'Value': [gold_price_jpy_purchase]})).mark_point(color='red').encode(
        x='Date:T',
        y=alt.Y('Value:Q', axis=alt.Axis(title='Gold Prices(￥)'))
    )
    st.altair_chart(chart + highlight, use_container_width=True)
else:
    st.altair_chart(chart, use_container_width=True)

if gold_price_jpy_purchase is not None:
    st.sidebar.write(f""" (購入日：{purchase_date} ￥{gold_price_jpy_purchase})""")
else:
    st.sidebar.write("購入日のデータがありません")
st.sidebar.write(f""" (最新：{latest_date} ￥{gold_price_jpy_latest})""")
