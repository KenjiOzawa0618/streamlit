import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title("金価格可視化アプリ")

st.sidebar.write("""
こちらは金価格可視化ツールです．以下のオプションから表示日数を指定してください．
""")
st.sidebar.write("""
# 表示日数選択
""")
option = st.sidebar.radio(
    "",
    ("day","month","year")
)
if option == "day":
    #1～50，デフォルト20
    date = st.sidebar.slider("範囲を指定してください",1,100,10)
    st.write(f"""### 過去 **{date}日間**の金価格""")
if option == "month":
    #1～50，デフォルト20
    date = st.sidebar.slider("範囲を指定してください",1,36,12)
    st.write(f"""### 過去 **{date}月間**の金価格""")
if option == "year":
    #1～50，デフォルト20
    date = st.sidebar.slider("範囲を指定してください",1,100,100)
    st.write(f"""### 過去 **{date}年間**の金価格""")


#@st.cache
def get_data(date, exchange_rate):
    df = pd.DataFrame()
    #金価格をヤフーファイナンスから取得
    gold = yf.Ticker("GC=F")
    #可視化
    if option == "day":
        hist = gold.history(period =f"{date}d")
    if option == "month":
        hist = gold.history(period =f"{date}mo")
    if option == "year":
        hist = gold.history(period =f"{date}y")
    #使用データを終値のみを使用
    hist.index = hist.index.strftime("%Y-%m-%d")
    hist = hist[['Close']]
    hist = (hist/31.1035) * exchange_rate
    hist = round(hist, 2)
    #clumns名をGoldに変更
    hist.columns = ["Gold"]
    #転置
    hist= hist.T
    hist = hist.rename_axis("metals")
    #df = pd.concat([df,hist])
    return hist

try:
    if option == "day":
         st.sidebar.write("""## 金価格の範囲指定""")
         #（最小値，最大値，デフォルト）
         ymin,ymax = st.sidebar.slider("範囲を指定してください", 0,20000,(8600,10000))
    if option == "month":
        st.sidebar.write("""## 金価格の範囲指定""")
        #（最小値，最大値，デフォルト）
        ymin,ymax = st.sidebar.slider("範囲を指定してください", 0,20000,(7000,10000))
    if option == "year":
        st.sidebar.write("""## 金価格の範囲指定""")
        #（最小値，最大値，デフォルト）
        ymin,ymax = st.sidebar.slider("範囲を指定してください", 0,20000,(0,10000))
    
    st.sidebar.write(f"""### USD/JPYレートを入力してください""")
    exchange_rate = st.sidebar.number_input("数値を入力してください（半角）",value= 150.0)


#COMEX価格は通常、1トロイオンス（約31.1035グラム）単位で表示され、米ドルで表されます
    df = get_data(date, exchange_rate)
    #表を表示，sortで並び替え
    st.write("### 金価格 ", df.T.sort_index(ascending=False))
    #index部分からdateを取り除く
    data = df.T.reset_index()
    date_array = data['Date'].values
    data = pd.melt(data ,id_vars = ["Date"]).rename(columns = {"value":"Gold Prices(￥)"})
    chart = (
        alt.Chart(data)
        #mark_lineは折れ線グラフ，opacityは透明度，clip=Trueグラフの外に描かれるグラフを削除
        .mark_line(opacity=0.8,clip=True)
        .encode(
            #Tはタイム
            x="Date:T",
            #Q定量化
            y=alt.Y("Gold Prices(￥):Q", stack = None,scale=alt.Scale(domain=[ymin,ymax]))
        )
    )
    specific_date = '2023-09-08'  # 変更したい日付
    specific_value = (1918.4/31.1035) * exchange_rate # 仮の列名
    specific_value = round(specific_value, 2)
    # 金購入日が指定範囲内に入っていたら赤のポイントで示す
    if "2023-09-08" in date_array:
        # 特定の日付に点を追加
        highlight = alt.Chart(pd.DataFrame({'Date': [specific_date], 'Value': [specific_value]})).mark_point(color='red').encode(
            x='Date:T',
            y=alt.Y('Value:Q', axis=alt.Axis(title='Gold Prices(￥)'))  # y軸の値を指定
        )
        #use_container_width画面の幅に合わせる
        st.altair_chart(chart+highlight, use_container_width=True)
    else:
        st.altair_chart(chart, use_container_width=True)


except:
    st.error(
        "何かエラーが起きています"
    )

st.sidebar.write(f""" (購入2023/9/8 ￥{specific_value})""")

