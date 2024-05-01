import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title('Streamlit 入門')

st.write('Interactive Widgets')
"Start"

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f"Iteration{i+1}")
    bar.progress(i+1)
    time.sleep(0.1)

"Done"

# left_column,right_column = st.columns(2)
# button = left_column.button("右カラムに文字を表示")
# if button:
#     right_column.write("ここは右カラム")


# expander = st.expander("問い合わせ")
# expander.write("問い合わせの回答")

# condition = st.slider("あなたの今の調子は？",0,100,50)
# "condition",condition


# text = st.text_input("あなたの好きな趣味を教えてください")
# "あなたの好きな趣味：",text



# option = st.selectbox(
#     "あなたが好きな数字を教えてください",
#     list(range(1,11))
# )
# "あなたの好きな数字は",option,"です．"


# if st.checkbox("Show Image"):
#     img = Image.open("bone33.png")
#     #Trueで幅に合わせて表示してくれる
#     st.image(img,caption="bone",use_column_width=False)


""" 
# 章
## 節
### 項

'''python
import streamlit as st
import numpy as np
import pandas as pd
'''
"""
